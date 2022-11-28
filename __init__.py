from flask import Flask, jsonify


app = Flask(__name__)
app.config.from_object('config')


@app.route('/', methods=['GET'])
def root():
    return jsonify({'message': 'Hello World!'})


if __name__ == '__main__':
    app.run()
