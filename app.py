from flask import Flask, render_template, request
from analyzer.gps_analysis import analyze_gpx
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["gpxfile"]
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)
        results = analyze_gpx(filepath)
        return render_template("index.html", results=results)
    return render_template("index.html", results=None)

if __name__ == "__main__":
    app.run(debug=True)
