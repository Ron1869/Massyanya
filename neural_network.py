# neural_network.py
# Ron Company #

import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras.optimizers import Adam
from joblib import dump, load

class NeuralNetwork:
    def __init__(self):
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.model = None
        self.kmeans_model = None

    def train_cluster_model(self, df, n_clusters=5):
        """
        Обучает кластерную модель K-Means для поиска паттернов в данных.
        """
        try:
            df_scaled = self.scaler.fit_transform(df[['open', 'high', 'low', 'close', 'volume']])
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            df['cluster'] = kmeans.fit_predict(df_scaled)
            self.kmeans_model = kmeans
            print(f"Кластерная модель K-Means обучена с {n_clusters} кластерами.")
        except Exception as e:
            print(f"Ошибка при обучении кластерной модели: {e}")

    def create_model(self, input_shape):
        """
        Создает и компилирует модель LSTM для предсказания цен.
        """
        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=input_shape))
        model.add(LSTM(50))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mean_squared_error')
        self.model = model

    def train_model(self, df, epochs=10, batch_size=1, window_size=10):
        """
        Обучает модель LSTM на данных.
        """
        try:
            # Создаем окна для обучения
            data = df['close'].values.reshape(-1, 1)
            scaled_data = self.scaler.fit_transform(data)
            x_train, y_train = [], []
            for i in range(window_size, len(scaled_data)):
                x_train.append(scaled_data[i - window_size:i, 0])
                y_train.append(scaled_data[i, 0])

            x_train, y_train = np.array(x_train), np.array(y_train)
            x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

            # Создаем и обучаем модель
            self.create_model(input_shape=(x_train.shape[1], 1))
            self.model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size)
            print(f"Модель LSTM обучена на {epochs} эпохах.")
        except Exception as e:
            print(f"Ошибка при обучении LSTM модели: {e}")

    def predict(self, df, window_size=10):
        """
        Выполняет предсказание цены на основе обученной модели LSTM.
        """
        try:
            if not self.model:
                print("Ошибка: Модель не обучена.")
                return None

            data = df['close'].values.reshape(-1, 1)
            scaled_data = self.scaler.transform(data)
            x_test = []
            for i in range(window_size, len(scaled_data)):
                x_test.append(scaled_data[i - window_size:i, 0])

            x_test = np.array(x_test)
            x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
            predictions = self.model.predict(x_test)
            predictions = self.scaler.inverse_transform(predictions)
            return predictions[-1][0]  # Возвращаем последнее предсказание
        except Exception as e:
            print(f"Ошибка при предсказании с LSTM моделью: {e}")
            return None

    def predict_clusters(self, df):
        """
        Выполняет предсказание на основе кластеров K-Means.
        """
        try:
            if not self.kmeans_model:
                print("Ошибка: Кластерная модель не обучена.")
                return None

            df_scaled = self.scaler.transform(df[['open', 'high', 'low', 'close', 'volume']])
            clusters = self.kmeans_model.predict(df_scaled)
            return clusters[-1]  # Возвращаем кластер для последнего ряда
        except Exception as e:
            print(f"Ошибка при предсказании кластеров: {e}")
            return None

    def evaluate_model(self, df, window_size=10):
        """
        Оценивает обученную модель LSTM на тестовых данных и выводит среднеквадратичную ошибку.
        """
        try:
            data = df['close'].values.reshape(-1, 1)
            scaled_data = self.scaler.transform(data)
            x_test, y_test = [], []
            for i in range(window_size, len(scaled_data)):
                x_test.append(scaled_data[i - window_size:i, 0])
                y_test.append(scaled_data[i, 0])

            x_test, y_test = np.array(x_test), np.array(y_test)
            x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

            predictions = self.model.predict(x_test)
            predictions = self.scaler.inverse_transform(predictions.reshape(-1, 1))
            y_test = self.scaler.inverse_transform(y_test.reshape(-1, 1))
            mse = mean_squared_error(y_test, predictions)
            print(f"Среднеквадратичная ошибка на тестовых данных: {mse}")
        except Exception as e:
            print(f"Ошибка при оценке модели: {e}")

# Обертки для совместимости с trading_logic

def train_models(df, window_size=10, epochs=10, batch_size=32):
    nn = NeuralNetwork()
    nn.train_model(df, epochs=epochs, batch_size=batch_size, window_size=window_size)
    return nn, nn.scaler

def predict_next_close(nn, df, window_size=10):
    return nn.predict(df, window_size)

