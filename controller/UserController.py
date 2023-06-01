from flask import jsonify
from database.UserModel import UserModel, db
from controller.AuthenticationController import JWT
from controller.Authorization import add_token_to_header
from dotenv import load_dotenv
import os
import re

load_dotenv()
user_jwt = JWT(os.getenv('secret_key'))


class UserController():
    def createUser(self, username, email, password, confirmPass):
        username = username
        email = email
        password = password
        confirmPassword = confirmPass

        pattern = re.compile(r"^[a-z0-9](\.?[a-z0-9]){5,}@g(oogle)?mail\.com$")
        pattern2 = re.compile(r"^[a-z0-9](\.?[a-z0-9]){5,}@y(ahoo)?ahoo\.com$")
        # inp = email
        if not pattern.match(email) and not pattern2.match(email):
            return jsonify({"message": "Email harus lebih dari 5 karakter, dan menggunakan yahoo atau gmail "}), 400

        if password != confirmPassword:
            return jsonify({"message": "Password tidak sama dengan sebelumnya"}), 400

        userData = UserModel(username, email, password)
        db.session.add(userData)
        db.session.commit()
        Data = {
            "username": username,
            "email": email,
            "password": password,
            "confirmPassword": confirmPass
        }
        return jsonify(message="Berhasil membuat data", data=Data), 201

    # For the Admin
    def getAll(self):
        data = UserModel.query.all()
        custom_data = []
        for d in data:
            user_data = {
                "id": d.id,
                "username": d.username,
                "email": d.email,
            }
            custom_data.append(user_data)
        return jsonify(message="Berhasil mengambil seluruh users", data=custom_data), 200

    def loginUser(self, username, password):
        try:  # Test for SSL features
            user = UserModel.query.filter_by(username=username).first()
            if user is None:
                return jsonify({"message": "Username tidak ditemukan"}), 404
            if user.password != password:
                return jsonify({"message": "Password salah"}), 400

            format_data = {
                "id": user.id,
                "username": user.username,
            }
            token = user_jwt.generateToken(format_data, 1)
            add_token_to_header(token)
            return jsonify(message="Login berhasil", token=token), 200
        except ImportError:
            return jsonify({"message": "Username tidak ditemukan"}), 404

    def payloadUser(self, token):
        try:
            data = user_jwt.decode_token(token)
            return jsonify(message="Berhasil mengambil data", data=data), 200
        except ImportError:
            return jsonify({"message": "Token salah"}), 400

    # For the Admin
    def updateUser(self, id, username=None, email=None):
        user = UserModel.query.filter_by(id=id).first()
        if user is None:
            return jsonify({"message": "User tidak ditemukan"}), 404
        if username:
            user.username = username
            if email:
                user.email = email
                db.session.commit()

                data_format = {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }

                return jsonify(message="User berhasil diupdate", data=data_format), 200
    # For the Admin

    def deleteUser(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if user is None:
            return jsonify({"message": "User tidak ditemukan"}), 404

        data_format = {
            "id": user.id,
        }

        db.session.delete(user)
        db.session.commit()
        return jsonify(message="User berhasil dihapus", data=data_format), 200
