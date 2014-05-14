#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""TheStretcherTestCase.py: A bunch of unittests for testing this module."""

__author__ = "monkee"
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "monk-ee"
__email__ = "magic.monkee.magic@gmail.com"
__status__ = "Development"


import unittest
from mock import MagicMock, patch
import requests
from TheStretcher import TheStretcher
import json
import helpers


class TheStretcherTestCase(unittest.TestCase):
    def setUp(self):
        self._client = TheStretcher()

    def tearDown(self):
        pass

    @patch('puppetdb.utils.api_request')
    def test_get_nodes(self, get):
        get.side_effect = helpers.mock_api_request
        resp = self._client.get_nodes()
        self.assertEqual(len(resp), 2)
        node_0 = resp[0]
        self.assertTrue(node_0.has_key('name'))
        self.assertEqual(node_0.get('name'), 'host1')
        node_1 = resp[1]
        self.assertTrue(node_1.has_key('name'))
        self.assertEqual(node_1.get('name'), 'host2')

