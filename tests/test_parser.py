"""Test parser.py"""

import datetime
import pathlib
from unittest import TestCase

from daylio_parser.parser import Entry, Parser


class TestParser(TestCase):
    def setUp(self):
        here = pathlib.Path(__file__).parent.resolve()

        self.parser = Parser()
        self.entries = self.parser.load_csv(here / 'data' / 'test_data.csv')

    def test_load_csv(self):
        """Test that loading the CSV correctly parses the data into Entry objects."""

        first_entry = Entry(
            datetime.datetime(2020, 5, 25, 7, 9), self.parser.config.get('meh'), [], ''
        )

        last_entry = Entry(
            datetime.datetime(2020, 5, 30, 18, 50),
            self.parser.config.get('rad'),
            ['friends', 'gaming', 'programming', 'nap'],
            'Awesome',
        )

        self.assertEqual(self.entries[0], first_entry)
        self.assertEqual(self.entries[-1], last_entry)

    def test_both_hour_formats(self):
        """Test that both 12 and 24 hour formats are parsed"""

        entry_12h = self.entries[0]
        entry_24h = self.entries[1]

        self.assertEqual(entry_12h.datetime, datetime.datetime(2020, 5, 25, 7, 9))
        self.assertEqual(entry_24h.datetime, datetime.datetime(2020, 5, 25, 14, 58))
