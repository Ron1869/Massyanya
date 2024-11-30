# Massyanya
Общее описание проекта 'Massyanya':
![photo_2024-11-17_12-02-10](https://github.com/user-attachments/assets/fde4b00a-c101-4b3c-b424-5155b09ca7c0)

Проект 'Massyanya' представляет собой торгового бота для криптовалют, использующего данные биржи Binance для анализа и прогнозирования цен. Бот сочетает в себе машинное обучение (LSTM и K-Means) и классические методы технического анализа для принятия торговых решений. Основная цель проекта — автоматизация процесса торговли криптовалютами на основе предсказаний цены и анализа данных.

Основные файлы и их описание:

Main.pyЭтот файл служит входной точкой приложения. Он запускает пользовательский интерфейс и связывает все компоненты проекта. Основные функции включают настройку начальных параметров, запуск графического интерфейса и координацию взаимодействия между компонентами бота.

neural_network.pyЭтот файл содержит реализацию моделей машинного обучения, используемых для предсказания цен криптовалют. Основные используемые модели включают:

LSTM (Long Short-Term Memory): LSTM нейронная сеть используется для анализа временных рядов данных. Она обучается на исторических данных цен и предсказывает будущие значения.

K-Means: Используется для кластеризации данных. Модель разбивает ценовые данные на кластеры для выделения закономерностей и аномалий.

Функции:

train_lstm_model(data): обучает LSTM на предоставленных данных, используя историю цен.

predict_price(data): на основе обученной модели предсказывает будущие значения цен.

trading_logic.pyФайл реализует торговую логику бота. В нем содержатся функции для получения данных с биржи, расчета индикаторов и размещения торговых ордеров.

calculate_indicators(data): рассчитывает различные технические индикаторы, такие как скользящие средние (MA), индекс относительной силы (RSI), и использует их для принятия решений.

execute_trade(decision): функция для открытия или закрытия ордеров в зависимости от решения, принятого моделью.

update_manager.pyЭтот модуль обновляет данные в пользовательском интерфейсе, такие как баланс, текущие цены и объемы торгов.

update_balance(): обновляет баланс пользователя в реальном времени.

update_price(): получает текущую цену и отображает ее в интерфейсе.

data_fetcher.pyМодуль отвечает за получение данных с биржи Binance, включая баланс, цены и объемы.

fetch_price_data(symbol): получает исторические и текущие данные по определенной криптовалюте.

fetch_balance(): возвращает текущий баланс пользователя.

data_manager.pyЭтот файл управляет данными и взаимодействует с биржей. Содержит функции для обработки и сохранения данных.

process_data(data): предварительная обработка данных перед передачей в модель.

save_data(data): сохраняет обработанные данные для последующего анализа.

exchange_manager.pyМодуль отвечает за управление взаимодействием с Binance API, включая установку плеча и отмену ордеров.

set_leverage(symbol, leverage): устанавливает уровень плеча для торговли.

cancel_order(order_id): отменяет указанный ордер.

interface_manager.pyУправляет графическим интерфейсом пользователя (GUI), реализованным с использованием Tkinter. Обеспечивает взаимодействие пользователя с ботом через визуальный интерфейс.

create_main_window(): создает главное окно приложения с необходимыми виджетами.

update_interface(data): обновляет данные в интерфейсе в реальном времени.

cache_handler.pyУправляет кэшированием данных, что помогает улучшить производительность системы. Используется для временного хранения данных, чтобы минимизировать количество запросов к бирже.

cache_data(data): сохраняет данные в кэш.

retrieve_cached_data(): возвращает данные из кэша, если они актуальны.

.envЭтот файл содержит конфигурационные данные, включая API-ключи Binance и комиссии. Он расположен в папке C:\Project_Massyanya_New\config. Данные из .env файла используются для подключения к API и настройки параметров торговли.

Процесс предсказания и торговли:

Сбор данных: Сначала 'data_fetcher.py' получает исторические данные по криптовалютам и текущий баланс с помощью Binance API.

Обработка данных: Данные предварительно обрабатываются в 'data_manager.py', где они нормализуются и готовятся к анализу. Также производится кэширование для повышения производительности.

Обучение и предсказание: 'neural_network.py' использует LSTM модель для предсказания будущих значений цены на основе исторических данных. K-Means помогает разбить данные на кластеры, чтобы определить наиболее выгодные точки входа и выхода.

Анализ и принятие решений: 'trading_logic.py' рассчитывает технические индикаторы (RSI, MA и др.) и совместно с результатами предсказания от модели принимает торговые решения.

Размещение ордеров: В зависимости от решения, функция 'execute_trade()' размещает соответствующие ордера через 'exchange_manager.py'.

Обновление интерфейса: 'update_manager.py' и 'interface_manager.py' обновляют информацию для пользователя в реальном времени, показывая баланс, открытые позиции и другие данные.

Проект 'Massyanya' объединяет различные аспекты анализа данных и автоматизации торговли, предоставляя пользователю удобный инструмент для работы с криптовалютами.
