import json
import time
from datetime import datetime
from flask import Flask, render_template, request, jsonify, stream_with_context, Response
from download_data_from_firebase import *

app = Flask(__name__)

import sqlite3


@app.route("/admin")
def getData():  # Retrieve data from database
    x, y, z, v, t = downloadData()
    info = {
        "Toadox": x,
        "Toadoy": y,
        "Toadoz": z,
        "Tocdogio": v,
        "Huonggio": t
    }
    # get_json = json.dumps(info)
    return jsonify(info)


# main route
@app.route("/")
def index():
    dummy_data = data_json()
    return render_template('indexBTS.html', matches=dummy_data.json)


@app.route('/data_json')
def data_json():
    dummy_data = [
        {
            "id": 1,
            "Name": "BTS1",
            "Location": "C1 - ĐHBK",
            "Coordinates": "(20.4213, 204.3211) ",
        },
        {
            "id": 2,
            "Name": "BTS2",
            "Location": "C2 - ĐHBK",
            "Coordinates": "(21.2452, 203.4953)",
        },
        {
            "id": 3,
            "Name": "BTS3",
            "Location": "C3-ĐHBK",
            "Coordinates": "(22.3454, 202.5324)",
        },
    ]
    return jsonify(dummy_data)


@app.route('/cot1')
def infor1():
    return render_template('index1.html')


@app.route('/cot2')
def infor2():
    return render_template('index2.html')


@app.route('/chart-data')
def chart_data():
    def generate_random_data():
        while True:
            x, y, z, v, t = downloadData()
            json_data = json.dumps(
                {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': v, 'toadox': x, 'toadoy': y,
                 'toadoz': z})
            yield f"data:{json_data}\n\n"
            time.sleep(1)

    response = Response(stream_with_context(generate_random_data()), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    # print(response)
    return response


if __name__ == "__main__":
    app.run(debug=True, port=6868)
