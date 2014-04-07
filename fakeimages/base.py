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
__version__ = '0.2'
__build__ = 0x0002
__author__ = 'Lev Rubel'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2013 Lev Rubel'

import abc
import requests
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

try:
    from StringIO import StringIO
except ImportError:
    from io import BytesIO as StringIO

from PIL import Image
from six.moves import xrange


class BaseSettings(object):

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


class BaseImage(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, width, settings=None, *args, **kwargs):
        for slot in self.__slots__:
            setattr(self, slot, None)
        self.width = width
        self.response = self.get(width, *args, **kwargs)

    def urljoin(self, *args):
        """
        Joins given arguments into a url.
        Trailing but not leading slashes are stripped for each argument.
        """
        return '/'.join(str(s).strip('/') for s in args if s)

    def _response(self, params):
        http_error_msg = 'Can\'t get such image from server: Status code is {}'
        response = requests.get(self.construct_url(), params=params)
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
        return Image.open(StringIO(self.content)).save(path, format)

    def get(self, width):
        raise NotImplementedError

    def construct_url(self):
        raise NotImplementedError
