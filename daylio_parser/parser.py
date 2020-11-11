# -*- coding: utf-8 -*-
"""
Export CSV parser
"""

import csv
import datetime
from dataclasses import dataclass
from typing import List

from .config import Mood, MoodConfig


@dataclass
class Entry:
    """
    Data for one day
    """

    datetime: datetime.datetime
    mood: Mood
    activities: List[str]
    notes: str


class Parser:
    """
    Parser for the CSV file
    """

    def __init__(self, config=None):
        if not config:
            self.config = MoodConfig()
        else:
            self.config = config

    def load_csv(self, path):
        """
        Load data from a CSV file
        """

        with open(path, 'r') as fread:
            return self.load_from_buffer(fread)

    def load_from_buffer(self, f):
        """
        Load data from any file-like object
        """

        entries = []
        csv_reader = csv.reader(f, delimiter=',', quotechar='"')
        next(csv_reader)  # Skip header

        for row in csv_reader:
            # Raw data
            date_str = row[0]
            time_str = row[3]
            mood_str = row[4]
            activities = row[5]
            notes = row[6]

            mood = self.config.get(mood_str)

            # Create entry object
            dt = datetime.datetime.strptime(date_str, '%Y-%m-%d')

            try:
                t = datetime.datetime.strptime(time_str, '%I:%M %p')
            except ValueError:
                t = datetime.datetime.strptime(time_str, '%H:%M')

            # TODO: There has to be a better way
            t = datetime.time(hour=t.hour, minute=t.minute)
            dt = dt.combine(dt, t)

            entry = Entry(
                dt,
                mood,
                [] if activities == '' else activities.split(' | '),
                notes
            )

            entries.append(entry)

        entries.reverse()

        return entries
