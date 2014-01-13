# -*- coding: utf-8 -*-
import os
import requests

from pytest import raises

from fakeimages import FakeImage, FakeImageSettings, SchemeNotAllowed


class TestFakeImageSettings(object):

    def test_schema_exception(self):
        with raises(SchemeNotAllowed):
            FakeImageSettings(scheme='ftp')

    def test_default_settings(self):
        fakeimages_settings = FakeImageSettings()
        assert fakeimages_settings.url == u'http://fakeimg.pl:80'

    def test_custom_settings(self):
        fakeimages_settings = FakeImageSettings('http', 'google.com', '8080')
        assert fakeimages_settings.url == u'http://google.com:8080'

    def test_internationalized_domain(self):
        fakeimages_settings = FakeImageSettings('http', u'кто.рф', '80')
        assert fakeimages_settings.url == u'http://кто.рф:80'

    def test_settings_repr_default(self):
        fakeimages_settings = FakeImageSettings()
        base_string = u'FakeImageSettings Object <{}>'
        assert fakeimages_settings.__repr__() == base_string.format(fakeimages_settings.url)


class TestFakeImage(object):

    def test_init_without_width(self):
        with raises(TypeError):
            FakeImage()

    def test_wrong_parameters(self):
        with raises(requests.exceptions.HTTPError):
            FakeImage('asdasdasdas')

    def test_init_with_height(self):
        fakeimage = FakeImage(width=300, height=400)
        assert fakeimage.size == '300x400'

    def test_image_save(self):
        fakeimage = FakeImage(width=300, height=400)
        fakeimage.save('test.png')
        assert os.path.isfile('test.png')
        os.remove('test.png')

    def test_fakeimage_repr_default(self):
        fakeimage = FakeImage(300)
        base_string = u'FakeImage Object <{}>'
        assert fakeimage.__repr__() == base_string.format(fakeimage.response.url)
