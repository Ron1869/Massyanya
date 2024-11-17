# update_manager.py
# Ron Company #

import time
import tkinter as tk
from data_fetcher import DataFetcher

class UpdateManager:
    def __init__(self, window, balance_label, current_price_label, current_volume_label, bot, interval=5000):
        self.window = window
        self.balance_label = balance_label
        self.current_price_label = current_price_label
        self.current_volume_label = current_volume_label
        self.bot = bot
        self.interval = interval
        self.data_fetcher = DataFetcher()

    def update_balance(self):
        """
        Обновляет отображение баланса пользователя в интерфейсе.
        """
        try:
            balance = self.data_fetcher.fetch_balance()
            if balance is not None:
                self.balance_label.config(text=f"Баланс (USDT): {balance:.2f}")
            else:
                self.balance_label.config(text="Ошибка: Не удалось получить баланс.")
        except Exception as e:
            self.balance_label.config(text=f"Ошибка при получении баланса: {e}")
        self.window.after(self.interval, self.update_balance)

    def update_current_price(self):
        """
        Обновляет отображение текущей цены BTC/USDT в интерфейсе.
        """
        try:
            current_price = self.data_fetcher.fetch_current_price("BTC/USDT")
            if current_price is not None:
                self.current_price_label.config(text=f"Текущая цена BTC/USDT: {current_price:.2f}")
            else:
                self.current_price_label.config(text="Ошибка: Не удалось получить текущую цену.")
        except Exception as e:
            self.current_price_label.config(text=f"Ошибка при получении цены: {e}")
        self.window.after(self.interval, self.update_current_price)

    def update_volume(self):
        """
        Обновляет отображение текущего объема торгов в интерфейсе.
        """
        try:
            current_volume = self.data_fetcher.fetch_current_volume("BTC/USDT")
            if current_volume is not None:
                self.current_volume_label.config(text=f"Текущий объем: {current_volume:.2f}")
            else:
                self.current_volume_label.config(text="Ошибка: Не удалось получить текущий объем.")
        except Exception as e:
            self.current_volume_label.config(text=f"Ошибка при обновлении объема: {e}")
        self.window.after(self.interval, self.update_volume)

    def start_updates(self):
        """
        Запускает циклическое обновление данных в интерфейсе.
        """
        self.update_balance()
        self.update_current_price()
        self.update_volume()
