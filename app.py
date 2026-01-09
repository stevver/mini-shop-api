from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

VERSION = "2.0.0"

PRODUCTS = [
    {"id": 1, "name": "Laptop", "price": 999},
    {"id": 2, "name": "Phone", "price": 599},
]

@app.route("/")
def home():
    return jsonify({
        "message": "Mini Shop API",
        "version": VERSION,
        "timestamp": datetime.now().isoformat(timespec="seconds")
    })

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat(timespec="seconds")}), 200

@app.route("/products")
def products():
    return jsonify(PRODUCTS), 200

@app.route("/api/version")
def api_version():
    return jsonify({"version": VERSION, "build": "stable"}), 200

@app.route("/api/status")
def api_status():
    return jsonify({
        "api": "running",
        "version": VERSION,
        "endpoints": ["/", "/health", "/products", "/api/version", "/api/status"]
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
