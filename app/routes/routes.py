from app import app
from app.views import users
from flask import jsonify


@app.route('/', methods=['GET'])
def root():
    return jsonify({'message': 'Hello World!'})


@app.route('/users', methods=['POST'])
def post_user():
    return users.post_user()
