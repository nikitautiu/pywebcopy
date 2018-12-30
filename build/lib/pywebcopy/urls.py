# -*- coding: utf-8 -*-

"""
pywebcopy.urls
~~~~~~~~~~~~~~

Deals with different types of urls in pywebcopy.parsers.

"""

<<<<<<< HEAD
import os.path
import re
import hashlib
from uuid import uuid4
from mimetypes import guess_extension
try:
    from urlparse import urlsplit, urljoin
    from urllib import url2pathname, pathname2url
except ImportError:
    from urllib.request import url2pathname, pathname2url
    from urllib.parse import urlsplit, urljoin
from pywebcopy.exceptions import InvalidUrlError
from pywebcopy.config import config
from pywebcopy import LOGGER


FILENAME_CLEANER = re.compile(r'[*":<>|?]+?\.\.?[/|\\]+')
URL_CLEANER = re.compile(r'[*"<>|]?\.\.?[/|\\]+')


def filename_present(url):
    """Checks whether a filename is present in the url/path or not."""
=======
__all__ = [
    'filename_present', 'url2path', 'relate',
    'URLTransformer',
]

import os
import re
import hashlib

from six.moves.urllib.request import url2pathname
from six.moves.urllib.parse import urljoin, unquote, urldefrag, urlsplit

from . import LOGGER


# Removes the non-fileSystem compatible letters or patterns from a file path
FILENAME_CLEANER = re.compile(r'[*":<>|?]+?\.\.?[/|\\]+')

# Cleans query params or fragments from url to make it look like a path
URL_CLEANER = re.compile(r'[*"<>|]?\.\.?[/|\\]+(?:[#]\S+)')

# Matches any special character like #, : etc.
SPECIAL_CHARS = re.compile(r'(?:[\*\"\<\>\|\!\$\&\:\<\>\|\?])+?')  # any unwanted char

# Matches any fragment or query data in url
URL_FRAG = re.compile(r'(?:[#?;=]\S+)?')  # query strings

# Matches any relative path declaration i.e. '../', './' etc.
RELATIVE_PATHS = re.compile(r'(?:\.+/+)+?')  # relative paths


def filename_present(url):
    """Checks whether a `filename` is present in the url/path or not.

    :param str url: url string to check the file name in.
    :return boolean: True if present, else False
    """
>>>>>>> v5.0.0

    if not url:
        return False
    if url.startswith(u'#'):
        return False

    url_obj = urlsplit(url)
<<<<<<< HEAD
    path = url_obj.path.strip('/')

    if url_obj.hostname == u'data' or not path:
        return False

    _possible_name = path.rsplit('/', 1)[-1]

    if not _possible_name or _possible_name.find('.') < 0:
        return False

    if len(_possible_name.rsplit('.', 1)[1]) < 1:
=======
    url = url_obj.path
    if url_obj.hostname == u'data' or not url:
        return False

    i = len(url)
    while i and url[i - 1] not in '/\\':
        i -= 1
    fn = url[i:]

    if fn.strip() == '':
        return False
    if i == 0:
>>>>>>> v5.0.0
        return False

    return True


def url2path(url, base_url=None, base_path=None, default_filename=None):
    """Converts urls to disk style file paths. """

    if not url:
        return

    if base_url:
        url = urljoin(base_url or '', url)

    if not filename_present(url):
<<<<<<< HEAD
        url = urljoin(url, default_filename or str(uuid4())[:10] + '.download')
    
=======
        url = urljoin(url, default_filename)

>>>>>>> v5.0.0
    url_obj = urlsplit(url)

    if url_obj.hostname == 'data':
        return

<<<<<<< HEAD
    url = "%s%s" % (url_obj.hostname or '', url_obj.path or '')
=======
    url = "%s%s" % (url_obj.hostname, url_obj.path)
>>>>>>> v5.0.0
    
    if not url:
        return

    path = FILENAME_CLEANER.sub('_', url)
    
    if base_path:
        path = os.path.join(base_path or '', path)

    return path


<<<<<<< HEAD
class Url(object):
    """Provides several operations on a url. """

    def __init__(self, url):

        if not url:
            raise InvalidUrlError("Url is invalid %s" % url)

        self._unique_fn_required = config['unique_filenames']
        self.original_url = url
        self.default_filename = self.hash() + (guess_extension(url) or '.download')
        self.url = url
        self._base_url = ''
        self._base_path = ''
=======
class URLTransformer:
    """Transforms url into various types and subsections.

    :param str url: a url to perform transform operations on
    :param str base_url: parent url of the given url, if any.
    :param str base_path: absolute path to be added to new paths generated.
    :param str default_fn: filename to use when there is no filename present in url
    """

    def __init__(self, url, base_url=None, base_path=None, default_fn=None):

        self.original_url = url
        self._url = None
        self._parsed = None
        self._base_url = base_url
        self._base_path = base_path

        if default_fn:
            self.default_filename = default_fn
        else:
            self.default_filename = "%d.pwcf" % (hash(self))

        LOGGER.debug('URLTransformer {} has been set to self.base_url {} '
                     'and self.url is {}'.format(self, self.base_url, self.url))

        # special tweaks for url to path conversion
        self.default_fileext = '.pwcf'
        self.check_fileext = False
