#!/usr/bin/env python
import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = '0.0.1'
setup(
    name='TheStretcher',
    version=version,
    description='A utility for stretching ec2 volumes with minimal effortB',
    url='http://github.com/monk-ee/TheStretcher',
    download_url=('https://github.com/monk-ee'
                  'TheStretcher/archive/%s.tar.gz' % version),
    author='monk-ee',
    author_email='magic.monkee.magic@gmail.com',
    keywords=['aws', 'ec2','ebs'],
    license='GNU GPL v3.0',
    packages=['TheStretcher'],
    install_requires = [ 'boto' ],
    test_suite='tests.all_tests',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU GPL v3.0',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        ]
)
