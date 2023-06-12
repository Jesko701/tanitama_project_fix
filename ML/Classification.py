# define function predict
import io
import base64
import numpy as np
from PIL import Image
from flask import Flask, jsonify, request
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import load_img, img_to_array
from PIL import Image
import base64
import os
import functools

class Classification():
    path_folder = 'ML/static'
    file_name = 'klasifikasi_new.h5'
    model = load_model(os.path.join(path_folder,file_name))
    # define function prediction
    @functools.lru_cache()
    def predict_img(self,img_input):
        image_data = base64.b64decode(img_input)
        image = Image.open(io.BytesIO(image_data))
        x = img_to_array(image)
        x /= 255
        x = np.expand_dims(x, axis=0)

        images = np.vstack([x])
        classes = self.model.predict(images, batch_size=10)
        result = np.argmax(classes, axis=1)

        if result[0] == 0:
            prediction = {'tanaman': 'Jagung', 'kondisi':'sakit'}
        elif result[0] == 1:
            prediction = {'tanaman': 'Jagung', 'kondisi':'sehat'}
        elif result[0] == 2:
            prediction = {'tanaman': 'Kentang', 'kondisi':'sakit'}
        elif result[0] == 3:
            prediction = {'tanaman': 'Kentang', 'kondisi':'sehat'}
        elif result[0] == 4:
            prediction = {'tanaman': 'Padi', 'kondisi':'sakit'}
        elif result[0] == 5:
            prediction = {'tanaman': 'Padi', 'kondisi':'sehat'}
        elif result[0] == 6:
            prediction = {'tanaman': 'Tomat', 'kondisi':'sakit'}
        elif result[0] == 7:
            prediction = {'tanaman': 'Tomat', 'kondisi':'sehat'}
        
        return prediction
