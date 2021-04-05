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

    def __init__(self, entries: List[Entry], config: MoodConfig = None):
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

    def mean(self):
        """
        Returns mean, std from all entries.
        """

        mood_levels = [x.mood.level for x in self.entries]

        return np.mean(mood_levels), np.std(mood_levels)

    def rolling_mean(self, N=5):
        """
        Compute rolling mean for the average moods, where N is the
        window size
        """

        data = np.array(self.average_moods())

        # Compute the rolling mean for our data
        # Moods are stored in the 1st column, dates in 0th
        filtered_data = np.convolve(data[:, 1], np.ones((N, ))/N, mode='valid')
        filtered_data = filtered_data.astype(np.float64).round(2)

        # Fill the missing entries with NaN,
        # so we can replace the original column
        # with filtered data
        nans = np.zeros(N - 1)
        nans[:] = np.nan
        filtered_data = np.concatenate((nans, filtered_data))
        data[:, 1] = filtered_data

        return data

    def stability(self, mood_levels: List[float]) -> int:
        """
        Return percent stability for given list of mood levels.
        """

        raise NotImplementedError('Mood stability is not yet implemented.')

        return 0

    def stability_by_month(self) -> List[Tuple[datetime.date, int]]:
        """
        Computes mood stability for each year-month in given entries.
        """

        raise NotImplementedError('Mood stability is not yet implemented.')

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
