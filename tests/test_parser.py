# -*- coding: utf-8 -*-
"""
Test parser.py
"""

import datetime
import pathlib
from unittest import TestCase

from daylio_parser.parser import Entry, Parser


class TestParser(TestCase):
    def test_load_csv(self):
        here = pathlib.Path(__file__).parent.resolve()

        parser = Parser()
        entries = parser.load_csv(here/'data'/'test_data.csv')

        first_entry = Entry(
            datetime.datetime(2020, 5, 25, 7, 9),
            parser.config.get('meh'),
            [],
            ''
        )

        last_entry = Entry(
            datetime.datetime(2020, 5, 30, 18, 50),
            parser.config.get('rad'),
            ['friends', 'gaming', 'programming', 'nap'],
            'Awesome'
        )

        self.assertEqual(entries[0], first_entry)
        self.assertEqual(entries[-1], last_entry)