>>>>>>> v5.0.0

    def __str__(self):
        return self.url

    def __repr__(self):
<<<<<<< HEAD
        return "<Url({})>".format(self.original_url)

    def hash(self):
        return str(int(hashlib.sha1(self.original_url.encode('utf-8')).hexdigest(), 16) % (10 ** 8))
=======
        return "<URLTransformer({})>".format(self.original_url)

    def __hash__(self):
        """8 chars long hash of url for unique identity.
        :rtype: int
        :return: hash of the url
        """
        return int(hashlib.sha1(self.original_url.encode('utf-8')).hexdigest(), 16) % (10 ** 8)

    @property
    def url(self):
        """Final url generated after any base_url or original change actions.
        :rtype: str
        :return: url calculated using all the factors
        """

        if self.base_url:
            new_url = urljoin(self.base_url, self.original_url)
        else:
            new_url = self.original_url
        return RELATIVE_PATHS.sub('', unquote(new_url))

    @staticmethod
    def clean_url(url):
        """Cleans any url of relative paths remaining after urljoins.

        :param url: any url containing relative path contaimination
        :type url: str
        :rtype: str
        :returns: cleaned url

        Example:
            clean_url('http://google.com/../../url/path/#frag') => 'http://google.com/url/path/'
            clean_url('../../url/path') => '/url/path'
            clean_url('./same/dir/') => 'same/dir/'

        """
        return RELATIVE_PATHS.sub('', unquote(urldefrag(url)[0]))

    @staticmethod
    def clean_fn(file_path):
        """Removes any unwanted patterns or characters from filepath."""

        file_path = SPECIAL_CHARS.sub('', file_path)         # any unwanted char
        file_path = URL_FRAG.sub('', file_path)              # query strings
        file_path = RELATIVE_PATHS.sub('', file_path)        # relative paths

        return file_path
>>>>>>> v5.0.0

    @property
    def parsed_url(self):
        """Parses the url in six part tuple."""
<<<<<<< HEAD
        return urlsplit(self.url, allow_fragments=False)
=======
        if not self._parsed:
            self._parsed = urlsplit(self.clean_url(self.url))
        return self._parsed
>>>>>>> v5.0.0

    @property
    def hostname(self):
        return self.parsed_url.hostname

    @property
    def port(self):
<<<<<<< HEAD
=======
        """:rtype: int"""
>>>>>>> v5.0.0
        return self.parsed_url.port

    @property
    def url_path(self):
<<<<<<< HEAD
        return self.parsed_url.path.split('#', 1)[0]
=======
        return self.parsed_url.path
>>>>>>> v5.0.0

    @property
    def scheme(self):
        return self.parsed_url.scheme

<<<<<<< HEAD
    def _join_with(self, other_url):
        """Joins this url with new url. """
        return urljoin(other_url or '', self.url)

    @property
    def base_url(self):
        """Returns the base url this url if set."""
        if self._base_url:
            return self._base_url
        return ''

    @base_url.setter
    def base_url(self, base_url):
        """Converts self.url to join result of self.url and provided base_url"""
        self._base_url = base_url or ''
        self.url = URL_CLEANER.sub('', self._join_with(self.base_url or ''))
        LOGGER.debug('Base url of Url obj %s is now set to %s now self.url is %s' % (self, self.base_url, self.url))

    @property
    def base_path(self):
        """Returns the base path if set."""
        if self._base_path:
            return self._base_path
        return ''

    @base_path.setter
    def base_path(self, base_path):
        """Sets a base for the return value of file_path() function."""
        self._base_path = base_path or ''

    @property
    def to_path(self):
        """Returns a file path made from url."""
        if self.base_path:
            return os.path.join(self.base_path, url2pathname(self.hostname + self.url_path))
        return url2pathname(self.hostname + self.url_path)

    @property
    def file_name(self):
        """Returns a file name from url url_path."""
        # Web pages can be displayed without any file name So a default
        # file name is required in case.

        if not filename_present(self.url):
            return self.default_filename
        else:
            return os.path.split(self.to_path)[-1]

    @property
    def file_path(self):
        """Returns a path with filename if not already present in the url to store the Content. """

        # Either of the filename or default_filename needs to be present

        if not self.file_name:
            raise InvalidUrlError("File name is not present in url %s" % self.url)

        # default path generated for the url by the function
        _path = FILENAME_CLEANER.sub('', self.to_path)

        # If the default file name is used then it is not definitely
        # present in the url and hence to be joined to the _path
        if not _path.endswith(self.file_name):
            if self._unique_fn_required:
                path = os.path.join(_path, self.hash() + "__" + self.file_name)
            else:
                path = os.path.join(_path, self.file_name)
        else:
            if self._unique_fn_required:
                path = _path.replace(self.file_name, os.path.join(self.hash() + "___" + self.file_name))
            else:
                path = _path

        LOGGER.debug("Url obj for %s generated file path %s" % (self, path))

        return path
