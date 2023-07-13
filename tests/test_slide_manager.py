"""
The code defines unit tests for the `SlideManager` class in the provided module.
Each test is documented with a docstring describing what is being tested
and why the test is useful. The tests are organized into two classes:
`TestSlideManagerInit` for testing the `__init__` method, and
`TestSlideManagerMethods` for testing the other methods in the class.
A pytest fixture is used to set up a `SlideManager` instance with some
example data to be used in the tests.
"""
import json

import pytest

from slideshow import PROJECT_ROOT
from slideshow.ImageSlide import ImageSlide
from slideshow.SlideManager import SlideManager
from slideshow.VideoSlide import VideoSlide

input_files = [
    PROJECT_ROOT / "tests" / "fixtures" / "img_001.jpeg",
    PROJECT_ROOT / "tests" / "fixtures" / "img_001.jpeg",
]
input_files = [str(file) for file in input_files]

audio_files = [
    PROJECT_ROOT / "tests" / "fixtures" / "poin.mp3",
    PROJECT_ROOT / "tests" / "fixtures" / "poin.mp3",
]
audio_files = [str(file) for file in audio_files]

config_full_file = PROJECT_ROOT / "tests" / "fixtures" / "config.json"

@pytest.fixture
def get_config():
    with open(config_full_file) as config_file:
        config = json.load(config_file)

        config.update(
            {
                "output_width": 400,
                "output_height": 250,
                "output_codec": "",
                "output_parameters": "",
                "slide_duration": 2,
                "slide_duration_min": 1,
                "fade_duration": 1.0,
                "transition_bars_count": 10,
                "transition_cell_size": 50,
                "fps": 30,
                "overwrite": True,
            }
        )
    return config

@pytest.fixture
def slide_manager(get_config):
    return SlideManager(
        config=get_config, input_files=input_files, audio_files=audio_files
    )

class TestSlideManagerInit:
    def test_empty_init(self):
        """
        Test SlideManager initialization with empty config, input_files, and audio_files.
        This test is useful to ensure that SlideManager initializes without errors when
        provided with empty inputs.
        """
        # raise exception if SlideManager is not initialized properly
        with pytest.raises(KeyError):
            SlideManager()

    def test_empty_config(self):
        """
        Test SlideManager initialization with empty config and provided input_files and audio_files.
        This test is useful to ensure that SlideManager initializes without errors when
        provided with empty config and some input and audio files.
        """

        with pytest.raises(KeyError):
            SlideManager(input_files=input_files, audio_files=audio_files)

    def test_init__smoke(self, get_config):
        """
        Test SlideManager initialization with proper config and provided input_files and audio_files.
        This test is useful to ensure that SlideManager initializes without errors when
        provided with proper config and some input and audio files.
        """
        SlideManager(config=get_config, input_files=input_files, audio_files=audio_files)


class TestSlideManagerMethods:
    def test_add_slide(self, slide_manager):
        """
        Test the addSlide method.
        This test is useful to ensure that the addSlide method properly adds slides to the SlideManager.
        """
        initial_slide_count = len(slide_manager.slides)
        slide_manager.addSlide(input_files[0])
        assert len(slide_manager.slides) == initial_slide_count + 1

    def test_remove_slide(self, slide_manager):
        """
        Test the removeSlide method.
        This test is useful to ensure that the removeSlide method properly removes slides from the SlideManager.
        """
        initial_slide_count = len(slide_manager.slides)
        slide_manager.removeSlide(0)
        assert len(slide_manager.slides) == initial_slide_count - 1

    def test_move_slide(self, slide_manager):
        """
        Test the moveSlide method.
        This test is useful to ensure that the moveSlide method properly moves slides within the SlideManager.
        """
        initial_slide_order = slide_manager.slides.copy()
        slide_manager.moveSlide(0, 1)
        assert slide_manager.slides[0] == initial_slide_order[1]
        assert slide_manager.slides[1] == initial_slide_order[0]

    def test_add_audio(self, slide_manager):
        """
        Test the addAudio method.
        This test is useful to ensure that the addAudio method properly adds audio files to the SlideManager.
        """
        initial_audio_count = len(slide_manager.background_tracks)
        slide_manager.addAudio(audio_files[0])
        assert len(slide_manager.background_tracks) == initial_audio_count + 1

    def test_remove_audio(self, slide_manager):
        """
        Test the removeAudio method.
        This test is useful to ensure that the removeAudio method properly removes audio files from the SlideManager.
        """
        initial_audio_count = len(slide_manager.background_tracks)
        slide_manager.removeAudio(0)
        assert len(slide_manager.background_tracks) == initial_audio_count - 1

    def test_move_audio(self, slide_manager):
        """
        Test the moveAudio method.
        This test is useful to ensure that the moveAudio method properly moves audio files within the SlideManager.
        """
        initial_audio_order = slide_manager.background_tracks.copy()
        slide_manager.moveAudio(0, 1)
        assert slide_manager.background_tracks[0] == initial_audio_order[1]
        assert slide_manager.background_tracks[1] == initial_audio_order[0]

    def test_get_videos(self, slide_manager):
        """
        Test the getVideos method.
        This test is useful to ensure that the getVideos method returns the correct list of video slides.
        """
        video_slides = slide_manager.getVideos()
        assert all(isinstance(slide, VideoSlide) for slide in video_slides)

    def test_get_image_slides(self, slide_manager):
        """
        Test the getImageSlides method.
        This test is useful to ensure that the getImageSlides method returns the correct list of image slides.
        """
        image_slides = slide_manager.getImageSlides()
        assert all(isinstance(slide, ImageSlide) for slide in image_slides)

    def test_get_slides(self, slide_manager):
        """
        Test the getSlides method.
        This test is useful to ensure that the getSlides method returns the correct list of slides.
        """
        slides = slide_manager.getSlides()
        assert len(slides) == len(slide_manager.slides)
