import json
import pytest
from argparse import Namespace
from unittest.mock import MagicMock

from slideshow import PROJECT_ROOT
from slideshow.cli import CLI

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


class TestCLI:
    @pytest.fixture
    def config(self):
        return {
            "output_width": 1280,
            "output_height": 720,
            "slide_duration": 5,
            "slide_duration_min": 3,
            "fade_duration": 1,
            "transition": "linear",
            "fps": 30,
            "zoom_direction_x": "random",
            "zoom_direction_y": "random",
            "zoom_direction_z": "random",
            "zoom_rate": 1.1,
            "scale_mode": "auto",
            "loopable": False,
            "overwrite": False,
            "generate_temp": False,
            "delete_temp": False,
            "sync_to_audio": False,
            "sync_titles_to_slides": False,
            "test": False,
            "save": None,
        }

    def test_init(self, config):
        """Test the initialization of the CLI class."""
        cli = CLI(config)

        assert cli.config == config
        assert cli.parser is not None

    def test_parse(self, config, monkeypatch):
        """Test the parse method of the CLI class."""
        cli = CLI(config)

        def mock_parse_args(*args, **kwargs):
            return Namespace(
                size="1920x1080",
                slide_duration=10,
                slide_duration_min=5,
                fade_duration=2,
                fade_transition="ease",
                fps=60,
                zoom_direction_x="left",
                zoom_direction_y="top",
                zoom_direction_z="in",
                zoom_rate=1.2,
                scale_mode="pad",
                loopable=True,
                y=True,
                temp=True,
                delete_temp=True,
                audio=["audio1.mp3", "audio2.mp3"],
                sync_to_audio=True,
                sync_titles_to_slides=True,
                input_files=["input1.jpg", "input2.jpg"],
                file_list=None,
                save="config.json",
                test=True,
                output_file="output.mp4",
            )

        monkeypatch.setattr(cli.parser, "parse_args", mock_parse_args)

        new_config, input_files, audio_files, output_file = cli.parse()

        assert new_config["output_width"] == 1920
        assert new_config["output_height"] == 1080
        assert new_config["slide_duration"] == 10
        assert new_config["slide_duration_min"] == 5
        assert new_config["fade_duration"] == 2
        assert new_config["transition"] == "ease"
        assert new_config["fps"] == 60
        assert new_config["zoom_direction_x"] == "left"
        assert new_config["zoom_direction_y"] == "top"
        assert new_config["zoom_direction_z"] == "in"
        assert new_config["zoom_rate"] == 1.2
        assert new_config["scale_mode"] == "pad"
        assert new_config["loopable"] is True
        assert new_config["overwrite"] is True
        assert new_config["generate_temp"] is True
        assert new_config["delete_temp"] is True
        assert new_config["sync_to_audio"] is True
        assert new_config["sync_titles_to_slides"] is True
        assert new_config["test"] is True
        assert new_config["save"] == "config.json"

        assert input_files == ["input1.jpg", "input2.jpg"]
        assert audio_files == ["audio1.mp3", "audio2.mp3"]
        assert output_file == "output.mp4"

    @pytest.mark.skip(reason="Not fully implemented yet.")
    def test_parse_file_list(self, config, monkeypatch):
        """Test the parse method with a file list."""
        cli = CLI(config)

        def mock_parse_args(*args, **kwargs):
            return Namespace(
                size=None,
                slide_duration=None,
                slide_duration_min=None,
                fade_duration=None,
                fade_transition=None,
                fps=None,
                zoom_direction_x=None,
                zoom_direction_y=None,
                zoom_direction_z=None,
                zoom_rate=None,
                scale_mode=None,
                loopable=False,
                y=False,
                temp=False,
                delete_temp=False,
                audio=None,
                sync_to_audio=False,
                sync_titles_to_slides=False,
                input_files=None,
                file_list="file_list.json",
                save=None,
                test=False,
                output_file="output.mp4",
            )

        def mock_open(*args, **kwargs):
            content = {
                "config": {
                    "slide_duration": 8,
                    "slide_duration_min": 4,
                },
                "slides": ["input1.jpg", "input2.jpg"],
                "audio": ["audio1.mp3", "audio2.mp3"],
            }
            return MagicMock(spec=open, read=MagicMock(return_value=json.dumps(content)))

        monkeypatch.setattr(cli.parser, "parse_args", mock_parse_args)
        monkeypatch.setattr("builtins.open", mock_open)

        new_config, input_files, audio_files, output_file = cli.parse()

        assert new_config["slide_duration"] == 8
        assert new_config["slide_duration_min"] == 4

        assert input_files == ["input1.jpg", "input2.jpg"]
        assert audio_files == ["audio1.mp3", "audio2.mp3"]
        assert output_file == "output.mp4"
