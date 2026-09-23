import os
import sys

import pytest

from PIL import Image


sys.path.insert(
    0,
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)


from src.utils import allowed_file
from src.model import generate_caption


def test_allowed_file_accepts_valid_extensions():

    assert allowed_file("photo.jpg")
    assert allowed_file("photo.jpeg")
    assert allowed_file("photo.PNG")
    assert allowed_file("photo.webp")
    assert allowed_file("photo.bmp")


def test_allowed_file_rejects_invalid_extensions():

    assert not allowed_file("document.pdf")
    assert not allowed_file("video.mp4")
    assert not allowed_file("document.txt")
    assert not allowed_file("no_extension")


@pytest.mark.slow
def test_generate_caption_returns_string(
    tmp_path
):

    image_path = (
        tmp_path / "test.jpg"
    )


    Image.new(
        "RGB",
        (224, 224),
        color=(120, 180, 90)
    ).save(image_path)


    caption = generate_caption(
        str(image_path)
    )


    assert isinstance(
        caption,
        str
    )

    assert len(caption) > 0
