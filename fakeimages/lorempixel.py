# -*- coding: utf-8 -*-
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

from .base import BaseImage, BaseSettings
from .exceptions import SchemeNotAllowed


class LorempixelSettings(BaseSettings):
    """
    Settings class represents basic settings required to make API calls.
    Lorempixel server settings:
        scheme: base scheme of the fake images server
        address: base address of the fake images server
        port: base port of the fake images server
    """

    def __init__(self, scheme='http', address='lorempixel.com', port='80', *args):
        if scheme not in ['http', 'https']:
            raise SchemeNotAllowed('Lorempixel doesn\'t support protocols except http or https.')
        self.scheme = scheme
        self.address = address
        self.port = port
        self.url = self._construct_url(*args)

    def __repr__(self):
        return 'LorempixelSettings Object <{}>'.format(self.url)


class Lorempixel(BaseImage):
    """
    Lorempixel class represents the actual image recieved from server
    """
    __slots__ = ['width', 'text', 'category', 'grey', 'number',
                 'height', 'response', 'content', 'url']

    def get(self, width=None, height=None, category=None,
            grey=False, number=None, text=None, settings=None):
        """
        Get the image from the lorempixel server.
        The only required parameter to make a call to server is 'width'.
        Height is required by lorempixel but if it's missing it'll return square image.
        """
        self.settings = settings or LorempixelSettings()
        self.width = width or self.width
        self.text = text or self.text
        self.category = category or self.category
        self.grey = grey or self.grey
        self.number = number or self.number
        self.height = height or width
        self.response = self._response(None)
        self.content = self.response.content
        return self.response

    def construct_url(self):
        grey = None
        if self.grey:
            grey = 'g'
        return urlparse.urljoin(
            self.settings.url,
            self.urljoin(grey, self.width, self.height, self.category, self.number, self.text)
        )

    def __repr__(self):
        return 'Lorempixel Object <{}>'.format(self.response.url)
