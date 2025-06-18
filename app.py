from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable cross-origin access

# Initial traffic light state
traffic_state = {
    "horizontal": True,
    "vertical": False
}

@app.route("/state", methods=["GET"])
def get_state():
    return jsonify(traffic_state)

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # default to 5000 if not set
    app.run(host="0.0.0.0", port=port))
