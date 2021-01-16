from flask import Flask, jsonify, request
from flask_cors import cross_origin
import json

app = Flask(__name__)


@app.route('/get_sample', methods=['GET'])
@cross_origin()
def get_sample():
    name = request.args.get('name')
    return 'hello {}'.format(name)

@app.route('/post_sample', methods=['POST'])
@cross_origin()
def post_sample():
    data = request.get_data().decode("utf-8")
    print(data)
    return data


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8090, debug=True)