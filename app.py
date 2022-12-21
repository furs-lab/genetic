from flask import Flask, jsonify, request, abort
from datetime import datetime

import main

REQUESTS_PER_MINUTE = 3
requests_number = 0
previous_time = datetime.now()

app = Flask(__name__)


def can_response():
    global requests_number, previous_time
    requests_number += 1
    if (datetime.now() - previous_time).seconds > 60:
        previous_time = datetime.now()
        requests_number = 1
    return requests_number <= REQUESTS_PER_MINUTE


@app.route('/')
def index():
    return "Genetic web-service 0.0.1"


@app.route('/results', methods=['GET'])
def get_tasks():
    if not request.json:
        abort(400)
    if not can_response():
        return jsonify({'error': f'limit {REQUESTS_PER_MINUTE} requests per minute'})
    dic = main.create_json_test(request.json)
    dic = request.json
    return jsonify(dic)


if __name__ == '__main__':
    app.run(debug=True)
