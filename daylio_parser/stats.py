# -*- coding: utf-8 -*-
"""
Mood statistics
"""

import datetime
from typing import Dict, List, Tuple

import numpy as np

from .parser import Entry


def average_moods(entries: List[Entry]) -> List[Tuple[datetime.date, float]]:
    """
    Computes average moods for each day. Returns a list
    of tuples: [(datetime.date, average mood that day), ...]
    """

    group_by_date = {}

    for entry in entries:
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


def activity_moods(entries: List[Entry]) -> Dict[str, Tuple[float, float]]:
    """
    Computes average moods for each activity in entries.
    Returns a dict: {activity name: (average mood, standard deviation)}
    """

    activity_to_mood = {}

    for entry in entries:
        for activity in entry.activities:
            activity_to_mood.setdefault(activity, [])
            activity_to_mood[activity].append(entry.mood.level)

    activities_avg = {}

    for activity, moods in activity_to_mood.items():
        activities_avg[activity] = (np.mean(moods), np.std(moods))

    return activities_avg
