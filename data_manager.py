# data_manager.py
# Ron Company #

import os  # Необходимый импорт для работы с переменными окружения
from exchange_manager import ExchangeManager
import pandas as pd
import time

# Инициализация экземпляра ExchangeManager
data_manager_instance = ExchangeManager()

def ensure_exchange_initialized():
    """
    Убедитесь, что биржа инициализирована. Если нет - попробуйте инициализировать.
    """
    if not data_manager_instance.is_initialized:
        api_key = os.getenv('BINANCE_API_KEY')
        api_secret = os.getenv('BINANCE_API_SECRET')
        if api_key and api_secret:
            print("Инициализация биржи с предоставленными API ключами...")
            data_manager_instance.setup_exchange(api_key, api_secret)
        else:
            print("Ошибка: API ключи отсутствуют. Проверьте файл .env.")
        if data_manager_instance.is_initialized:
            print("Биржа успешно инициализирована.")
        else:
            print("Ошибка: Не удалось инициализировать биржу. Проверьте ключи API.")

def fetch_balance():
    """Получение текущего баланса аккаунта."""
    ensure_exchange_initialized()
    exchange = data_manager_instance.get_exchange()
    if not exchange:
        print("Ошибка: Биржа не инициализирована.")
        return 0
    try:
        print("Получение баланса с биржи...")
        balance_info = exchange.fetch_balance()
        print(f"Информация о балансе: {balance_info}")
        balance = balance_info['total'].get('USDT', 0)
        return balance
    except Exception as e:
        print(f"Ошибка при получении баланса: {e}")
        return 0

def fetch_current_price(symbol):
    """Получение текущей цены для указанного символа."""
    ensure_exchange_initialized()
    exchange = data_manager_instance.get_exchange()
    if not exchange:
        print("Ошибка: Биржа не инициализирована.")
        return None
    try:
        ticker = exchange.fetch_ticker(symbol)
        current_price = ticker.get('last')
        return current_price
    except Exception as e:
        print(f"Ошибка при получении текущей цены для {symbol}: {e}")
        return None

def fetch_current_volume(symbol):
    """Получение текущего объема для указанного символа."""
    ensure_exchange_initialized()
    exchange = data_manager_instance.get_exchange()
    if not exchange:
        print("Ошибка: Биржа не инициализирована.")
        return None
    try:
        ticker = exchange.fetch_ticker(symbol)
        current_volume = ticker.get('quoteVolume')
        return current_volume
    except Exception as e:
        print(f"Ошибка при получении текущего объема для {symbol}: {e}")
        return None

def fetch_historical_data(symbol, timeframe='1d', limit=100):
    """Получение исторических данных для указанного символа и таймфрейма."""
    ensure_exchange_initialized()
    exchange = data_manager_instance.get_exchange()
    if not exchange:
        print("Ошибка: Биржа не инициализирована.")
        return pd.DataFrame()
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        print(f"Исторические данные для {symbol} успешно получены.")
        return df
    except Exception as e:
        print(f"Ошибка при получении исторических данных для {symbol}: {e}")
        return pd.DataFrame()

def calculate_take_profit_and_stop_loss(entry_price, min_distance=800):
    """
    Рассчитать уровни тейк-профита и стоп-лосса с минимальным расстоянием.
    """
    take_profit = entry_price + min_distance
    stop_loss = entry_price - min_distance
    return take_profit, stop_loss

def wait_for_next_candle(interval_seconds):
    """Функция ожидания следующей свечи, чтобы минимизировать дублирование данных."""
    current_time = time.time()
    next_candle_time = (current_time // interval_seconds + 1) * interval_seconds
    wait_seconds = next_candle_time - current_time
    print(f"Ожидание {wait_seconds:.2f} секунд до следующей свечи.")
    time.sleep(wait_seconds)
    print("Начало нового интервала.")
