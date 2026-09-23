import os

from flask import Flask, jsonify, render_template, request, url_for

from src.config import DEBUG, MAX_CONTENT_LENGTH, UPLOAD_FOLDER
from src.model import generate_caption
from src.utils import allowed_file, save_upload


app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/caption", methods=["POST"])
def caption():

    if "image" not in request.files:
        return jsonify({
            "error": "No image file provided."
        }), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({
            "error": "No file selected."
        }), 400

    if not allowed_file(file.filename):
        return jsonify({
            "error": "Unsupported image format."
        }), 400

    try:

        saved_path = save_upload(file)

        generated_caption = generate_caption(saved_path)

        image_url = url_for(
            "static",
            filename=f"uploads/{os.path.basename(saved_path)}"
        )

        return jsonify({
            "caption": generated_caption,
            "image_url": image_url
        }), 200

    except Exception as error:

        return jsonify({
            "error": f"Failed to process image: {error}"
        }), 500


@app.errorhandler(413)
def file_too_large(_error):

    return jsonify({
        "error": "File too large. Maximum size is 10 MB."
    }), 413


if __name__ == "__main__":

    app.run(
        debug=DEBUG,
        host="0.0.0.0",
        port=5000
    )
