"""
This test suite includes tests for the initialization of the Queue object,
adding items to the queue, creating temporary videos using the provided ffmpeg
command, and cleaning up temporary files.
"""
import os
import tempfile
import shutil
from unittest import TestCase
from unittest.mock import MagicMock, patch

from slideshow.Queue import Queue


class TestQueue(TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.temp_prefix = "temp"
        self.queue = Queue(self.temp_dir, self.temp_prefix)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_init(self):
        """
        Test the initialization of the Queue object and
        the creation of the temporary directory.
        """
        self.assertEqual(self.queue.tempFileFolder, self.temp_dir)
        self.assertEqual(self.queue.tempFilePrefix, self.temp_prefix)
        self.assertTrue(os.path.exists(self.temp_dir))

    def test_add_item(self):
        """
        Test the addition of an item to the queue and
        the generation of the output name.
        """
        inputs = ["input1.mp4", "input2.mp4"]
        filters = ["filter1", "filter2"]
        suffix = "1"

        output_name = self.queue.addItem(inputs, filters, suffix)
        expected_output_name = os.path.join(
            self.temp_dir, f"{self.temp_prefix}{suffix}.mp4"
        )

        self.assertEqual(output_name, expected_output_name)
        self.assertEqual(self.queue.getQueueLength(), 1)

    def test_create_temporary_video(self):
        """
        Test the creation of a temporary video file using the provided ffmpeg command and item.
        """
        item = {
            "inputs": ["input1.mp4", "input2.mp4"],
            "filters": ["filter1", "filter2"],
            "suffix": "1",
        }

        with patch("subprocess.call", MagicMock()) as mock_subprocess_call:
            self.queue.createTemporaryVideo("ffmpeg", item)

            mock_subprocess_call.assert_called_once()

    def test_clean(self):
        """
        Test the cleanup of temporary files created during the process.
        """
        item = {
            "inputs": ["input1.mp4", "input2.mp4"],
            "filters": ["filter1", "filter2"],
            "suffix": "1",
        }

        self.queue.createTemporaryVideo("ffmpeg", item)

        self.queue.clean()

        self.assertEqual(self.queue.getQueueLength(), 0)
        for temp_file in self.queue.tempFiles:
            self.assertFalse(os.path.exists(os.path.join(self.temp_dir, temp_file)))
