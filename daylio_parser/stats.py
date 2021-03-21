# -*- coding: utf-8 -*-
"""
Mood statistics
"""

import datetime
from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np

from .parser import Entry, MoodConfig


@dataclass
class MoodPeriod:
    """
    A class to represent a closed period of either good or bad mood
    """

    start_date: datetime.datetime
    end_date: datetime.datetime
    duration: int
    avg_mood: float


class Stats:
    """
    A class to compute stats, interpolate data and so on.
    """

    def __init__(self, entries: List[Entry], config: MoodConfig=None):
        self.entries = entries
        self.config = config

        if not self.config:
            self.config = MoodConfig()

    def average_moods(self) -> List[Tuple[datetime.date, float]]:
        """
        Computes average moods for each day. Returns a list
        of tuples: [(datetime.date, average mood that day), ...]
        """

        group_by_date = {}

        for entry in self.entries:
            date = datetime.date(
                entry.datetime.year,
                entry.datetime.month,
                entry.datetime.day
            )

            group_by_date.setdefault(date, [])
            group_by_date[date].append(entry.mood.level)

        result = []

        for date, moods in group_by_date.items():
            result.append((date, np.mean(moods)))

        return result


    def activity_moods(self) -> Dict[str, Tuple[float, float]]:
        """
        Computes average moods for each activity in entries.
        Returns a dict: {activity name: (average mood, standard deviation)}
        """

        activity_to_mood = {}

        for entry in self.entries:
            for activity in entry.activities:
                activity_to_mood.setdefault(activity, [])
                activity_to_mood[activity].append(entry.mood.level)

        activities_avg = {}

        for activity, moods in activity_to_mood.items():
            activities_avg[activity] = (np.mean(moods), np.std(moods))

        return activities_avg


    def split_into_bands(self):
        """
        Splits input entries into bands given by config.
        """

        # {mood_name: masked_array}
        split_data = dict.fromkeys([mood.name for mood in self.config.moods])

        # Mood values from entries
        moods = np.array([e.mood.level for e in self.entries])

        for mood in self.config.moods:
            # Upper bound
            masked_data = np.ma.masked_where(moods >= mood.boundaries[1], moods)

            # Lower bound
            masked_data = np.ma.masked_where(moods < mood.boundaries[0], masked_data)

            split_data[mood.name] = masked_data

        return split_data

    def stability(self, mood_levels: List[float]) -> int:
        """
        Return percent stability for given list of mood levels.
        """

        return 0

    def stability_by_month(self) -> List[Tuple[datetime.date, int]]:
        """
        Computes mood stability for each year-month in given entries.
        """

        group_by_date = {}

        for entry in self.entries:
            date = datetime.date(
                entry.datetime.year,
                entry.datetime.month,
                1
            )

            group_by_date.setdefault(date, [])
            group_by_date[date].append(entry.mood.level)

        result = []

        for date, moods in group_by_date.items():
            result.append((date, self.stability(moods)))

        return result
