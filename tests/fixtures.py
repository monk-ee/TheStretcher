#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""fixtures.py: These are fixture functions for returning mocked api data."""

__author__ = "monkee"
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "monk-ee"
__email__ = "magic.monkee.magic@gmail.com"
__status__ = "Development"


def calls():
    return {
        '/nodes': [
            {
                'name': 'host1',
                'deactivated': None,
                'catalog_timestamp': '2013-02-09T21:05:15.663Z',
                'facts_timestamp': '2013-02-09T21:05:15.663Z',
                'report_timestamp': None
            },
            {
                'name': 'host2',
                'deactivated': None,
                'catalog_timestamp': '2013-02-09T21:05:15.663Z',
                'facts_timestamp': '2013-02-09T21:05:15.663Z',
                'report_timestamp': None

            }
        ],
    }
