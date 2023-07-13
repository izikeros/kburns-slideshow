class TestImageSlide:
    def test_init(self, image_slide, image_slide_config):
        assert image_slide.duration == image_slide_config["duration"]
        assert image_slide.fade_duration == image_slide_config["fade_duration"]
        assert image_slide.direction_x in ["left", "right"]
        assert image_slide.direction_y in ["top", "bottom"]
        assert image_slide.direction_z in ["in", "out"]

    def test_set_scale_mode(self, image_slide):
        image_slide.setScaleMode("pad")
        assert image_slide.scale == "pad"
        image_slide.setScaleMode("crop_center")
        assert image_slide.scale == "crop_center"

    def test_set_zoom_direction_x(self, image_slide):
        image_slide.setZoomDirectionX("left")
        assert image_slide.direction_x == "left"
        image_slide.setZoomDirectionX("right")
        assert image_slide.direction_x == "right"

    def test_set_zoom_direction_y(self, image_slide):
        image_slide.setZoomDirectionY("top")
        assert image_slide.direction_y == "top"
        image_slide.setZoomDirectionY("bottom")
        assert image_slide.direction_y == "bottom"

    def test_set_zoom_direction_z(self, image_slide):
        image_slide.setZoomDirectionZ("in")
        assert image_slide.direction_z == "in"
        image_slide.setZoomDirectionZ("out")
        assert image_slide.direction_z == "out"

    def test_get_filter(self, image_slide):
        slide_filters = image_slide.getFilter()
        assert isinstance(slide_filters, list)
        assert len(slide_filters) > 0

    def test_get_zoom_direction_x(self, image_slide):
        direction_x = image_slide.getZoomDirectionX()
        assert direction_x in ["left", "right"]

    def test_get_zoom_direction_y(self, image_slide):
        direction_y = image_slide.getZoomDirectionY()
        assert direction_y in ["top", "bottom"]

    def test_get_zoom_direction_z(self, image_slide):
        direction_z = image_slide.getZoomDirectionZ()
        assert direction_z in ["in", "out"]

    def test_get_object(self, image_slide, image_slide_config):
        config = image_slide.getObject(image_slide_config)
        assert isinstance(config, dict)
        # assert "slide_duration_min" in config
        # assert "zoom_rate" in config
        assert "zoom_direction_x" in config
        assert "zoom_direction_y" in config
        assert "zoom_direction_z" in config
        assert "scale_mode" in config
