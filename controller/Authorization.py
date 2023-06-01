from flask import request, jsonify
from functools import wraps


def add_token_to_header(func):
    def wrapper(*args, **kwargs):
        # Memanggil fungsi original
        response = func(*args, **kwargs)

        # check jika response ada variable token dan terisi
        if 'Token' in response:
            # Tambah
            response.headers['Authorization'] = 'Bearer ' + response['Token']
        return response
    return wrapper


def required_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            access_token = request.headers.get('Authorization')
            if access_token:
                return func(*args, **kwargs)
            else:
                # If access is not allowed, return a 401 Unauthorized error
                return jsonify({'message': 'Tidak mempunyai akses'}), 401
        except ImportError:
            return jsonify(message="Token tidak valid")
    return wrapper
