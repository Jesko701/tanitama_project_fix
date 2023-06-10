import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from flask import jsonify
import functools
import os


class TimeSeries():
    # 1 time load all model
    model_folder = "ML/static"
    model_filename_1 = "1.h5"
    model_filename_2 = "2.h5"
    model_filename_3 = "3.h5"
    model_filename_4 = "4.h5"
    model_filename_5 = "multiForecast.h5"
    model_path_1 = os.path.join(model_folder, model_filename_1)
    model_path_2 = os.path.join(model_folder, model_filename_2)
    model_path_3 = os.path.join(model_folder, model_filename_3)
    model_path_4 = os.path.join(model_folder, model_filename_4)
    model_path_5 = os.path.join(model_folder, model_filename_5)
    model_1 = tf.keras.models.load_model(model_path_1)
    model_2 = tf.keras.models.load_model(model_path_2)
    model_3 = tf.keras.models.load_model(model_path_3)
    model_4 = tf.keras.models.load_model(model_path_4)
    model_5 = tf.keras.models.load_model(model_path_5)

    # Load data CSV
    data_folder = "ML/data"
    data_name = "DataBaru_HargaPangan.csv"
    data_multiforecast = "Dataset Pangan Maret 2017 - May 2023.csv"
    df = pd.read_csv(os.path.join(data_folder, data_name))
    df_multiforecast = pd.read_csv(os.path.join(data_folder,data_multiforecast))

    def __init__(self):
        self.dataBeras = self.predictBeras()
        self.dataCabaiMerah = self.predictCabaiMerah()
        self.dataBawangMerah = self.predictBawangMerah()
        self.dataBawangPutih = self.predictBawangPutih()

    @functools.lru_cache(maxsize=128)
    def predict(self):
        return jsonify(message="Berhasil mengambil data", data={"Beras": self.dataBeras, "Cabai Merah": self.dataCabaiMerah, "Bawang Merah": self.dataBawangMerah, "Bawang Putih": self.dataBawangPutih}), 200

    @functools.lru_cache(maxsize=128)
    def predictBeras(self):
        # Filter Data as 'Beras' only
        data_filter = self.df.filter(['Beras'])
        data = data_filter.values
        data = np.array(data)

        # Normalize
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_value = scaler.fit_transform(data)

        # Reshaping process
        seq_legth = 3
        result_data = []
        for i in range(seq_legth, len(scaled_value)):
            result_data.append(scaled_value[i - seq_legth:i, 0])

        result_data = np.array(result_data)
        result_data = np.reshape(
            result_data, (result_data.shape[0], result_data.shape[1], 1))

        # Make predictions
        predict = self.model_1.predict(result_data)
        unscaled_predict = scaler.inverse_transform(predict)

        # Return as JSON\
        seperate_data_beras = unscaled_predict.flatten().tolist()
        return seperate_data_beras

    @functools.lru_cache(maxsize=128)
    def predictBawangMerah(self):
        # Filter Data as 'Beras' only
        data_filter = self.df.filter(['Bawang Merah'])
        data = data_filter.values
        data = np.array(data)

        # Normalize
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_value = scaler.fit_transform(data)

        # Reshaping process
        seq_legth = 3
        result_data = []
        for i in range(seq_legth, len(scaled_value)):
            result_data.append(scaled_value[i - seq_legth:i, 0])

        result_data = np.array(result_data)
        result_data = np.reshape(
            result_data, (result_data.shape[0], result_data.shape[1], 1))

        # Make predictions
        predict = self.model_2.predict(result_data)
        unscaled_predict = scaler.inverse_transform(predict)

        # Return as JSON
        data_one_dimension = unscaled_predict.flatten().tolist()
        return data_one_dimension

    @functools.lru_cache(maxsize=128)
    def predictBawangPutih(self):
        # Filter Data as 'Beras' only
        data_filter = self.df.filter(['Bawang Putih'])
        data = data_filter.values
        data = np.array(data)

        # Normalize
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_value = scaler.fit_transform(data)

        # Reshaping process
        seq_legth = 3
        result_data = []
        for i in range(seq_legth, len(scaled_value)):
            result_data.append(scaled_value[i - seq_legth:i, 0])

        result_data = np.array(result_data)
        result_data = np.reshape(
            result_data, (result_data.shape[0], result_data.shape[1], 1))

        # Make predictions
        predict = self.model_3.predict(result_data)
        unscaled_predict = scaler.inverse_transform(predict)

        # Return as JSON
        data_one_dimension = unscaled_predict.flatten().tolist()
        return data_one_dimension

    @functools.lru_cache(maxsize=128)
    def predictMultivariative(self):
        df_raw = self.df_multiforecast.drop(['Daging Ayam', 'Daging Sapi', 'Telur Ayam', 'Minyak Goreng', 'Gula Pasir'], axis=1)
        cols = list(df_raw)[1:]
        dates = df_raw.Date
        df_for_training = df_raw[cols].astype(float)

        scaler = MinMaxScaler()
        df_for_training_scaled = scaler.fit_transform(df_for_training)
        df_for_training_scaled

        trainX = []
        n_future = 90
        n_past = 30

        for i in range(n_past, len(df_for_training_scaled) - n_future + 1):
            trainX.append(df_for_training_scaled[i - n_past:i, 0:df_for_training.shape[1]])

        trainX = np.array(trainX)

        forecast_period_dates = pd.date_range(list(dates)[-1], periods=n_future, freq='1d').tolist()
        forecast = self.model_5.predict(trainX[-n_future:])

        y_pred_future = scaler.inverse_transform(forecast)

        forecast_dates = []
        for time_i in forecast_period_dates:
            forecast_dates.append(time_i.date())

        df_forecast = pd.DataFrame({'Date': np.array(forecast_dates).astype(str),
                                    'Beras': y_pred_future[:, 0],
                                    'Bawang Merah': y_pred_future[:, 1],
                                    'Bawang Putih': y_pred_future[:, 2],
                                    'Cabai Merah': y_pred_future[:, 3],
                                    'Cabai Rawit': y_pred_future[:, 4]})

        dict_data = {}

        for index, row in df_forecast.iterrows():
            name = row['Date']
            data = {
                'Beras': row['Beras'],
                'Bawang Merah': row['Bawang Merah'],
                'Bawang Putih': row['Bawang Putih'],
                'Cabai Merah': row['Cabai Merah'],
                'Cabai Rawit': row['Cabai Rawit'],
            }
            dict_data[name] = data

        # Print or use the JSON data as desired
        return jsonify(dict_data)

    @functools.lru_cache(maxsize=128)
    def predictCabaiMerah(self):
        # Filter Data as 'Beras' only
        data_filter = self.df.filter(['Cabai Merah'])
        data = data_filter.values
        data = np.array(data)

        # Normalize
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_value = scaler.fit_transform(data)

        # Reshaping process
        seq_legth = 3
        result_data = []
        for i in range(seq_legth, len(scaled_value)):
            result_data.append(scaled_value[i - seq_legth:i, 0])

        result_data = np.array(result_data)
        result_data = np.reshape(
            result_data, (result_data.shape[0], result_data.shape[1], 1))

        # Make predictions
        predict = self.model_4.predict(result_data)
        unscaled_predict = scaler.inverse_transform(predict)

        # Return as JSON
        data_one_dimension = unscaled_predict.flatten().tolist()
        return data_one_dimension
