# interface_manager.py
# Ron Company #

import tkinter as tk
from tkinter import ttk
import threading
from update_manager import UpdateManager

class InterfaceManager:
    def __init__(self, window, bot):
        self.window = window
        self.bot = bot
        self.bot_running = False
        self.bot_thread = None
        self.initialize_interface()

    def initialize_interface(self):
        """
        Инициализирует основной интерфейс приложения, включая поля для отображения данных и элементы управления.
        """
        # Поля для ввода и кнопки
        tk.Label(self.window, text="Сумма входа (% от баланса):", bg="#000000", fg="white", font=("Helvetica", 11)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.amount_percentage_entry = ttk.Entry(self.window)
        self.amount_percentage_entry.insert(0, "500")
        self.amount_percentage_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.window, text="Плечо:", bg="#000000", fg="white", font=("Helvetica", 11)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.leverage_entry = ttk.Entry(self.window)
        self.leverage_entry.insert(0, "20")
        self.leverage_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.window, text="Стоп-лосс (%):", bg="#000000", fg="white", font=("Helvetica", 11)).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.sl_entry = ttk.Entry(self.window)
        self.sl_entry.insert(0, "1")
        self.sl_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.window, text="Тейк-профит (%):", bg="#000000", fg="white", font=("Helvetica", 11)).grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.tp_entry = ttk.Entry(self.window)
        self.tp_entry.insert(0, "2")
        self.tp_entry.grid(row=3, column=1, padx=10, pady=10)

        # Поле для ввода буфера безубыточности
        tk.Label(self.window, text="Буфер безубыточности (%):", bg="#000000", fg="white", font=("Helvetica", 11)).grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.buffer_entry = ttk.Entry(self.window)
        self.buffer_entry.insert(0, "0.50")
        self.buffer_entry.grid(row=4, column=1, padx=10, pady=10)
        self.buffer_entry.configure(state='disabled')

        # Поле для выбора таймфрейма
        tk.Label(self.window, text="Таймфрейм:", bg="#000000", fg="white", font=("Helvetica", 11)).grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.timeframe_combobox = ttk.Combobox(self.window, values=["1m", "5m", "15m", "1h", "4h", "1d"])
        self.timeframe_combobox.set("15m")
        self.timeframe_combobox.grid(row=5, column=1, padx=10, pady=10)

        # Поле для настройки порога объема
        tk.Label(self.window, text="Порог Объема:", bg="#000000", fg="white", font=("Helvetica", 11)).grid(row=6, column=0, padx=10, pady=10, sticky="w")
        self.volume_threshold_entry = ttk.Entry(self.window)
        self.volume_threshold_entry.insert(0, "200")
        self.volume_threshold_entry.grid(row=6, column=1, padx=10, pady=10)

        # Отображение текущего объема
        self.current_volume_label = tk.Label(self.window, text="Текущий объем: Загрузка...", bg="#000000", fg="white", font=("Helvetica", 11))
        self.current_volume_label.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # Галочка для включения безубыточности
        self.enable_break_even = tk.BooleanVar()
        self.break_even_checkbox = tk.Checkbutton(
            self.window, text="Включить безубыточность", variable=self.enable_break_even,
            command=self.toggle_break_even, bg="#000000", fg="white", font=("Helvetica", 11), selectcolor="black"
        )
        self.break_even_checkbox.grid(row=8, columnspan=2, padx=10, pady=10)

        # Переключатель для автоматического Stop Loss / Take Profit
        self.auto_sl_tp_var = tk.BooleanVar()
        self.auto_sl_tp_checkbox = tk.Checkbutton(
            self.window, text="Авто Stop Loss/Take Profit", variable=self.auto_sl_tp_var,
            command=self.toggle_auto_sl_tp, bg="#000000", fg="white", font=("Helvetica", 11), selectcolor="black"
        )
        self.auto_sl_tp_checkbox.grid(row=9, columnspan=2, padx=10, pady=10)

        # Кнопка для запуска/остановки бота
        self.bot_button = tk.Button(
            self.window, text="Запустить Масяню", command=self.toggle_bot,
            bg="green", fg="white", font=("Helvetica", 11)
        )
        self.bot_button.grid(row=10, column=0, padx=10, pady=10, sticky="ew")

        # Кнопка для закрытия всех позиций
        self.stop_button = tk.Button(
            self.window, text="Закрыть Все Позиции", command=lambda: self.bot.stop_bot(),
            bg="red", fg="white", font=("Helvetica", 11)
        )
        self.stop_button.grid(row=10, column=1, padx=10, pady=10, sticky="ew")

        # Кнопка для открытия графика
        self.open_chart_button = tk.Button(
            self.window, text="Открыть график", command=self.open_chart,
            bg="blue", fg="white", font=("Helvetica", 11)
        )
        self.open_chart_button.grid(row=11, column=0, padx=10, pady=10, sticky="ew")

        # Кнопка для открытия истории ордеров
        self.order_history_button = tk.Button(
            self.window, text="История ордеров", command=self.open_order_history,
            bg="orange", fg="white", font=("Helvetica", 11)
        )
        self.order_history_button.grid(row=11, column=1, padx=10, pady=10, sticky="ew")

        # Отображение баланса
        self.balance_label = tk.Label(self.window, text="Баланс (USDT): Загрузка...", bg="#000000", fg="white", font=("Helvetica", 11))
        self.balance_label.grid(row=12, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # Отображение текущей цены BTC/USDT
        self.current_price_label = tk.Label(self.window, text="Текущая цена BTC/USDT: Загрузка...", bg="#000000", fg="white", font=("Helvetica", 11))
        self.current_price_label.grid(row=13, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # Отображение статистики сделок
        self.total_trades_label = tk.Label(self.window, text="Всего сделок: 0", bg="#000000", fg="white", font=("Helvetica", 11))
        self.total_trades_label.grid(row=14, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # Создание экземпляра UpdateManager для обновления данных
        self.update_manager = UpdateManager(self.window, self.balance_label, self.current_price_label, self.current_volume_label, self.bot)
        self.update_manager.start_updates()

    def toggle_break_even(self):
        if self.enable_break_even.get():
            self.buffer_entry.configure(state='normal')
        else:
            self.buffer_entry.configure(state='disabled')

    def toggle_auto_sl_tp(self):
        if self.auto_sl_tp_var.get():
            self.sl_entry.configure(state='disabled')
            self.tp_entry.configure(state='disabled')
        else:
            self.sl_entry.configure(state='normal')
            self.tp_entry.configure(state='normal')

    def toggle_bot(self):
        self.bot_running = not self.bot_running
        if self.bot_running:
            selected_timeframe = self.timeframe_combobox.get()
            entry_percentage = float(self.amount_percentage_entry.get())
            leverage = int(self.leverage_entry.get())
            volume_threshold = float(self.volume_threshold_entry.get())

            # Убедитесь, что `run_bot` получает нужное количество аргументов
            self.bot_thread = threading.Thread(target=self.bot.run_bot, args=(
                'BTC/USDT',
                entry_percentage,
                float(self.sl_entry.get()) / 100,
                float(self.tp_entry.get()) / 100,
                leverage,
                float(self.buffer_entry.get()) / 100,
                self.auto_sl_tp_var.get(),
                self.enable_break_even.get(),
                selected_timeframe,
                volume_threshold
            ), daemon=True)
            self.bot_thread.start()
            self.bot_button.config(text="Остановить Масяню", bg="red")
        else:
            self.bot.stop_bot()
            self.bot_button.config(text="Запустить Масяню", bg="green")

    def open_chart(self):
        try:
            import webview
            webview.create_window("График торговли", "https://www.binance.com/ru/futures/BTCUSDT")
            webview.start()
        except Exception as e:
            print(f"Ошибка при открытии графика: {e}")

    def open_order_history(self):
        order_history_window = tk.Toplevel(self.window)
        order_history_window.title("История ордеров")
        order_history_window.geometry("600x400")
        order_history_window.configure(bg="#000000")

        order_history_tree = ttk.Treeview(order_history_window, columns=('ID', 'Side', 'Price', 'Status', 'Date'), show='headings', height=15)
        order_history_tree.heading('ID', text='ID')
        order_history_tree.heading('Side', text='Side')
        order_history_tree.heading('Price', text='Price')
        order_history_tree.heading('Status', text='Status')
        order_history_tree.heading('Date', text='Date')
        order_history_tree.grid(row=0, column=0, padx=10, pady=10)

        orders = self.bot.fetch_order_history('BTC/USDT')
        for order in orders:
            order_history_tree.insert('', 'end', values=(order['id'], order['side'], order['price'], order['status'], order['datetime']))

    def start_interface(self):
        self.window.mainloop()
