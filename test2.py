# fake_gps_server.py
import math
import time
from flask import Flask, jsonify

app = Flask(__name__)
start_time = time.time()

@app.route('/gps.geojson')
def get_gps():
    t = time.time() - start_time
    latitude  = 37.4219999 + 0.0001 * math.sin(t / 10.0)
    longitude = -122.0840575 + 0.0001 * math.cos(t / 10.0)
    altitude  = 5.0 + 0.1 * math.sin(t / 5.0)

    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [longitude, latitude]
                },
                "properties": {
                    "altitude": altitude
                }
            }
        ]
    }
    return jsonify(geojson)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
