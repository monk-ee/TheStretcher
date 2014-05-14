#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""__init__.py: Init for unit testing this module."""

__author__ = "monkee"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "monk-ee"
__email__ = "magic.monkee.magic@gmail.com"
__status__ = "Development"

import unittest

from TheStretcherTestCase import PuppetDBClientTestCaseV2
from PuppetDBClientTestCaseV3 import PuppetDBClientTestCaseV3


def all_tests():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(PuppetDBClientTestCaseV2))
    suite.addTest(unittest.makeSuite(PuppetDBClientTestCaseV3))
    return suite
