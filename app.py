from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import time

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

traffic_state = {
    "horizontal": True,
    "vertical": False
}

car_counts = {
    "lane1": 0,
    "lane2": 0
}

# Variables to compute average cars per minute
total_cars = 0
start_time = time.time()

@app.route("/state", methods=["GET"])
def get_state():
    global total_cars, start_time

    # Calculate elapsed minutes
    elapsed_minutes = max((time.time() - start_time) / 60, 1/60)  # avoid division by zero

    # Update total cars with latest counts
    total_cars = car_counts["lane1"] + car_counts["lane2"]

    average_per_minute = total_cars / elapsed_minutes

    return jsonify({
        "traffic_state": traffic_state,
        "car_counts": car_counts,
        "average_per_minute": round(average_per_minute, 2)
    })

@app.route("/set", methods=["POST"])
def set_state():
    data = request.json
    traffic_state["horizontal"] = data.get("horizontal", traffic_state["horizontal"])
    traffic_state["vertical"] = data.get("vertical", traffic_state["vertical"])
    return jsonify(traffic_state)

@app.route("/toggle", methods=["POST"])
def toggle_state():
    traffic_state["horizontal"] = not traffic_state["horizontal"]
    traffic_state["vertical"] = not traffic_state["vertical"]
    return jsonify(traffic_state)

@app.route("/counts", methods=["POST"])
def update_counts():
    data = request.json
    car_counts["lane1"] = data.get("lane1", car_counts["lane1"])
    car_counts["lane2"] = data.get("lane2", car_counts["lane2"])
    return jsonify(car_counts)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for Android app

# Initial traffic light state
traffic_state = {
    "horizontal": True,
    "vertical": False
}

# Store car counts
car_counts = {
    "lane1": 0,
    "lane2": 0
}

@app.route("/state", methods=["GET"])
def get_state():
    return jsonify({
        "traffic_state": traffic_state,
        "car_counts": car_counts
    })

@app.route("/set", methods=["POST"])
def set_state():
    data = request.json
    traffic_state["horizontal"] = data.get("horizontal", traffic_state["horizontal"])
    traffic_state["vertical"] = data.get("vertical", traffic_state["vertical"])
    return jsonify(traffic_state)

@app.route("/toggle", methods=["POST"])
def toggle_state():
    traffic_state["horizontal"] = not traffic_state["horizontal"]
    traffic_state["vertical"] = not traffic_state["vertical"]
    return jsonify(traffic_state)

@app.route("/counts", methods=["POST"])
def update_counts():
    data = request.json
    car_counts["lane1"] = data.get("lane1", car_counts["lane1"])
    car_counts["lane2"] = data.get("lane2", car_counts["lane2"])
    return jsonify(car_counts)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # default to 5000 if not set
    app.run(host="0.0.0.0", port=port)
