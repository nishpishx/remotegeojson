# fake_gps_stream_server.py
import math
import time
import threading
import random
from flask import Flask, jsonify

app = Flask(__name__)

# Base location
BASE_LAT = 37.8591
BASE_LON = 122.4853

# Store all published points
all_points = []

# Lock for thread safety
lock = threading.Lock()

# Publish rate (points per second)
PUBLISH_RATE_HZ = 5  # 5 points/sec
PUBLISH_INTERVAL = 1.0 / PUBLISH_RATE_HZ

start_time = time.time()

def publish_points():
    """Background thread to generate points continuously"""
    while True:
        t = time.time() - start_time

        # Simulate circular motion + small random offset
        latitude  = BASE_LAT + 0.0001 * math.sin(t / 10.0) + random.uniform(-0.00005, 0.00005)
        longitude = BASE_LON + 0.0001 * math.cos(t / 10.0) + random.uniform(-0.00005, 0.00005)
        altitude  = 5.0 + 0.1 * math.sin(t / 5.0)

        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [longitude, latitude]
            },
            "properties": {
                "altitude": altitude
            }
        }

        with lock:
            all_points.append(feature)
            # Optional: limit max points for performance
            if len(all_points) > 1000:
                all_points.pop(0)

        time.sleep(PUBLISH_INTERVAL)

# Start background publishing thread
threading.Thread(target=publish_points, daemon=True).start()

@app.route('/gps.geojson')
def get_gps():
    """Return all points accumulated so far"""
    with lock:
        geojson = {
            "type": "FeatureCollection",
            "features": list(all_points)
        }
    return jsonify(geojson)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
