# -*- coding: utf-8 -*-
"""
Test stats.py
"""

import datetime
import pathlib
from unittest import TestCase

from daylio_parser.parser import Entry, Parser
from daylio_parser.stats import average_moods, activity_moods


class TestParser(TestCase):
    def setUp(self):
        here = pathlib.Path(__file__).parent.resolve()

        parser = Parser()
        self.entries = parser.load_csv(here/'data'/'test_data.csv')

    def test_average_moods(self):
        avg_moods = average_moods(self.entries)

        expected = [
            (datetime.date(2020, 5, 25), 2.0),
            (datetime.date(2020, 5, 27), 4.3),
            (datetime.date(2020, 5, 28), 4.6),
            (datetime.date(2020, 5, 29), 5.0),
            (datetime.date(2020, 5, 30), 5.0),
        ]

        self.assertEqual(avg_moods, expected)

    def test_activity_moods(self):
        moods = activity_moods(self.entries)

        self.assertAlmostEqual(moods['work'][0], 4.0, 0)
        self.assertAlmostEqual(moods['work'][1], 0.89, 2)

        self.assertAlmostEqual(moods['programming'][0], 5.0, 0)
        self.assertAlmostEqual(moods['programming'][1], 0, 0)
