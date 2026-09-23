import os

from dotenv import load_dotenv


load_dotenv()


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "Salesforce/blip-image-captioning-base"
)


UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    os.getenv(
        "UPLOAD_FOLDER",
        "static/uploads"
    )
)


ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "webp",
    "bmp"
}


MAX_CONTENT_LENGTH = (
    int(
        os.getenv(
            "MAX_CONTENT_LENGTH_MB",
            10
        )
    )
    * 1024
    * 1024
)


DEBUG = bool(
    int(
        os.getenv(
            "FLASK_DEBUG",
            1
        )
    )
)
