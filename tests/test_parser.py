"""Test parser.py"""

import datetime

from daylio_parser.parser import Entry, Parser


def test_load_csv(test_csv):
    """Test that loading the CSV correctly parses the data into Entry objects."""
    parser = Parser()
    entries = parser.load_csv(test_csv)

    first_entry = Entry(
        datetime=datetime.datetime(2020, 5, 25, 7, 9),
        mood=parser.config.get("meh"),
        activities=[],
        notes="",
    )

    last_entry = Entry(
        datetime=datetime.datetime(2020, 5, 30, 18, 50),
        mood=parser.config.get("rad"),
        activities=["friends", "gaming", "programming", "nap"],
        notes="Awesome",
    )

    assert entries[0] == first_entry
    assert entries[-1] == last_entry


def test_both_hour_formats(test_csv):
    """Test that both 12 and 24 hour formats are parsed"""
    parser = Parser()
    entries = parser.load_csv(test_csv)

    entry_12h = entries[0]
    entry_24h = entries[1]

    assert entry_12h.datetime == datetime.datetime(2020, 5, 25, 7, 9)
    assert entry_24h.datetime == datetime.datetime(2020, 5, 25, 14, 58)
