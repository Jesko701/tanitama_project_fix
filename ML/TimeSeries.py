import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from flask import jsonify
import os

class TimeSeries():
    def predictBeras(self):
        model_folder = "ML/static"
        model_filename = "1.h5"
        model_path = os.path.join(model_folder, model_filename)
        model = tf.keras.models.load_model(model_path)
        
        #Load Data
        data_folder = "ML/data"
        data_name = "DataBaru_HargaPangan.csv"
        df = pd.read_csv(os.path.join(data_folder,data_name))

        #Filter Data as 'Beras' only
        data_filter = df.filter(['Beras'])
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
        predict = model.predict(result_data)
        unscaled_predict = scaler.inverse_transform(predict)

        #Return as JSON\
        seperate_data_beras = unscaled_predict.flatten().tolist()
        response = {'Beras': seperate_data_beras}
        return jsonify(response)

    def predictBawangMerah(self):
        model_folder = "ML/static"
        model_filename = "2.h5"
        model_path = os.path.join(model_folder, model_filename)
        model = tf.keras.models.load_model(model_path)

        #Load Data
        data_folder = "ML/data"
        data_name = "DataBaru_HargaPangan.csv"
        df = pd.read_csv(os.path.join(data_folder,data_name))

        #Filter Data as 'Beras' only
        data_filter = df.filter(['Bawang Merah'])
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
        predict = model.predict(result_data)
        unscaled_predict = scaler.inverse_transform(predict)

        #Return as JSON
        data_one_dimension = unscaled_predict.flatten().tolist()
        response = {'Bawang Merah': data_one_dimension}
        return jsonify(response)

    def predictBawangPutih(self):
        model_folder = "ML/static"
        model_filename = "3.h5"
        model_path = os.path.join(model_folder, model_filename)
        model = tf.keras.models.load_model(model_path)

        #Load Data
        data_folder = "ML/data"
        data_name = "DataBaru_HargaPangan.csv"
        df = pd.read_csv(os.path.join(data_folder,data_name))

        #Filter Data as 'Beras' only
        data_filter = df.filter(['Bawang Putih'])
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
        predict = model.predict(result_data)
        unscaled_predict = scaler.inverse_transform(predict)

        #Return as JSON
        data_one_dimension = unscaled_predict.flatten().tolist()
        response = {'Bawang Putih': data_one_dimension}
        return jsonify(response)

    def predictCabaiMerah(self):
        model_folder = "ML/static"
        model_filename = "4.h5"
        model_path = os.path.join(model_folder, model_filename)
        model = tf.keras.models.load_model(model_path)

        #Load Data
        data_folder = "ML/data"
        data_name = "DataBaru_HargaPangan.csv"
        df = pd.read_csv(os.path.join(data_folder,data_name))

        #Filter Data as 'Beras' only
        data_filter = df.filter(['Cabai Merah'])
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
        predict = model.predict(result_data)
        unscaled_predict = scaler.inverse_transform(predict)

        #Return as JSON
        data_one_dimension = unscaled_predict.flatten().tolist()
        response = {'Cabai Merah': data_one_dimension}
        return jsonify(response)