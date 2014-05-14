from unittest import TestCase
from TheStretcher import TheStretcher
import os

__author__ = 'monkee'
__project__ = 'TheStretcher'


class TestTheStretcher(TestCase):

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

