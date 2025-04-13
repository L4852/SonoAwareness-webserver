import math

import flask
from flask import Flask, request

app = Flask(__name__)


def analogToDecibel(value):
    return 20 * math.log(value, 10)


@app.route('/', methods=['get', 'post'])
def hello():
    return flask.render_template("hello.html")


@app.route('/receiveData', methods=['get'])
def receiveData():
    MIC_SEPARATION = 14  # cm
    SAMPLING_RATE = 15  # kHz
    data = request.args

    if isinstance(data, dict):
        print("-" * 20)
        print("V1:", float(data.get('mic1')))
        print("V2:", float(data.get('mic2')))

        print("Extra Samples:", data.get('samples'))

        L1 = analogToDecibel(float(data.get('mic1')))
        L2 = analogToDecibel(float(data.get('mic2')))

        D = int(data.get('samples'))

        print("MIC 1:", L1)
        print("MIC 2:", L2)

        if (D == 0):
            return {"result": 998}

        try:
            angle = (180 / math.pi) * math.acos(
                ((MIC_SEPARATION / 100) / (343 * D / (SAMPLING_RATE * 1000))) * (10 ** ((L2 - L1) / 20) - 1))
            print("ANGLE", angle)
            print("-" * 20)
            return {
                "result": int(angle)
            }
        except ValueError as e:
            print("ERROR: ", type(e))
            return {"result": 999}


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        debug=True,
        port=5892
    )
