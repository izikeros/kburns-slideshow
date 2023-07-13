import pytest
import subprocess

from slideshow import PROJECT_ROOT
from slideshow.AudioFile import AudioFile
from unittest import mock

AUDIO_FILE = PROJECT_ROOT / "tests" / "fixtures" / "poin.mp3"

class TestAudioFile:
    @pytest.fixture(scope="class")
    def audio_file(self):

        return AudioFile(AUDIO_FILE, "ffprobe")

    def test_init(self, audio_file):
        """
        Test if the initialization of the AudioFile class sets
        the file attribute correctly and calculates the duration properly.
        This test is useful because it checks if the class is initialized
        with the correct values and the duration calculation is working.
        """
        assert audio_file.file == AUDIO_FILE
        assert isinstance(audio_file.duration, float)

    def test_getTimestamps(self, audio_file):
        """
        Test if the getTimestamps method returns the expected timestamps list.
        This test is useful because it checks if the method is working as
        intended and the timestamps list is generated correctly.
        """
        with mock.patch.object(subprocess, 'check_output') as mock_method:
            mock_method.return_value = b"1.0\n2.0\n3.0\n"
            expected_timestamps = ["1.0", "2.0", "3.0"]
            assert audio_file.getTimestamps("aubio") == expected_timestamps

    def test_getObject(self, audio_file):
        """
        Test if the getObject method returns the correct file attribute.
        This test is useful because it checks if the method is working as
        intended and the file attribute is returned correctly.
        """
        assert audio_file.getObject() == AUDIO_FILE
