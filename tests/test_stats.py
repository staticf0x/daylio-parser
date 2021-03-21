# -*- coding: utf-8 -*-
"""
Test stats.py
"""

import datetime
import pathlib
from unittest import TestCase, skip

import numpy as np

from daylio_parser.parser import Entry, Parser
from daylio_parser.stats import Stats


class TestStats(TestCase):
    def setUp(self):
        """
        Load the test CSV for all test methods.
        """

        here = pathlib.Path(__file__).parent.resolve()

        parser = Parser()
        self.entries = parser.load_csv(here/'data'/'test_data.csv')
        self.stats = Stats(self.entries)

    def test_average_moods(self):
        """
        Test computing average moods (day by day) from the CSV.
        """

        avg_moods = self.stats.average_moods()

        expected = [
            (datetime.date(2020, 5, 25), 2.0),
            (datetime.date(2020, 5, 27), 4.3),
            (datetime.date(2020, 5, 28), 4.6),
            (datetime.date(2020, 5, 29), 5.0),
            (datetime.date(2020, 5, 30), 5.0),
        ]

        self.assertEqual(avg_moods, expected)

    def test_activity_moods(self):
        """
        Test mood averages for each activity.
        """

        moods = self.stats.activity_moods()

        self.assertAlmostEqual(moods['work'][0], 4.0, 0)
        self.assertAlmostEqual(moods['work'][1], 0.89, 2)

        self.assertAlmostEqual(moods['programming'][0], 5.0, 0)
        self.assertAlmostEqual(moods['programming'][1], 0, 0)

    @skip('TODO: test this method')
    def test_split_into_bands(self):
        split_data = self.stats.split_into_bands()

    @skip('TODO: implement Stats.stability')
    def test_stability(self):
        """
        Test stability on some real world data.
        """

        self.assertEqual(self.stats.stability([3]), 100)
        self.assertEqual(self.stats.stability([4, 3, 4, 2, 3, 2, 4, 3]), 68)
        self.assertEqual(self.stats.stability([4, 3, 4, 2, 3, 2, 4, 3, 4, 4, 4]), 81)
