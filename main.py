# * Diskusi mengenai prediksi menanam tanaman menggunakan Cuaca
from flask import Flask, jsonify, request
from ML.TimeSeries import TimeSeries
from ML.Classification import Classification
import requests
from flask_caching import Cache
import os


app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

time_series = TimeSeries()
klasifikasi = Classification()

@app.route('/predict', methods=['GET'])
@cache.cached(timeout=None)
def predict():
    return time_series.predict()

@app.route('/classification', methods=['GET'])
def classification():
    try:
        # 2 step enconde from base64 and then url-encode
        image_text = request.args.get('text-image')
        return klasifikasi.predict_img(image_text)
    except Exception as e:
        return jsonify(message = "ukuran harus 150 x 150"),400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port='8000', debug='True')
else:
    print("Tidak bisa menjalankan program ini")
