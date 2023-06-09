# * Diskusi mengenai prediksi menanam tanaman menggunakan Cuaca
from flask import Flask, jsonify, request
from ML.TimeSeries import TimeSeries
from ML.Classification import Classification
from flask_caching import Cache
import base64, io
from PIL import Image


app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

time_series = TimeSeries()
klasifikasi = Classification()

@app.route('/predict', methods=['GET'])
@cache.cached(timeout=None)
def predict():
    return time_series.predict()

@app.route('/classification', methods=['POST'])
def classification():
    try:
        # 2 step from resizing to encode to b64
        file_data = request.files['image-file']
        if file_data:
            #change the size of the file to 150x150
            image = Image.open(file_data)
            resize_image = image.resize((150,150))
            buffer = io.BytesIO()
            resize_image.save(buffer, format='JPEG')

            #encode the image file to base64
            buffer.seek(0)
            image_encoded_string = base64.b64encode(buffer.read()).decode('utf-8')
            return klasifikasi.predict_img(image_encoded_string)
        return jsonify(message='Tidak ada file yang diupload')
        # return klasifikasi.predict_img(my_image)
    except Exception as e:
        return jsonify(message = str(e)),400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port='8080', debug='True')
else:
    print("Tidak bisa menjalankan program ini")
