import threading

import torch

from PIL import Image

from transformers import (
    BlipProcessor,
    BlipForConditionalGeneration
)

from src.config import MODEL_NAME


_model_lock = threading.Lock()

_processor = None
_model = None


DEVICE = (
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)


def _load_model():

    global _processor
    global _model

    if _model is None:

        with _model_lock:

            if _model is None:

                print(
                    f"Loading BLIP model on {DEVICE}..."
                )

                _processor = (
                    BlipProcessor.from_pretrained(
                        MODEL_NAME
                    )
                )

                _model = (
                    BlipForConditionalGeneration
                    .from_pretrained(
                        MODEL_NAME
                    )
                )

                _model.to(DEVICE)

                _model.eval()

                print(
                    "BLIP model loaded successfully."
                )

    return _processor, _model


def generate_caption(image_path: str) -> str:

    processor, model = _load_model()


    image = Image.open(
        image_path
    ).convert("RGB")


    inputs = processor(
        image,
        return_tensors="pt"
    ).to(DEVICE)


    with torch.no_grad():

        output_ids = model.generate(
            **inputs,
            max_new_tokens=50,
            num_beams=4,
            early_stopping=True
        )


    caption = processor.decode(
        output_ids[0],
        skip_special_tokens=True
    )


    return caption.strip().capitalize()
