from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)
SAVE_DIR = "received_files"
os.makedirs(SAVE_DIR, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "no file part"}), 400
    f = request.files["file"]
    if f.filename == "":
        return jsonify({"error": "empty filename"}), 400

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    safe_name = f"{timestamp}_{f.filename}"
    path = os.path.join(SAVE_DIR, safe_name)
    f.save(path)
    return jsonify({"status": "saved", "path": path}), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
