# Massyanya
# Massyanya: Automated Cryptocurrency Trading Bot

**Massyanya** is an automated cryptocurrency trading bot designed for trading on the Binance exchange. The bot utilizes machine learning models and various trading strategies to identify profitable trading opportunities in the highly volatile cryptocurrency market. Massyanya aims to make informed trading decisions by analyzing historical data, calculating technical indicators, and predicting future price movements.

## Overview
Massyanya is built using Python and leverages several key technologies and libraries, including **TensorFlow** for neural networks, **scikit-learn** for clustering, **TA-Lib** for technical analysis, and **ccxt** for exchange interaction. The trading logic is powered by both traditional trading strategies and modern machine learning models to make accurate predictions and execute trades autonomously.

## Components
Massyanya consists of multiple components that work in conjunction to achieve seamless trading. Here are the main components:

### 1. Neural Network (`neural_network.py`)
- The bot utilizes **Long Short-Term Memory (LSTM)** neural networks for price prediction.
- It also incorporates a **K-Means clustering model** to identify different price patterns and clusters in historical data.
- The LSTM model is used to predict future prices based on historical price movements, while the K-Means model helps identify potential clusters that may indicate support or resistance levels.
- **LSTM Model Structure**: The LSTM model has two layers with 50 units each, followed by a dense output layer for the price prediction.
- The data is scaled using `MinMaxScaler` to bring all values between 0 and 1 for better training performance.
- The model is trained using the **Adam optimizer** to minimize mean squared error, ensuring efficient and stable training.

### 2. Trading Logic (`trading_logic.py`)
- The core trading logic is implemented here. The bot collects market data (using **ccxt** to interact with Binance) and calculates key trading indicators like **MACD** and **RSI** using **TA-Lib** and the **ta** library.
- **MACD and RSI Indicators**: The bot uses these indicators to determine overbought and oversold conditions in the market, helping it to make buy or sell decisions.
- The bot determines entry amounts, calculates potential profits, and manages open positions.
- It also handles risk management by setting stop-loss and take-profit levels based on market analysis.

### 3. Update Manager (`update_manager.py`)
- This module updates the user interface (Tkinter-based) with real-time information, such as the current balance, BTC/USDT price, and trading volume.
- It ensures that the user is always informed about the current state of the market and the trading bot's performance.

### 4. Interface Manager (`interface_manager.py`)
- The user interface is developed using **Tkinter**.
- It allows the user to configure important parameters like leverage, entry percentage, stop-loss percentage, and more.
- The interface includes buttons to start or stop the bot, view trade history, and monitor account balance and live trading metrics.

### 5. Data Fetcher (`data_fetcher.py`) and Data Manager (`data_manager.py`)
- The **Data Fetcher** module is responsible for retrieving real-time data such as the current balance, price, and volume from the Binance exchange via **ccxt**.
- The **Data Manager** is used to manage historical data and interact with the exchange, ensuring that the bot has all the required information to make informed decisions.

### 6. Exchange Manager (`exchange_manager.py`)
- The Exchange Manager handles interaction with the Binance exchange.
- It uses **ccxt** to place orders, set leverage, manage positions, and cancel all orders when necessary.
- The Exchange Manager is also responsible for setting isolated margin modes and updating trading fees dynamically.

### 7. Cache Handler (`cache_handler.py`)
- The bot uses caching to store certain data temporarily and enhance performance by reducing the frequency of API calls.
- The **Cache Manager** allows the retrieval of cached data if it is within the allowed duration, which helps to lower the load on Binance servers and minimize the risk of hitting rate limits.

### 8. `.env` Configuration (`.env`)
- Contains sensitive information like **Binance API keys** (API Key and Secret) and trading fees (taker and maker fees).
- The bot loads these values to interact securely with the Binance exchange.

### 9. Main Application (`main.py`)
- The entry point of the trading bot.
- Loads configuration, initializes the trading bot, sets up the user interface, and launches the entire system.
- Ensures all components are properly set up before starting to trade.

## Key Features
- **LSTM-Based Prediction**: Uses an LSTM neural network to predict future prices, allowing for more data-driven decision-making.
- **Cluster Analysis**: The K-Means model identifies recurring price patterns that help determine potential market conditions like support or resistance levels.
- **Technical Analysis**: Integrates commonly used indicators like **MACD** and **RSI** to enhance the reliability of trade decisions.
- **Leverage and Risk Management**: Supports adjustable leverage settings and dynamic risk management with stop-loss and take-profit settings.
- **User Interface**: Offers a user-friendly interface using **Tkinter**, allowing easy control and monitoring of the bot's activities.
- **Modular Design**: Each component is built to handle specific tasks, making it easier to maintain and update.

## Libraries and Tools Used
- **TensorFlow** for LSTM implementation.
- **scikit-learn** for K-Means clustering.
- **TA-Lib** and **ta** for technical indicators.
- **ccxt** for interaction with Binance exchange.
- **Tkinter** for the graphical user interface.
- **dotenv** for secure loading of sensitive API keys.

## Getting Started
To get started with Massyanya:
1. Clone this repository.
2. Install the required Python packages listed in `requirements.txt`.
3. Add your Binance API keys to the `.env` file.
4. Run `main.py` to start the application.

```bash
python main.py
```

Ensure that you have sufficient balance on your Binance account before starting the bot. Additionally, adjust the bot settings in the interface to suit your risk appetite.

## Disclaimer
This trading bot is for educational purposes only. Cryptocurrency trading is risky, and there is no guarantee of profit. Use this bot at your own risk.

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.


