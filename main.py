# * Diskusi mengenai prediksi menanam tanaman menggunakan Cuaca
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from database.UserModel import init_app
from controller.UserController import UserController  # * with Class
from controller.Authorization import required_token  # * no Class
from ML.TimeSeries import TimeSeries
import requests
import os


load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('database_uri')
app.config['SECRET_KEY'] = os.getenv("secret_key")

init_app(app)
user_controller = UserController()
time_series = TimeSeries()

@app.route('/', methods=['GET'])
def helloWL():
    return jsonify(message="Hello World")

@app.route('/users', methods=['GET'])
@required_token
def get_all_users():
    return user_controller.getAll()


@app.route('/profile', methods=['GET'])
@required_token
def getUser():
    header = request.headers.get('Authorization')
    token = None
    if header.startswith('Bearer '):
        token = header[7:]
    return user_controller.payloadUser(token)


@app.route('/weather', methods=['GET'])
@required_token
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
def create_user():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    confirm_password = request.json['confirm_password']
    return UserController.createUser(self=UserController, username=username, email=email, password=password, confirmPass=confirm_password)


@app.route('/login', methods=['POST'])
def login():
    username = request.json['username']
    pw = request.json['password']
    return user_controller.loginUser(username=username, password=pw)


@app.route('/predictBeras',methods=['GET'])
def predictBeras():
    return time_series.predictBeras()

@app.route('/predictCabaiMerah', methods=['GET'])
def predictCabaiMerah():
    return time_series.predictCabaiMerah()

@app.route('/predictBawangMerah',methods=['GET'])
def predictBawangMerah():
    return time_series.predictBawangMerah()

@app.route('/predictBawangPutih',methods=['GET'])
def predictBawangPutih():
    return time_series.predictBawangPutih()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port='8000', debug='True')
else:
    print("Tidak bisa menjalankan program ini")
