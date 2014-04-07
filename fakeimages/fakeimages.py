# -*- coding: utf-8 -*-
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

from .base import BaseImage, BaseSettings
from .exceptions import SchemeNotAllowed


class FakeImageSettings(BaseSettings):
    """
    Settings class represents basic settings required to make API calls.
    FakeImage server settings:
        scheme: base scheme of the fake images server
        address: base address of the fake images server
        port: base port of the fake images server
    """

    def __init__(self, scheme='http', address='fakeimg.pl', port='80', *args):
        if scheme not in ['http', 'https']:
            raise SchemeNotAllowed('Fakeimages doesn\'t support protocols except http or https.')
        self.scheme = scheme
        self.address = address
        self.port = port
        self.url = self._construct_url(*args)

    def __repr__(self):
        return 'FakeImageSettings Object <{}>'.format(self.url)


class FakeImage(BaseImage):
    """
    FakeImage class represents the actual image received from server
    """
    __slots__ = ['width', 'text', 'font', 'font_size',
                 'retina', 'height', 'bg_color', 'text_color',
                 'size', 'response', 'settings', 'content']

    def get(self, width=None, height=None, bg_color=None, text_color=None,
            text=None, font=None, font_size=None, retina=False, settings=None):
        """
        Get the image from the fakeimage server.
        The only required parameter to make a call to server is 'width'.
        """
        self.settings = settings or FakeImageSettings()
        self.width = width or self.width
        self.text = text or self.text
        self.font = font or self.font
        self.font_size = font_size or self.font_size
        self.retina = retina or self.retina
        params = {
            'text': self.text,
            'font': self.font,
            'font_size': self.font_size,
            'retina': self.retina or None
        }
        self.height = height or self.height
        if height:
            self.size = '{}x{}'.format(self.width, self.height)
        else:
            self.size = self.width
        self.bg_color = bg_color or self.bg_color
        self.text_color = text_color or self.text_color
        self.response = self._response(params)
        self.content = self.response.content
        return self.response

    def construct_url(self):
        return urlparse.urljoin(
            self.settings.url,
            self.urljoin(self.size, self.bg_color, self.text_color)
        )

    def __repr__(self):
        return 'FakeImage Object <{}>'.format(self.response.url)
