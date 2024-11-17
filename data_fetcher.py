# data_fetcher.py
# Ron Company #

from exchange_manager import exchange_manager
import pandas as pd

class DataFetcher:
    def __init__(self):
        self.exchange = exchange_manager.get_exchange()

    def fetch_balance(self):
        """Получение текущего баланса аккаунта."""
        try:
            balance_info = self.exchange.fetch_balance()
            balance = balance_info['total']['USDT']

            return balance
        except Exception as e:
            print(f"Ошибка при получении баланса: {e}")
            return 0

    def fetch_current_price(self, symbol):
        """Получение текущей цены для указанного символа."""
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            current_price = ticker['last']

            return current_price
        except Exception as e:
            print(f"Ошибка при получении текущей цены для {symbol}: {e}")
            return None

    def fetch_current_volume(self, symbol):
        """Получение текущего объема для указанного символа."""
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            current_volume = ticker['quoteVolume']

            return current_volume
        except Exception as e:
            print(f"Ошибка при получении текущего объема для {symbol}: {e}")
            return None

# Создаем глобальный экземпляр DataFetcher
data_fetcher = DataFetcher()






# print(f"Текущий баланс: {balance} USDT")
# print(f"Текущая цена для {symbol}: {current_price}")
# print(f"Текущий объем для {symbol}: {current_volume}")# убрал чтобы не мешали
