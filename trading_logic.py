# trading_logic.py
# Ron Company #

import time
import numpy as np
import pandas as pd
import talib
from ta.trend import MACD
from exchange_manager import exchange_manager, get_trading_fees
from data_manager import fetch_balance, fetch_current_price, fetch_current_volume
import ccxt
from neural_network import train_models, predict_next_close
from sklearn.cluster import KMeans

class TradingBot:
    def __init__(self):
        self.bot_running = False
        self.active_trade = False  # Флаг для проверки активной сделки
        self.exchange = exchange_manager.get_exchange()  # Создаем объект биржи

    def fetch_binance_data(self, symbol, timeframe='1h', limit=500):
        """Получает исторические данные с Binance с использованием CCXT."""
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            if df.empty:
                print(f"Ошибка: Не удалось получить данные для {symbol}. Полученные данные пустые.")
            return df
        except Exception as e:
            print(f"Ошибка при получении данных с Binance: {e}")
            return pd.DataFrame()

    def calculate_entry_amount(self, entry_percentage, leverage):
        """Рассчитывает сумму входа на основе процента от баланса и проверяет минимальное требование."""
        balance = fetch_balance()
        entry_amount = balance * (entry_percentage / 100)
        min_required_amount = 100 / leverage  # Минимальная сумма с учетом плеча

        if entry_amount < min_required_amount:
            print(f"Минимальная сумма для сделки с плечом {leverage} составляет {min_required_amount} USDT.")
            entry_amount = min_required_amount
        return entry_amount

    def find_price_zones(self, df, price_range=100):
        """Находит зоны плотности свечей, которые находятся в пределах указанного диапазона."""
        support_zones = []
        resistance_zones = []

        for i in range(len(df) - 2):
            min_price = min(df['low'][i:i + 3])
            max_price = max(df['high'][i:i + 3])

            if max_price - min_price <= price_range:
                zone_center = (max_price + min_price) / 2
                if df['close'][i] < zone_center:
                    support_zones.append(zone_center)
                else:
                    resistance_zones.append(zone_center)

        support = min(support_zones) if support_zones else None
        resistance = max(resistance_zones) if resistance_zones else None

        return support, resistance

    def calculate_indicators(self, df):
        """Расчет индикаторов с использованием TA-Lib и ta."""
        if df is None or df.empty:
            print("Ошибка: Данные для расчета индикаторов отсутствуют или пустые.")
            return None

        # Используем TA-Lib для расчета RSI
        df['rsi'] = talib.RSI(df['close'], timeperiod=14)

        # Используем ta для расчета MACD
        macd_indicator = MACD(df['close'], window_slow=26, window_fast=12, window_sign=9)
        df['macd'] = macd_indicator.macd()
        df['macd_signal'] = macd_indicator.macd_signal()

        return df

    def calculate_potential_profit(self, entry_price, target_price, side, commission_rate=None):
        """Рассчитывает потенциальную прибыль с учетом комиссии."""
        # Получаем комиссии, если они не были переданы
        if commission_rate is None:
            commission_rate = get_trading_fees()  # Получение актуальной комиссии
            if commission_rate is None:
                # Если комиссия не была получена, установить значение по умолчанию
                commission_rate = 0.0004  # По умолчанию используем значение тейкера из .env

        # Рассчитать разницу между ценой входа и целью
        if side == 'buy':
            price_diff = target_price - entry_price
        else:
            price_diff = entry_price - target_price

        # Рассчитать прибыль без учета комиссии
        potential_profit_percent = (price_diff / entry_price) * 100

        # Рассчитать комиссии только один раз, так как комиссия берется на вход
        commission_cost = commission_rate * 100

        # Вычислить итоговую потенциальную прибыль с учетом комиссии
        final_potential_profit = potential_profit_percent - commission_cost

        return final_potential_profit

    def place_order(self, symbol, side, entry_amount_usdt, leverage, stop_loss_percent, take_profit_percent):
        """Размещение ордера с учетом поддержки и сопротивления на основе зон плотности свечей."""
        if self.active_trade:
            print("Активная сделка уже открыта. Новая сделка не будет размещена.")
            return None

        try:
            # Установка кредитного плеча
            market = self.exchange.market(symbol)
            self.exchange.set_leverage(leverage, market['id'])

            # Получение текущей цены для расчета объема сделки
            current_price = fetch_current_price(symbol)

            entry_amount_usdt = max(entry_amount_usdt, 110)
            amount = entry_amount_usdt / current_price
            print(f"Рассчитанный объем сделки: {amount}")

            min_amount = 0.001
            if entry_amount_usdt * leverage < 100 or amount < min_amount:
                print(
                    "Даже после увеличения сумма или объем не соответствуют минимальным требованиям. Ордер не будет размещен.")
                return None

            # Проверка минимального объема сделки для биржи
            market_info = self.exchange.market(symbol)
            if amount < market_info['limits']['amount']['min']:
                print(f"Ошибка: Рассчитанный объем сделки {amount} меньше минимально допустимого {market_info['limits']['amount']['min']} для {symbol}.")
                return None

            # Логирование перед размещением ордера
            print(f"Параметры ордера: Сторона - {side}, Объем - {amount}, Текущая цена - {current_price}")

            # Размещение рыночного ордера
            order = self.exchange.create_market_order(symbol, side, amount)
            print(f"Ордер на {side} размещен: {order}")
            self.active_trade = True

            # Установка стоп-лосса и тейк-профита
            stop_loss_price = current_price * (1 - stop_loss_percent / 100) if side == 'buy' else current_price * (
                    1 + stop_loss_percent / 100)
            take_profit_price = current_price * (1 + take_profit_percent / 100) if side == 'buy' else current_price * (
                    1 - take_profit_percent / 100)

            # Логирование перед установкой стоп-лосса и тейк-профита
            print(f"Установка стоп-лосса на {stop_loss_price} и тейк-профита на {take_profit_price}")

            self.exchange.create_order(symbol, 'STOP_MARKET', 'sell' if side == 'buy' else 'buy', amount, None,
                                       {'stopPrice': stop_loss_price})
            self.exchange.create_order(symbol, 'TAKE_PROFIT_MARKET', 'sell' if side == 'buy' else 'buy', amount, None,
                                       {'stopPrice': take_profit_price})

        except Exception as e:
            print(f"Ошибка при размещении ордера: {e}")
            return None

    def run_bot(self, symbol, entry_percentage, stop_loss_percent, take_profit_percent, leverage, buffer_percent, auto_sl_tp,
                enable_break_even, timeframe, volume_threshold):
        """Основная логика бота с использованием кластерного анализа и технических индикаторов."""
        self.bot_running = True

        entry_amount_usdt = self.calculate_entry_amount(entry_percentage, leverage)

        # Получаем исторические данные и обучаем модели
        df = self.fetch_binance_data(symbol, timeframe, limit=500)
        if df is None or df.empty:
            print("Ошибка: Не удалось получить данные для обучения модели.")
            return
        models, scaler = train_models(df)

        while self.bot_running:
            if self.active_trade:
                open_positions = self.exchange.fetch_positions()
                if not any(pos['contracts'] > 0 for pos in open_positions):
                    self.active_trade = False
                    self.exchange.cancel_all_orders(symbol)
                    print("Активная сделка закрыта, оставшиеся ордера отменены.")
                print("Активная сделка уже открыта, бот ждет закрытия сделки.")
                time.sleep(5)
                continue

            current_volume = fetch_current_volume(symbol)
            if current_volume < volume_threshold:
                print(f"Объем {current_volume:.2f} ниже порога {volume_threshold}. Пропуск сделки.")
                time.sleep(5)
                continue

            # Используем модели для предсказания следующей цены закрытия
            predicted_close_short = predict_next_close(models, df, window_size=10)
            predicted_close_long = predict_next_close(models, df, window_size=60)
            current_price = fetch_current_price(symbol)

            # Проверка потенциальной прибыли для краткосрочной сделки
            potential_profit_short = self.calculate_potential_profit(current_price, predicted_close_short, 'buy')
            if potential_profit_short > 0:
                print(f"Краткосрочное предсказание: цена вырастет с {current_price} до {predicted_close_short}. Открытие сделки на покупку.")
                self.place_order(symbol, 'buy', entry_amount_usdt, leverage, stop_loss_percent, take_profit_percent)
            else:
                print(f"Краткосрочное предсказание: цена упадет с {current_price} до {predicted_close_short}. Пропуск сделки. Потенциальная прибыль: {potential_profit_short:.2f}% (учитывая комиссию).")

            # Проверка потенциальной прибыли для долгосрочной сделки
            potential_profit_long = self.calculate_potential_profit(current_price, predicted_close_long, 'buy')
            if potential_profit_long > 0:
                print(f"Долгосрочное предсказание: цена вырастет с {current_price} до {predicted_close_long}. Открытие сделки на покупку.")
                self.place_order(symbol, 'buy', entry_amount_usdt, leverage, stop_loss_percent, take_profit_percent)
            else:
                print(f"Долгосрочное предсказание: цена упадет с {current_price} до {predicted_close_long}. Пропуск сделки. Потенциальная прибыль: {potential_profit_long:.2f}% (учитывая комиссию).")

            time.sleep(5)

    def stop_bot(self):
        """Останавливает выполнение бота."""
        self.bot_running = False

    def fetch_order_history(self, symbol):
        """Получение истории ордеров для указанного символа."""
        try:
            orders = self.exchange.fetch_orders(symbol)
            return orders
        except Exception as e:
            print(f"Ошибка при получении истории ордеров: {e}")
            return []
