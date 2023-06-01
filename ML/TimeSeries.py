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
    model_path_1 = os.path.join(model_folder, model_filename_1)
    model_path_2 = os.path.join(model_folder, model_filename_2)
    model_path_3 = os.path.join(model_folder, model_filename_3)
    model_path_4 = os.path.join(model_folder, model_filename_4)
    model_1 = tf.keras.models.load_model(model_path_1)
    model_2 = tf.keras.models.load_model(model_path_2)
    model_3 = tf.keras.models.load_model(model_path_3)
    model_4 = tf.keras.models.load_model(model_path_4)


    # Load data CSV
    data_folder = "ML/data"
    data_name = "DataBaru_HargaPangan.csv"
    df = pd.read_csv(os.path.join(data_folder,data_name))
    @functools.lru_cache(maxsize=128)
    def predictBeras(self):
        #Filter Data as 'Beras' only
        data_filter = self.df.filter(['Beras'])
        data = data_filter.values
        data = np.array(data)

        #Normalize
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_value = scaler.fit_transform(data)

        #Reshaping process
        seq_legth = 3
        result_data = []
        for i in range(seq_legth, len(scaled_value)):
            result_data.append(scaled_value[i - seq_legth:i, 0])

        result_data = np.array(result_data)
        result_data = np.reshape(result_data, (result_data.shape[0], result_data.shape[1], 1))

        #Make predictions
        predict = self.model_1.predict(result_data)
        unscaled_predict = scaler.inverse_transform(predict)

        #Return as JSON\
        seperate_data_beras = unscaled_predict.flatten().tolist()
        response = {'Beras': seperate_data_beras}
        return jsonify(response)

    @functools.lru_cache(maxsize=128)
    def predictBawangMerah(self):
        #Filter Data as 'Beras' only
        data_filter = self.df.filter(['Bawang Merah'])
        data = data_filter.values
        data = np.array(data)

        #Normalize
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_value = scaler.fit_transform(data)

        #Reshaping process
        seq_legth = 3
        result_data = []
        for i in range(seq_legth, len(scaled_value)):
            result_data.append(scaled_value[i - seq_legth:i, 0])

        result_data = np.array(result_data)
        result_data = np.reshape(result_data, (result_data.shape[0], result_data.shape[1], 1))

        #Make predictions
        predict = self.model_2.predict(result_data)
        unscaled_predict = scaler.inverse_transform(predict)

        #Return as JSON
        data_one_dimension = unscaled_predict.flatten().tolist()
        response = {'Bawang Merah': data_one_dimension}
        return jsonify(response)

    @functools.lru_cache(maxsize=128)
    def predictBawangPutih(self):
        #Filter Data as 'Beras' only
        data_filter = self.df.filter(['Bawang Putih'])
        data = data_filter.values
        data = np.array(data)

        #Normalize
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_value = scaler.fit_transform(data)

        #Reshaping process
        seq_legth = 3
        result_data = []
        for i in range(seq_legth, len(scaled_value)):
            result_data.append(scaled_value[i - seq_legth:i, 0])

        result_data = np.array(result_data)
        result_data = np.reshape(result_data, (result_data.shape[0], result_data.shape[1], 1))

        #Make predictions
        predict = self.model_3.predict(result_data)
        unscaled_predict = scaler.inverse_transform(predict)

        #Return as JSON
        data_one_dimension = unscaled_predict.flatten().tolist()
        response = {'Bawang Putih': data_one_dimension}
        return jsonify(response)

    @functools.lru_cache(maxsize=128)
    def predictCabaiMerah(self):
        #Filter Data as 'Beras' only
        data_filter = self.df.filter(['Cabai Merah'])
        data = data_filter.values
        data = np.array(data)

        #Normalize
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_value = scaler.fit_transform(data)

        #Reshaping process
        seq_legth = 3
        result_data = []
        for i in range(seq_legth, len(scaled_value)):
            result_data.append(scaled_value[i - seq_legth:i, 0])

        result_data = np.array(result_data)
        result_data = np.reshape(result_data, (result_data.shape[0], result_data.shape[1], 1))

        #Make predictions
        predict = self.model_4.predict(result_data)
        unscaled_predict = scaler.inverse_transform(predict)

        #Return as JSON
        data_one_dimension = unscaled_predict.flatten().tolist()
        response = {'Cabai Merah': data_one_dimension}
        return jsonify(response)