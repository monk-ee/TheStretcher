#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""helpers.py: These are helper mock functions for testing this module."""

__author__ = "monkee"
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "monk-ee"
__email__ = "magic.monkee.magic@gmail.com"
__status__ = "Development"

from mock import Mock
import fixtures
import json

def mock_api_request(host_url=None, path=None, *args, **kwargs):
    resp = Mock()
    data = fixtures.calls().get(path)
    resp.content = json.dumps(data)
    resp.headers = kwargs.get('headers')
    return resp
