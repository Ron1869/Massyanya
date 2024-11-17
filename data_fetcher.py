# data_fetcher.py
# Ron Company #

from exchange_manager import exchange_manager
from cache_handler import cache_manager
import pandas as pd

class DataFetcher:
    def __init__(self):
        self.exchange = exchange_manager.get_exchange()

    def fetch_balance(self):
        """Получение текущего баланса аккаунта с использованием кэша."""
        cache_key = "balance"
        cached_balance = cache_manager.get_cache(cache_key, cache_duration=60)  # Кэш на 60 секунд
        if cached_balance is not None:
            return cached_balance

        try:
            balance_info = self.exchange.fetch_balance()
            balance = balance_info['total']['USDT']
            cache_manager.set_cache(cache_key, balance)
            return balance
        except Exception as e:
            print(f"Ошибка при получении баланса: {e}")
            return 0

    def fetch_current_price(self, symbol):
        """Получение текущей цены для указанного символа с использованием кэша."""
        cache_key = f"current_price_{symbol}"
        cached_price = cache_manager.get_cache(cache_key, cache_duration=30)  # Кэш на 30 секунд
        if cached_price is not None:
            return cached_price

        try:
            ticker = self.exchange.fetch_ticker(symbol)
            current_price = ticker['last']
            cache_manager.set_cache(cache_key, current_price)
            return current_price
        except Exception as e:
            print(f"Ошибка при получении текущей цены для {symbol}: {e}")
            return None

    def fetch_current_volume(self, symbol):
        """Получение текущего объема для указанного символа с использованием кэша."""
        cache_key = f"current_volume_{symbol}"
        cached_volume = cache_manager.get_cache(cache_key, cache_duration=30)  # Кэш на 30 секунд
        if cached_volume is not None:
            return cached_volume

        try:
            ticker = self.exchange.fetch_ticker(symbol)
            current_volume = ticker['quoteVolume']
            cache_manager.set_cache(cache_key, current_volume)
            return current_volume
        except Exception as e:
            print(f"Ошибка при получении текущего объема для {symbol}: {e}")
            return None

# Создаем глобальный экземпляр DataFetcher
data_fetcher = DataFetcher()
