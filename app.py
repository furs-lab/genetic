from flask import Flask, jsonify

import main

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/tasks', methods=['GET'])
def get_tasks():
    dic = main.create_json_test()
    return jsonify(dic)


if __name__ == '__main__':
    app.run(debug=True)
