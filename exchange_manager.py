# exchange_manager.py
# Ron Company #

import os
import ccxt
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

class ExchangeManager:
    def __init__(self):
        self.exchange = None
        self.is_initialized = False  # Флаг для отслеживания успешной инициализации
        self.taker_commission = float(os.getenv('TAKER_COMMISSION', 0.0004))
        self.maker_commission = float(os.getenv('MAKER_COMMISSION', 0.0002))

    def setup_exchange(self, api_key, api_secret):
        """Настройка подключения к бирже Binance с указанными API-ключами."""
        if self.exchange is None and not self.is_initialized:
            if not api_key or not api_secret:
                print("Ошибка: ключи API отсутствуют. Проверьте файл .env.")
                return None

            self.exchange = ccxt.binance({
                'apiKey': api_key,
                'secret': api_secret,
                'options': {'defaultType': 'future'},
                'enableRateLimit': True
            })

            try:
                self.exchange.load_time_difference()
                self.is_initialized = True  # Успешная инициализация
                # Убрал вывод синхронизации времени
            except Exception as e:
                print(f"Ошибка при синхронизации времени с Binance: {e}")

        return self.exchange

    def get_exchange(self):
        """Возвращает объект биржи, если он инициализирован, иначе пытается инициализировать."""
        if self.exchange is None and not self.is_initialized:
            print("Ошибка: Биржа не инициализирована. Сначала вызовите setup_exchange().")
        return self.exchange

    def set_leverage_and_margin(self, symbol, leverage):
        """Устанавливает кредитное плечо и изолированную маржу для символа."""
        if self.exchange:
            try:
                market = self.exchange.market(symbol)
                self.exchange.set_margin_mode('ISOLATED', market['symbol'])
                self.exchange.set_leverage(leverage, market['symbol'])
                # Убрал вывод установки плеча
            except Exception as e:
                print(f"Ошибка при установке плеча и маржи: {e}")

    def cancel_all_orders(self, symbol):
        """Отмена всех открытых ордеров для символа."""
        if self.exchange:
            try:
                orders = self.exchange.fetch_open_orders(symbol)
                for order in orders:
                    self.exchange.cancel_order(order['id'], symbol)
                    # Убрал вывод об отмене ордера
            except Exception as e:
                print(f"Ошибка при отмене ордеров: {e}")

    def get_trading_fees(self):
        """Получает текущие комиссии на торговлю с биржи."""
        if self.exchange:
            try:
                markets = self.exchange.load_markets()
                # Здесь берутся комиссии с рынка BTC/USDT в качестве примера
                if 'BTC/USDT' in markets:
                    market = markets['BTC/USDT']
                    maker_fee = market['maker']
                    taker_fee = market['taker']
                    self.maker_commission = maker_fee
                    self.taker_commission = taker_fee
                    return max(maker_fee, taker_fee)
                else:
                    print("Ошибка: Не удалось найти рынок BTC/USDT для получения комиссий.")
            except Exception as e:
                print(f"Ошибка при получении комиссий: {e}")
        return None

# Создаем глобальный экземпляр менеджера биржи
exchange_manager = ExchangeManager()

# Обертка для методов экземпляра exchange_manager
def setup_exchange(api_key, api_secret):
    exchange_manager.setup_exchange(api_key, api_secret)

def get_exchange():
    return exchange_manager.get_exchange()

def set_leverage_and_margin(symbol, leverage):
    exchange_manager.set_leverage_and_margin(symbol, leverage)

def cancel_all_orders(symbol):
    exchange_manager.cancel_all_orders(symbol)

def get_trading_fees():
    return exchange_manager.get_trading_fees()
