import math

import flask
from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['get', 'post'])
def hello():
    return flask.render_template("hello.html")


@app.route('/recieveData', methods=['post'])
def recieveData():
    data = request.form

    if isinstance(data, dict):
        print("MIC 1:", data['mic1'])
        print("MIC 2:", data['mic2'])
        print("Extra Samples", data['samples'])

        L1 = int(data['mic1'])
        L2 = int(data['mic2'])

        D = int(data['samples'])

        try:
            angle = (180 / math.pi) * math.acos((0.07 / (343 * D / 15000)) * (10 ** ((L2 - L1) / 20) - 1))
            print("ANGLE", angle)
        except ValueError:
            print("DOMAIN ERROR")

    return data


if __name__ == "__main__":
    app.run(
        debug=True,
        port=5892
    )
