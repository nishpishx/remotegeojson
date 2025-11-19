# fake_gps_server_50pts.py
import math
import time
import random
from flask import Flask, jsonify

app = Flask(__name__)
start_time = time.time()

NUM_POINTS = 50
points_offsets = [(random.uniform(-0.01, 0.01), random.uniform(-0.01, 0.01)) for _ in range(NUM_POINTS)]

@app.route('/seeds.geojson')
def get_gps():
    t = time.time() - start_time
    features = []

    for dx, dy in points_offsets:
        latitude  = 37.4219999 + dy + 0.0001 * math.sin(t / 10.0 + dx*100)
        longitude = -122.0840575 + dx + 0.0001 * math.cos(t / 10.0 + dy*100)

        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [longitude, latitude]
            },
            "properties": {}
        }
        features.append(feature)

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    return jsonify(geojson)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
