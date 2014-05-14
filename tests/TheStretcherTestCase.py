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
import os
from TheStretcher import TheStretcher


class TheStretcherTestCase(unittest.TestCase):
    def setUp(self):
        self._client = TheStretcher()

    def tearDown(self):
        pass

    def test_check_timezone_set(self):
        ts = TheStretcher()
        self.assertIn("TZ",os.environ)

        def test_check_timezone_value(self):
        ts = TheStretcher()
        self.assertEqual(os.environ["TZ"],"Australia/Brisbane")

    def test_check_timezone_notset(self):
        self.assertNotIn("TZ",os.environ)

    def test_stop_instance(self):
        ts = TheStretcher()
        self.assertRaises(Exception,ts.stop_instance)

    def test_start_instance(self):
        ts = TheStretcher
        self.assertRaises(Exception,ts.start_instance)

