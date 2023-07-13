import subprocess
from pathlib import Path
from unittest import mock

import pytest
from unittest.mock import MagicMock

from slideshow.VideoSlide import VideoSlide

PROJECT_ROOT = Path(__file__).parent.parent
VIDEO_FILE = PROJECT_ROOT / "tests" / "fixtures" / "video.mp4"


class TestVideoSlide:
    """
    Test class for VideoSlide class
    """

    @pytest.fixture
    def video_slide(self):
        """
        VideoSlide instance fixture
        """
        vs = VideoSlide(
            ffmpeg_version="ffmpeg_version",
            file=VIDEO_FILE,
            ffprobe="ffprobe",
            output_width=1280,
            output_height=720,
            fade_duration=1,
            title="title",
            fps=60,
            overlay_text="overlay_text",
            overlay_color="overlay_color",
            transition="random",
            force_no_audio=False,
            video_start=0,
            video_end=5,
        )
        return vs

    def test_calculate_duration_after_trimming(self, video_slide):
        """
        Test if duration after trimming is calculated correctly.
        This test is useful to ensure proper calculation of the trimmed duration.
        """
        video_slide.calculateDurationAfterTrimming()
        assert video_slide.is_trimmed
        assert video_slide.duration == 5

    def test_set_force_no_audio(self, video_slide):
        """
        Test if force_no_audio flag is set and has_audio is updated accordingly.
        This test is useful to ensure proper handling of the force_no_audio flag.
        """
        video_slide.setForceNoAudio(True)
        assert video_slide.force_no_audio
        assert not video_slide.has_audio

    def test_get_filter(self, video_slide):
        """
        Test if the correct filter string is returned.
        This test is useful to ensure the filter string is generated correctly.
        """
        filter_str = video_slide.getFilter()
        assert (
                'scale=w=-1:h=720,fps=60,pad=1280:720:(ow-iw)/2:(oh-ih)/2,trim=start=0:end=5,setpts=PTS-STARTPTS'
            in filter_str
        )

    def test_get_audio_filter(self, video_slide):
        """
        Test if the correct audio filter string is returned.
        This test is useful to ensure the audio filter string is generated correctly.
        """
        audio_filter_str = video_slide.getAudioFilter()
        assert "atrim=start=0:end=5,asetpts=PTS-STARTPTS" == audio_filter_str

    def test_get_object(self, video_slide):
        """
        Test if the correct object is returned.
        This test is useful to ensure the object representation is generated correctly.
        """
        config = MagicMock()
        obj = video_slide.getObject(config)
        assert obj["force_no_audio"] == False
        assert obj["start"] == 0
        assert obj["end"] == 5

    def test_subprocess_call(self, monkeypatch):
        """
        Test if subprocess_call method returns the correct output.
        This test is useful to ensure proper output is returned from the subprocess call.
        """
        video_slide = VideoSlide(
            "ffmpeg_version",
            VIDEO_FILE,
            "ffprobe",
            1280,
            720,
        )

        with mock.patch.object(subprocess, "check_output") as mock_method:
            mock_method.return_value = b"output"
            output = video_slide.subprocess_call(["command"])
            assert output == "output"