=======
    @property
    def base_url(self):
        """Absolute url this url if set.
        :rtype: str
        """
        return self._base_url

    @base_url.setter
    def base_url(self, new_base):
        """Set the parent url of this object to new new_base.

        :param str new_base: absolute url of the domain
        :rtype: None
        """
        self._base_url = new_base
        # reset
        self._url = None
        self._parsed = None

    @property
    def base_path(self):
        """Returns the base path if set.
        :rtype: str
        """
        return self._base_path

    @base_path.setter
    def base_path(self, new_base_path):
        """Base file which would be prepended to the new path generated via url."""
        self._base_path = new_base_path or ''

    @property
    def to_path(self):
        """Returns a file path made from url.

        :rtype: str
        :returns: path assumed from url
        """
        if self.base_path:
            return os.path.join(self.base_path, self._path_from_url())
        return self._path_from_url()

    def _path_from_url(self):
        """Returns a feasable path extracted from the url converted to disk style convention."""
        return url2pathname(self.clean_fn(self.hostname + self.url_path))

    @property
    def file_name(self):
        """Returns a file name from url url_path.
        # Web pages can be displayed without any file name So a default
        # file name is required in case.
        :rtype: str
        :return: filename present in the url or default one
        """
        fn, pos = self.get_filename_and_pos(self.url_path)

        if not fn:
            return self.default_filename
        else:
            return fn

    @staticmethod
    def insert(string, new_object, index):
        """Inserts a new string at specified index in the basestring

        :param string: base string in which new fragment to be inserted
        :type string: str
        :param new_object: new fragment
        :type new_object: str
        :param index: position at which the fragment will be inserted in basestring
        :type index: int
        :return: new extended string
        :rtype: str
        """
        return string[index:] + new_object + string[:index]

    def get_filename_and_pos(self, path):
        """Finds the filename in a url and returns a tuple containing filename and position.

        :type path: str
        :param path: path in which to find the filename
        :rtype: tuple
        :return: two-tuple containing filename name its start position
        """

        fn = self.clean_fn(path)

        i = len(fn)    # pointer to the end of string
        # iter until first slash found and stop before it
        while i and fn[i-1] not in '/\\':
            i -= 1
        fn = fn[i:]    # string slice present after the slash
        return fn, i

    def get_fileext_and_pos(self, path):
        """Finds the file extension in a url and returns a tuple containing extension and position.

        :type path: str
        :param path: path in which to find the extension
        :rtype: tuple
        :return: two-tuple containing filename name its start position
        """
        fn, _ = self.get_filename_and_pos(path)

        i = len(fn)  # pointer to the end of string
        # iter until first slash found and stop before it
        while i and fn[i - 1] != '.':
            i -= 1

        # no extension present
        if i == 0:
            return '', 0

        fe = fn[i:]
        return fe, len(path) - len(fn) + i

    def _refactor_filename(self, path):
        """Refactors a filename in a path and modifies it according to need.

        NOTE : internal use only
        NOTE : specially designed for webpages and not files


        :param path: path from which the filename to be extracted
        :return: two-tuple containing refactored filename and its start position
        """
        fn, pos = self.get_filename_and_pos(path)

        if fn:
            new_fn = str(hash(self)) + '__' + fn

        else:
            new_fn = self.default_filename

        if pos == 0:  # a slash does not exists in path
            new_fn = '/' + new_fn

        # make sure the files extension becomes required type
        if self.check_fileext:
            fe, ext_pos = self.get_fileext_and_pos(new_fn)

            if ext_pos == 0:
                new_fn += '.' + self.default_fileext
            else:
                new_fn = new_fn[:ext_pos] + self.default_fileext

        # replace original filename with unique filename inplace of
        return path[:pos] + new_fn, pos

    @property
    def file_path(self):
        """Make a unique path from the url.

        :rtype: str
        :return: disk compatible path
        """
        upath, _ = self._refactor_filename(self.url_path)

        # clean the url and prepend hostname to make it complete
        upath = url2pathname(self.hostname + upath)

        if self.base_path:
            upath = os.path.join(self.base_path, upath)
        return upath


def relate(target_file, start_file):
    """ Returns relative path of target-file from start-file. """

    # Default os.path.relpath takes directories as argument, thus we need strip the filename
    # if present in the path else continue as is.
    target_dir = os.path.dirname(target_file)
    start_dir = os.path.dirname(start_file)

    # Calculate the relative path using the standard module and then concatenate the file names if
    # they were previously present.
    return os.path.join(os.path.relpath(target_dir, start_dir), os.path.basename(target_file))
>>>>>>> v5.0.0