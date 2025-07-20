from flask import Flask, render_template, request, send_file
from pathlib import Path
import os
from main_minimal import render_tracked_effect

app = Flask(__name__)
UPLOAD_FOLDER = Path("uploads")
OUTPUT_FOLDER = Path("static/output")
UPLOAD_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "video" not in request.files:
            return "No file part", 400
        file = request.files["video"]
        if file.filename == "":
            return "No selected file", 400

        input_path = UPLOAD_FOLDER / file.filename
        file.save(input_path)

        output_path = OUTPUT_FOLDER / f"processed_{file.filename}"
        render_tracked_effect(
            video_in=input_path,
            video_out=output_path,
            fps=None,
            pts_per_beat=15,
            ambient_rate=4.0,
            jitter_px=0.5,
            life_frames=10,
            min_size=12,
            max_size=30,
            neighbor_links=2,
            orb_fast_threshold=20,
            bell_width=4.0,
            seed=None,
        )

        return send_file(output_path, as_attachment=True)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
