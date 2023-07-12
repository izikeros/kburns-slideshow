#!/usr/bin/env python3
import logging
import random

from PIL import ExifTags
from PIL import Image

from .Slide import Slide


class ImageSlide(Slide):
    def __init__(
        self,
        ffmpeg_version,
        file,
        output_width,
        output_height,
        duration,
        slide_duration_min,
        fade_duration=1,
        zoom_direction_x="random",
        zoom_direction_y="random",
        zoom_direction_z="random",
        scale_mode="auto",
        zoom_rate=0.1,
        fps=60,
        title=None,
        overlay_text=None,
        overlay_color=None,
        transition="random",
    ):
        self.zoom_rate = zoom_rate
        self.slide_duration_min = slide_duration_min
        if slide_duration_min > duration:
            duration = slide_duration_min

        super().__init__(
            ffmpeg_version,
            file,
            output_width,
            output_height,
            duration,
            fade_duration,
            fps,
            title,
            overlay_text,
            overlay_color,
            transition,
        )

        im = Image.open(self.file)

        """
        iPhone images are rotated, so rotate them according to the EXIF information
        https://stackoverflow.com/questions/37780729/ffmpeg-rotates-images
        https://stackoverflow.com/questions/13872331/rotating-an-image-with-orientation-specified-in-exif-using-python-without-pil-in#26928142
        """
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == "Orientation":
                    break
            exif = dict(im._getexif().items())

            if exif[orientation] == 3:
                im = im.rotate(180, expand=True)
            elif exif[orientation] == 6:
                im = im.rotate(270, expand=True)
            elif exif[orientation] == 8:
                im = im.rotate(90, expand=True)
            im.save(self.file)
            im.close()

        except (AttributeError, KeyError, IndexError):
            # cases: image don't have getexif
            pass

        width, height = im.size
        self.ratio = width / height

        self.width = width
        self.height = height

        self.setScaleMode(scale_mode)

        self.setZoomDirectionX(zoom_direction_x)
        self.setZoomDirectionY(zoom_direction_y)
        self.setZoomDirectionZ(zoom_direction_z)

    def setScaleMode(self, scale_mode):
        if scale_mode == "auto":
            self.scale = (
                "pad" if abs(self.ratio - self.output_ratio) > 0.5 else "crop_center"
            )
        else:
            self.scale = scale_mode

    def setZoomDirectionX(self, zoom_direction):
        if zoom_direction == "random":
            self.direction_x = random.choice(["left", "right"])
        else:
            self.direction_x = zoom_direction

    def setZoomDirectionY(self, zoom_direction):
        if zoom_direction == "random":
            self.direction_y = random.choice(["top", "bottom"])
        else:
            self.direction_y = zoom_direction

    def setZoomDirectionZ(self, zoom_direction):
        if zoom_direction == "random":
            self.direction_z = random.choice(["in", "out"])
        elif zoom_direction == "none":
            self.direction_x = "center"
            self.direction_y = "center"
            self.direction_z = "none"
        else:
            self.direction_z = zoom_direction

    def getFilter(self):
        slide_filters = ["format=pix_fmts=yuva420p"]

        # Crop to make video divisible
        slide_filters.append("crop=w=2*floor(iw/2):h=2*floor(ih/2)")

        # Pad filter
        if self.scale == "pad" or self.scale == "pan":
            width, height = (
                [self.width, int(self.width / self.output_ratio)]
                if self.ratio > self.output_ratio
                else [int(self.height * self.output_ratio), self.height]
            )
            slide_filters.append(
                f"pad=w={width}:h={height}:x='(ow-iw)/2':y='(oh-ih)/2'"
            )

        # Scale to fit image in output and crop
        if self.scale == "crop_center":
            width, height = (
                [self.output_width, int(self.output_width / self.ratio)]
                if self.ratio < self.output_ratio
                else [int(self.output_height * self.ratio), self.output_height]
            )
            slide_filters.append(f"scale=w={width}:h={height}")

            crop_x = "(iw-ow)/2"
            crop_y = "(ih-oh)/2"
            slide_filters.append(
                "crop=w={}:h={}:x='{}':y='{}'".format(
                    self.output_width, self.output_height, crop_x, crop_y
                )
            )

        # Zoom/pan filter
        try:
            z_step = self.zoom_rate / (self.fps * self.duration)
        except ZeroDivisionError:
            logging.error(
                f"Can't calculate z_step. In denominator: fps: {self.fps} * duration: {self.duration}"
            )

        z_rate = self.zoom_rate
        z_initial = 1
        x = 0
        y = 0
        z = 0
        if self.scale == "pan":
            z_initial = self.ratio / self.output_ratio
            z_step = z_step * self.ratio / self.output_ratio
            z_rate = z_rate * self.ratio / self.output_ratio
            if self.ratio > self.output_ratio:
                if (self.direction_x == "left" and self.direction_z != "out") or (
                    self.direction_x == "right" and self.direction_z == "out"
                ):
                    x = f"(1-on/({self.fps}*{self.duration}))*(iw-iw/zoom)"
                elif (self.direction_x == "right" and self.direction_z != "out") or (
                    self.direction_x == "left" and self.direction_z == "out"
                ):
                    x = f"(on/({self.fps}*{self.duration}))*(iw-iw/zoom)"
                else:
                    x = "(iw-ow)/2"

                y_offset = "(ih-iw/%s)/2" % (self.ratio)

                if self.direction_y == "top":
                    y = y_offset
                elif self.direction_y == "center":
                    y = "{}+iw/{}/2-iw/{}/zoom/2".format(
                        y_offset, self.ratio, self.output_ratio
                    )
                elif self.direction_y == "bottom":
                    y = "{}+iw/{}-iw/{}/zoom".format(
                        y_offset, self.ratio, self.output_ratio
                    )

            else:
                z_initial = self.output_ratio / self.ratio
                z_step = z_step * self.output_ratio / self.ratio
                z_rate = z_rate * self.output_ratio / self.ratio
                x_offset = "(iw-%s*ih)/2" % (self.ratio)

                if self.direction_x == "left":
                    x = x_offset
                elif self.direction_x == "center":
                    x = "{}+ih*{}/2-ih*{}/zoom/2".format(
                        x_offset, self.ratio, self.output_ratio
                    )
                elif self.direction_x == "right":
                    x = "{}+ih*{}-ih*{}/zoom".format(
                        x_offset, self.ratio, self.output_ratio
                    )

                if (self.direction_y == "top" and self.direction_z != "out") or (
                    self.direction_y == "bottom" and self.direction_z == "out"
                ):
                    y = f"(1-on/({self.fps}*{self.duration}))*(ih-ih/zoom)"
                elif (self.direction_y == "bottom" and self.direction_z != "out") or (
                    self.direction_y == "top" and self.direction_z == "out"
                ):
                    y = f"(on/({self.fps}*{self.duration}))*(ih-ih/zoom)"
                else:
                    y = "(ih-oh)/2"

        else:
            if self.direction_x == "left":
                x = 0
            elif self.direction_x == "center":
                x = "iw/2-(iw/zoom/2)"
            elif self.direction_x == "right":
                x = "iw-iw/zoom"

            if self.direction_y == "top":
                y = 0
            elif self.direction_y == "center":
                y = "ih/2-(ih/zoom/2)"
            elif self.direction_y == "bottom":
                y = "ih-ih/zoom"

        # with FFmpeg 4 the zoompan filter variables 'on' starts at 0 (previously started at 1)
        # https://trac.ffmpeg.org/ticket/7242
        start_frame = 1 if self.ffmpeg_version < 4 else 0
        if self.direction_z == "in":
            z = f"if(eq(on,{start_frame}),{z_initial},zoom+{z_step})"
        elif self.direction_z == "out":
            z = "if(eq(on,{}),{},zoom-{})".format(
                start_frame, z_initial + z_rate, z_step
            )
        elif self.direction_z == "none":
            z = "%s" % (z_initial)

        width = 0
        height = 0
        # if self.scale == "crop_center":
        #    if self.output_ratio > self.ratio:
        #        width, height = [self.output_width, int(self.output_width/self.ratio)]
        #    else:
        #        width, height = [int(self.output_height*self.ratio), self.output_height]
        # if self.scale == "pan" or self.scale == "pad":
        width, height = [self.output_width, self.output_height]

        # workaround a float bug in zoompan filter that causes a jitter/shake
        # https://superuser.com/questions/1112617/ffmpeg-smooth-zoompan-with-no-jiggle/1112680#1112680
        # https://trac.ffmpeg.org/ticket/4298
        supersample_width = self.output_width * 4
        supersample_height = self.output_height * 4

        slide_filters.append(
            "scale={}x{},zoompan=z='{}':x='{}':y='{}':fps={}:d={}*{}:s={}x{}".format(
                supersample_width,
                supersample_height,
                z,
                x,
                y,
                self.fps,
                self.fps,
                self.duration,
                width,
                height,
            )
        )

        # return the filters for rendering
        return slide_filters

    def getZoomDirectionX(self):
        return self.direction_x

    def getZoomDirectionY(self):
        return self.direction_y

    def getZoomDirectionZ(self):
        return self.direction_z

    def getObject(self, config):
        object = super().getObject(config)

        if self.slide_duration_min != config["slide_duration_min"]:
            object["slide_duration_min"] = self.slide_duration_min

        if self.zoom_rate != config["zoom_rate"]:
            object["zoom_rate"] = self.zoom_rate

        zoom_direction_x = self.getZoomDirectionX()
        if zoom_direction_x != config["zoom_direction_x"]:
            object["zoom_direction_x"] = zoom_direction_x

        zoom_direction_y = self.getZoomDirectionY()
        if zoom_direction_y != config["zoom_direction_y"]:
            object["zoom_direction_y"] = zoom_direction_y

        zoom_direction_z = self.getZoomDirectionZ()
        if zoom_direction_z != config["zoom_direction_z"]:
            object["zoom_direction_z"] = zoom_direction_z

        if self.scale != config["scale_mode"]:
            object["scale_mode"] = self.scale

        return object
