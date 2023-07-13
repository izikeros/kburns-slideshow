from io import BytesIO

import pytest
from PIL import Image, ImageDraw

from slideshow.ImageSlide import ImageSlide


@pytest.fixture(scope="module")
def image_slide_config():
    return {
        "ffmpeg_version": 4,
        "file": None,
        "output_width": 1280,
        "output_height": 720,
        "duration": 5,
        "slide_duration_min": 2,
        "fade_duration": 1,
        "zoom_direction_x": "random",
        "zoom_direction_y": "random",
        "zoom_direction_z": "random",
        "scale_mode": "auto",
        "zoom_rate": 0.1,
        "fps": 60,
        "title": None,
        "overlay_text": None,
        "overlay_color": None,
        "transition": "random",
    }


@pytest.fixture(scope="module")
def image_slide(image_slide_config):
    img = Image.new("RGB", (1920, 1080), color=(73, 109, 137))
    d = ImageDraw.Draw(img)
    d.text((10, 10), "Hello world", fill=(255, 255, 0))
    buffer = BytesIO()
    img.save(buffer, "JPEG")
    buffer.seek(0)
    image_slide_config["file"] = buffer
    return ImageSlide(**image_slide_config)
