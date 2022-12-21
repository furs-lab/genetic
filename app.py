from flask import Flask, jsonify, request, abort
from json import dump

import main

app = Flask(__name__)


@app.route('/')
def index():
    return "Genetic web-service 0.0.1"


@app.route('/results', methods=['GET'])
def get_tasks():
    if not request.json:
        abort(400)
    dic = main.create_json_test(request.json)
    return jsonify(request.json)


if __name__ == '__main__':
    app.run(debug=True)
