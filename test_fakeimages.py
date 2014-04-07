# -*- coding: utf-8 -*-
import os
import requests

from pytest import raises

from fakeimages.base import BaseImage
from fakeimages.exceptions import SchemeNotAllowed
from fakeimages.fakeimages import FakeImage, FakeImageSettings
from fakeimages.lorempixel import Lorempixel, LorempixelSettings


class TestBaseImageAbstract(object):

    def test_get_not_implemented(self):
        with raises(NotImplementedError):
            NewClass = type('NewClass', (BaseImage,), {'__slots__': ['width']})
            NewClass(300).get()

    def test_construct_url_not_implemented(self):
        def get(self, width):
            return width
        with raises(NotImplementedError):
            NewClass = type('NewClass', (BaseImage,), {'__slots__': ['width'], 'get': get})
            NewClass(300).construct_url()


class TestLorempixelSettings(object):

    def test_schema_exception(self):
        with raises(SchemeNotAllowed):
            LorempixelSettings(scheme='ftp')

    def test_default_settings(self):
        lorempixel_settings = LorempixelSettings()
        assert lorempixel_settings.url == u'http://lorempixel.com:80'

    def test_custom_settings(self):
        lorempixel_settings = LorempixelSettings('http', 'google.com', '8080')
        assert lorempixel_settings.url == u'http://google.com:8080'

    def test_internationalized_domain(self):
        lorempixel_settings = LorempixelSettings('http', u'кто.рф', '80')
        assert lorempixel_settings.url == u'http://кто.рф:80'

    def test_settings_repr_default(self):
        lorempixel_settings = LorempixelSettings()
        base_string = u'LorempixelSettings Object <{}>'
        assert lorempixel_settings.__repr__() == base_string.format(lorempixel_settings.url)

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


class TestLorempixel(object):

    def test_init_without_width(self):
        with raises(TypeError):
            Lorempixel()

    def test_wrong_parameters(self):
        with raises(requests.exceptions.HTTPError):
            Lorempixel('asdasdasdas')

    def test_init_with_grey(self):
        width, height = 300, 400
        lorempixel = Lorempixel(width=width, height=height, grey=True)
        assert lorempixel.construct_url() == '{}/g/{}/{}'.format(lorempixel.settings.url, width, height)

    def test_image_save(self):
        lorempixel = Lorempixel(width=300, height=400)
        lorempixel.save('test.png')
        assert os.path.isfile('test.png')
        os.remove('test.png')

    def test_lorempixel_repr_default(self):
        lorempixel = Lorempixel(300)
        base_string = u'Lorempixel Object <{}>'
        assert lorempixel.__repr__() == base_string.format(lorempixel.response.url)


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
