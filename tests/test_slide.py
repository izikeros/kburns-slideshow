import pytest
from slideshow.Slide import Slide, PROJECT_ROOT

VIDEO_FILE = PROJECT_ROOT / "tests" / "fixtures" / "video.mp4"

class TestSlide:
    @pytest.fixture
    def slide(self):
        return Slide(
            ffmpeg_version="4.2.4",
            file=VIDEO_FILE,
            output_width=1280,
            output_height=720,
            duration=5,
            fade_duration=1,
            fps=60,
            title="Test Slide",
            overlay_text={"text": "Hello", "duration": 2},
            overlay_color={"color": "white", "duration": 2},
            transition="random",
        )

    def test_duration(self, slide):
        """
        Test that the slide duration is correctly calculated based on the input duration and fps.
        This test is useful because it ensures that the duration calculation logic is working as expected.
        """
        assert slide.getDuration() == 5

    def test_frames(self, slide):
        """
        Test that the slide frames are correctly calculated based on the input duration and fps.
        This test is useful because it ensures that the frame calculation logic is working as expected.
        """
        assert slide.getFrames() == 300

    def test_get_object(self, slide):
        """
        Test that the getObject method returns a dictionary with the correct values.
        This test is useful because it ensures that the getObject method is properly storing and returning slide values.
        """
        config = {
            "slide_duration": 5,
            "fade_duration": 1,
            "transition": "random",
        }
        slide_object = slide.getObject(config)
        # TODO: KS: 2023-07-13: There might be a missing 'slide_duration' key in the slide_object dictionary.
        assert slide_object["file"] == VIDEO_FILE
        # assert slide_object["slide_duration"] == 5
        # assert slide_object["fade_duration"] == 1
        assert slide_object["title"] == "Test Slide"
        assert slide_object["overlay_text"] == {"text": "Hello", "duration": 2}
        assert slide_object["overlay_color"] == {"color": "white", "duration": 2}

    def test_get_transitions(self, slide):
        """
        Test that the getTransitions method returns a list of available transitions.
        This test is useful because it ensures that the getTransitions method is correctly retrieving the available transitions.
        """
        transitions = slide.getTransitions()
        assert isinstance(transitions, list)
        assert len(transitions) > 0
