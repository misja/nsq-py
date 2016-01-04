'''Our clients for interacting with various clients'''


import requests
from functools import wraps
from .. import json, logger
from ..exceptions import NSQException


def wrap(function):
    '''Wrap a function that returns a request with some exception handling'''
    @wraps(function)
    def inner(*args, **kwargs):
        try:
            req = function(*args, **kwargs)
            logger.debug('Got %s: %s', req.status_code, req.content)
            if req.status_code == 200:
                return req
            else:
                raise ClientException(req.reason, req.content)
        except ClientException:
            raise
        except Exception as exc:
            raise ClientException(exc)
    return inner


def json_wrap(function):
    '''Return the json content of a function that returns a request'''
    @wraps(function)
    def inner(*args, **kwargs):
        try:
            # Some responses have data = None, but they generally signal a
            # successful API call as well.
            return json.loads(function(*args, **kwargs).content)['data'] or True
        except Exception as exc:
            raise ClientException(exc)
    return inner


def ok_check(function, *args, **kwargs):
    '''Ensure that the response body is OK'''
    @wraps(function)
    def inner(*args, **kwargs):
        req = function(*args, **kwargs)
        if req.content.lower() != 'ok':
            raise ClientException(req.content)
        return req.content
    return inner


class ClientException(NSQException):
    '''An exception class for all client errors'''


class BaseClient(object):
    '''Base client class'''
    def __init__(self, target, **params):
        if isinstance(target, basestring):
            self._host = target
        elif isinstance(target, (tuple, list)):
            self._host = url.parse('http://%s:%s/' % target)
        else:
            raise TypeError('Host must be a string or tuple')
        self._params = params

    @wrap
    def get(self, path, *args, **kwargs):
        '''GET the provided endpoint'''
        target = self._host.relative(path).utf8()
        params = kwargs.get('params', {})
        params.update(self._params)
        kwargs['params'] = params
        logger.debug('GET %s with %s, %s', target, args, kwargs)
        return requests.get(target, *args, **kwargs)

    @wrap
    def post(self, path, *args, **kwargs):
        '''POST to the provided endpoint'''
        target = self._host.relative(path).utf8()
        params = kwargs.get('params', {})
        params.update(self._params)
        kwargs['params'] = params
        logger.debug('POST %s with %s, %s', target, args, kwargs)
        return requests.post(target, *args, **kwargs)
