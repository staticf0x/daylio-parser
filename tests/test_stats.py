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
    # TODO: Test low/high periods -- need more data for that

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

    def test_mean(self):
        mean, std = self.stats.mean()

        self.assertAlmostEqual(mean, 4.15625, 5)
        self.assertAlmostEqual(std, 1.2275, 4)

    @skip('TODO: implement Stats.stability')
    def test_stability(self):
        """
        Test stability on some real world data.
        """

        self.assertEqual(self.stats.stability([3]), 100)
        self.assertEqual(self.stats.stability([4, 3, 4, 2, 3, 2, 4, 3]), 68)
        self.assertEqual(self.stats.stability([4, 3, 4, 2, 3, 2, 4, 3, 4, 4, 4]), 81)

    def test_rolling_mean_2(self):
        """
        Test rolling mean of data for N=2
        """

        data = self.stats.rolling_mean(2)

        expected_data = [
            (datetime.date(2020, 5, 25), np.nan),
            # Missing day in CSV
            (datetime.date(2020, 5, 27), 3.15),
            (datetime.date(2020, 5, 28), 4.45),
            (datetime.date(2020, 5, 29), 4.8),
            (datetime.date(2020, 5, 30), 5.0),
        ]

        self.__assert_mood_data_equal(data, expected_data)

    def test_rolling_mean_5(self):
        """
        Test rolling mean of data for N=5
        """

        data = self.stats.rolling_mean(5)

        expected_data = [
            (datetime.date(2020, 5, 25), np.nan),
            # Missing day in CSV
            (datetime.date(2020, 5, 27), np.nan),
            (datetime.date(2020, 5, 28), np.nan),
            (datetime.date(2020, 5, 29), np.nan),
            (datetime.date(2020, 5, 30), 4.18),
        ]

        self.__assert_mood_data_equal(data, expected_data)

    def __assert_mood_data_equal(self, data, expected_data):
        """
        Compare two arrays of (datetime, avg_mood)
        """

        self.assertEqual(len(list(data)), len(list(expected_data)))

        for first, second in zip(data, expected_data):
            self.assertEqual(first[0], second[0])

            if np.isnan(first[1]):
                self.assertTrue(np.isnan(first[1]))
                self.assertTrue(np.isnan(second[1]))
            else:
                self.assertAlmostEquals(first[1], second[1], 3)
