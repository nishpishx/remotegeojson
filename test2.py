# fake_gps_straight_line.py
import time
import threading
from flask import Flask, jsonify

app = Flask(__name__)

# Base location
BASE_LAT = 37.8591
BASE_LON = -122.4853

# Store all published points
all_points = []

# Lock for thread safety
lock = threading.Lock()

# Publish 1 point per second, straight line
PUBLISH_INTERVAL = 1.0  # seconds
STEP = 0.0005  # increment in longitude per point

start_time = time.time()
current_lon = BASE_LON

def publish_points():
    """Background thread to generate points in a straight line"""
    global current_lon
    while True:
        latitude = BASE_LAT
        longitude = current_lon
        altitude = 5.0  # constant

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
            # Optional: keep last 1000 points
            if len(all_points) > 1000:
                all_points.pop(0)

        current_lon += STEP  # move east in a straight line
        time.sleep(PUBLISH_INTERVAL)

# Start background publishing thread
threading.Thread(target=publish_points, daemon=True).start()

@app.route('/seeds.geojson')
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
