#!/usr/bin/env python3

import subprocess


class AudioFile:
    def __init__(self, file, ffprobe):

        self.file = file

        # check if file exists
        err = subprocess.check_output(["%s" % (ffprobe), "-v", "error", "-i", file])
        if err:
            print(err)
            raise ValueError("File %s does not exist" % (file))

        duration = subprocess.check_output(
            [
                "%s" % (ffprobe),
                "-show_entries",
                "format=duration",
                "-v",
                "error",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                file,
            ]
        ).decode()
        self.duration = float(duration)

    def getTimestamps(self, aubio):
        timestamps = (
            subprocess.check_output(
                ["%s" % (aubio), "-i", self.file, "-O", "kl"], stderr=subprocess.DEVNULL
            )
            .decode()
            .splitlines()
        )
        return timestamps

    def getObject(self):
        return self.file
