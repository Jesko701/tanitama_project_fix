# * Diskusi mengenai prediksi menanam tanaman menggunakan Cuaca
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from database.UserModel import init_app
from controller.UserController import UserController  # * with Class 
from controller.Authorization import required_token  # * no Class
from ML.TimeSeries import TimeSeries
from ML.Classification import Classification
import requests
from flask_caching import Cache
import os


load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('database_uri')
app.config['SECRET_KEY'] = os.getenv("secret_key")
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

init_app(app)
user_controller = UserController()
time_series = TimeSeries()
klasifikasi = Classification()

@app.route('/', methods=['GET'])
def helloWL():
    return jsonify(message="Hello World")

@app.route('/users', methods=['GET'])
@required_token
@cache.cached(timeout=None)
def get_all_users():
    return user_controller.getAll()


@app.route('/profile', methods=['GET'])
@required_token
@cache.cached(timeout=None)
def getUser():
    header = request.headers.get('Authorization')
    token = None
    if header.startswith('Bearer '):
        token = header[7:]
    return user_controller.payloadUser(token)


@app.route('/weather', methods=['GET'])
@required_token
@cache.cached(timeout=None)
def weatherAPI():
    try:
        longitude = request.args.get('longitude')
        latitude = request.args.get('latitude')
        url = "https://api.open-meteo.com/v1/forecast?latitude={}&longitude={}&daily=weathercode,rain_sum,windspeed_10m_max&current_weather=true&timezone=Asia%2FBangkok".format(
            latitude, longitude)
        weatherData = requests.get(url)
        return weatherData.json()
    except ImportError:
        return jsonify(message='Gagal mengambil data cuaca'), 200


@app.route('/users', methods=['POST'])
@cache.cached(timeout=None)
def create_user():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    confirm_password = request.json['confirm_password']
    return UserController.createUser(self=UserController, username=username, email=email, password=password, confirmPass=confirm_password)


@app.route('/login', methods=['POST'])
@cache.cached(timeout=None)
def login():
    username = request.json['username']
    pw = request.json['password']
    return user_controller.loginUser(username=username, password=pw)

@app.route('/logoutPerson', methods=['POST'])
@cache.cached(timeout=None)
@required_token
def logout():
    return user_controller.logout()

@app.route('/predictBeras',methods=['GET'])
@cache.cached(timeout=None)
def predictBeras():
    return time_series.predictBeras()

@app.route('/predictCabaiMerah', methods=['GET'])
@cache.cached(timeout=None)
def predictCabaiMerah():
    return time_series.predictCabaiMerah()

@app.route('/predictBawangMerah',methods=['GET'])
@cache.cached(timeout=None)
def predictBawangMerah():
    return time_series.predictBawangMerah()

@app.route('/predictBawangPutih',methods=['GET'])
@cache.cached(timeout=None)
def predictBawangPutih():
    return time_series.predictBawangPutih()

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
