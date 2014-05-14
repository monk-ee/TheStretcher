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

class test_args(object):
    instance = "i-7244af4c"
    disk_partition = "/dev/sdb"
    disk_size = 100
    restart = True
    cleanup = True
    iops = 100
    dryrun = True

    # The class "constructor" - It's actually an initializer
    def __init__(self):
        pass

class TheStretcherTestCase(unittest.TestCase):
    def setUp(self):
        args = test_args()
        self._client = TheStretcher(args)

    def tearDown(self):
        pass

    def test_check_timezone_value(self):
        self.assertEqual(os.environ["TZ"], "Australia/Brisbane")

    def test_stop_instance(self):
        self.assertRaises(Exception, self._client.stop_instance)

    def test_start_instance(self):
        ts = TheStretcher
        self.assertRaises(Exception,self._client.start_instance)

