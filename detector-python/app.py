import os
import time
import threading
import requests
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from video_processor import VideoProcessor

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173", "http://localhost:5174"])

app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

processor = VideoProcessor()
JAVA_BACKEND_URL = "http://localhost:8080/traffic/update"


def update_java_backend():
    """Send lane data to Java backend every 2 seconds."""
    while True:
        lane_data = processor.get_lane_data()
        if lane_data:
            payload = {"lanes": lane_data}
            try:
                requests.post(JAVA_BACKEND_URL, json=payload, timeout=1)
            except requests.exceptions.RequestException:
                pass
        time.sleep(2)


update_thread = threading.Thread(target=update_java_backend, daemon=True)
update_thread.start()


@app.route("/upload", methods=["POST"])
def upload_videos():
    """Accept 4 lane video files and start processing."""
    lanes = ["lane_1", "lane_2", "lane_3", "lane_4"]
    uploaded_files = []

    for lane in lanes:
        if lane not in request.files:
            return jsonify({"error": f"Missing file for {lane}"}), 400

        file = request.files[lane]
        if file.filename == "":
            return jsonify({"error": f"No selected file for {lane}"}), 400

        file_path = os.path.join(app.config["UPLOAD_FOLDER"], f"{lane}.mp4")
        file.save(file_path)
        uploaded_files.append(file_path)

        processor.start_lane(lane, file_path)

    return jsonify({
        "message": "Videos uploaded and processing started",
        "files": uploaded_files
    }), 200


def generate_frames(lane_id):
    """MJPEG frame generator for live stream."""
    while True:
        frame = processor.get_frame(lane_id)
        if frame:
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
            )
        else:
            time.sleep(0.1)


@app.route("/video_feed/<lane_id>")
def video_feed(lane_id):
    """Return MJPEG stream for a lane."""
    if lane_id not in ["lane_1", "lane_2", "lane_3", "lane_4"]:
        return "Invalid lane ID", 404

    return Response(
        generate_frames(lane_id),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/status", methods=["GET"])
def get_status():
    """Return current lane counts and scores."""
    return jsonify(processor.get_lane_data())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)