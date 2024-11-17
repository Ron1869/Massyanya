# main.py
# Ron Company #

import os
from dotenv import load_dotenv
import tkinter as tk
from exchange_manager import setup_exchange
import trading_logic
from interface_manager import InterfaceManager


# Загрузка переменных из файла .env
load_dotenv()

# Инициализация и настройка биржи
api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')

if not api_key or not api_secret:
    print("Ошибка: ключи API не были загружены. Проверьте файл .env")
    exit(1)

setup_exchange(api_key, api_secret)

# Создание экземпляра торгового бота
bot = trading_logic.TradingBot()

# Создание окна интерфейса и запуск InterfaceManager
window = tk.Tk()
window.title("Торговый бот Масяня")
window.geometry("410x660")
window.configure(bg="#000000")

interface_manager = InterfaceManager(window, bot)
interface_manager.start_interface()
