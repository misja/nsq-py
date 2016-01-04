#! /usr/bin/env python
import sys
from nsq2 import __version__

extra = {}

from setuptools import setup
if sys.version_info >= (3,):
    extra['use_2to3'] = True


setup(name               = 'nsq2-py',
    version              = __version__,
    description          = 'NSQ for Python With Pure Sockets',
    url                  = 'http://github.com/dlecocq/nsq-py',
    author               = 'Dan Lecocq',
    author_email         = 'dan@moz.com',
    license              = "MIT License",
    keywords             = 'nsq, queue',
    packages             = ['nsq2', 'nsq2.http', 'nsq2.sockets'],
    package_dir          = {'nsq2': 'nsq2', 'nsq2.http': 'nsq2/http', 'nsq2.sockets': 'nsq2/sockets'},
    classifiers          = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent'
    ],
    install_requires=[
        'requests'
    ],
    **extra
)
