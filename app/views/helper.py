from werkzeug.security import check_password_hash
from app import app
from .users import user_by_username
import jwt
from flask import request, jsonify
from functools import wraps
from datetime import datetime, timedelta

ALGORITHMS = 'HS256'


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            if 'Authorization' not in request.headers:
                return jsonify({'message': 'token is missing.', 'data': {}}), 401
            try:
                token = request.headers['Authorization'].split()[1]
                if not token:
                    return jsonify({'message': 'token is missing.', 'data': {}}), 401
                data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=ALGORITHMS)
                current_user = user_by_username(username=data['username'])
            except:
                return jsonify({'messsage': 'token is invalid or expired.', 'data': {}}), 401
            return f(current_user, *args, **kwargs)
        except:
            return jsonify({'message': 'token is missing.', 'data': {}}), 401

    return decorated


def auth():
    authorization = request.authorization
    if not authorization or not authorization.username or not authorization.password:
        return jsonify({'message': 'could not verify', 'WWW-Authenticate': 'Basic auth="Login required"'}), 401

    user = user_by_username(authorization.username)
    if not user:
        return jsonify({'message': 'user not found', 'data': {}}), 401

    if user and check_password_hash(user.password, authorization.password):
        token = jwt.encode({'username': user.username,
                            'exp': datetime.now() + timedelta(hours=12),
                            'iat': datetime.now()},
                           app.config['SECRET_KEY'],
                           ALGORITHMS)
        return jsonify({'message': 'Validated successfully', 'token': token,
                        'exp': datetime.now() + timedelta(hours=12)}), 200

    return jsonify({'message': 'could not verify', 'WWW-Authenticate': 'Basic auth="Login required"'}), 401
