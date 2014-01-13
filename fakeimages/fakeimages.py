# -*- coding: utf-8 -*-

"""
|  ______   ______     __  __     ______                               |
| /\  ___\ /\  __ \   /\ \/ /    /\  ___\                              |
| \ \  __\ \ \  __ \  \ \  _"-.  \ \  __\                              |
|  \ \_\    \ \_\ \_\  \ \_\ \_\  \ \_____\                            |
|   \/_/     \/_/\/_/   \/_/\/_/   \/_____/                            |
|                                                                      |
|       __     __    __     ______     ______     ______     ______    |
|      /\ \   /\ "-./  \   /\  __ \   /\  ___\   /\  ___\   /\  ___\   |
|      \ \ \  \ \ \-./\ \  \ \  __ \  \ \ \__ \  \ \  __\   \ \___  \  |
|       \ \_\  \ \_\ \ \_\  \ \_\ \_\  \ \_____\  \ \_____\  \/\_____\ |
|        \/_/   \/_/  \/_/   \/_/\/_/   \/_____/   \/_____/   \/_____/ |

"""

__title__ = 'fakeimages'
__version__ = '0.1'
__build__ = 0x01
__author__ = 'Lev Rubel'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2013 Lev Rubel'

import urlparse
import requests

from StringIO import StringIO
from PIL import Image


class SchemeNotAllowed(Exception):
    pass


class FakeImageSettings(object):
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

    def _construct_url(self, *args):
        """
        *Should not be called directly*
        Construct full url from protocol, address and port.
        Netloc string is unicode wrapped to ensure internationalized domain
        names are processed correctly.
        The urlunparse function argument takes only six-item iterable,
        so we need to add necessary amount of empty elements.
        """
        netloc = u'{}:{}'.format(self.address, self.port)
        base_params = [self.scheme, netloc]
        optional_params = list(args) + list('' for _ in xrange(4 - len(args)))
        return urlparse.urlunparse(base_params + optional_params)

    def __repr__(self):
        return 'FakeImageSettings Object <{}>'.format(self.url)


class FakeImage(object):
    """
    FakeImage class represents the actual image received from server
    """
    __slots__ = ['width', 'text', 'font', 'font_size', 'retina', 'height', 'bg_color', 'text_color', 'size', 'response', 'settings', 'content']

    def __init__(self, width, settings=None, *args, **kwargs):
        for slot in self.__slots__:
            setattr(self, slot, None)
        self.settings = settings or FakeImageSettings()
        self.width = width
        self.response = self.get(width, *args, **kwargs)

    def get(self, width=None, height=None, bg_color=None, text_color=None,
            text=None, font=None, font_size=None, retina=False):
        """
        Get the image from the fakeimage server.
        The only required parameter to make a call to server is 'width'.
        """
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

    def urljoin(self, *args):
        """
        Joins given arguments into a url.
        Trailing but not leading slashes are stripped for each argument.
        """
        return '/'.join(str(s).strip('/') for s in args if s)

    def _construct_url(self):
        return urlparse.urljoin(
            self.settings.url,
            self.urljoin(self.size, self.bg_color, self.text_color)
        )

    def _response(self, params):
        http_error_msg = 'Can\'t get such image from server: Status code is {}'
        response = requests.get(self._construct_url(), params=params)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as exception:
            raise requests.exceptions.HTTPError(
                http_error_msg.format(exception.response.status_code))
        return response

    def save(self, path, format=None):
        """
        Saves response file with the following settings:
            path: path to the file, where to save the image
            format: format of output image file (i.e. 'png', 'jpg', 'gif', etc.)
        """
        return Image.open(StringIO(self.response.content)).save(path, format)

    def __repr__(self):
        return 'FakeImage Object <{}>'.format(self.response.url)
