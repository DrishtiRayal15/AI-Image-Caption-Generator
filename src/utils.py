import os
import uuid

from werkzeug.utils import secure_filename

from src.config import (
    ALLOWED_EXTENSIONS,
    UPLOAD_FOLDER
)


def allowed_file(filename: str) -> bool:

    return (
        "."
        in filename
        and filename.rsplit(
            ".",
            1
        )[1].lower()
        in ALLOWED_EXTENSIONS
    )


def save_upload(file_storage) -> str:

    os.makedirs(
        UPLOAD_FOLDER,
        exist_ok=True
    )


    original_name = secure_filename(
        file_storage.filename
    )


    extension = (
        original_name
        .rsplit(".", 1)[1]
        .lower()
    )


    unique_name = (
        f"{uuid.uuid4().hex}.{extension}"
    )


    save_path = os.path.join(
        UPLOAD_FOLDER,
        unique_name
    )


    file_storage.save(
        save_path
    )


    return save_path
