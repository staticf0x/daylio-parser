# -*- coding: utf-8 -*-
"""
Configuration objects for the parser and others
"""

from dataclasses import dataclass
from typing import List, Tuple

DEFAULT_MOODS = [
    ('awful', '#6C7679'),
    ('bad', '#5579A7'),
    ('meh', '#9454A3'),
    ('good', '#4CA369'),
    ('rad', '#FF8500'),
]


@dataclass
class Mood:
    """
    A class representing a mood level
    """

    name: str
    level: int
    color: str
    boundaries: Tuple[float, float]


class MoodConfig:
    """
    Configure mood levels and their properties

    TODO: Add color generator when there's too many moods
    """

    def __init__(self, mood_list: List[Tuple[str, str]] = None):
        """
        Create the config with a list of moods: [(name, color), ...].
        If no moods are provided, then the config is created
        with a default set of 5 moods.
        """

        self.moods = []
        self.__map = {}

        if mood_list:
            self.__load_moods(mood_list)
        else:
            self.__load_moods(DEFAULT_MOODS)

    def from_list(self, mood_list: List[Tuple[str, str]]):
        """
        Update the config with a list of moods: [(name, color), ...]
        """

        self.__load_moods(mood_list)

    def get(self, mood_name: str) -> Mood:
        """
        Returns a Mood by its name
        """

        return self.__map[mood_name]

    def __load_moods(self, mood_list: List[Tuple[str, str]]):
        self.moods = []
        self.__map = {}

        for level, (name, color) in enumerate(mood_list):
            if level == 0:
                # First (worst) mood
                b_lower = 1
                b_upper = 1.5
            elif level == len(mood_list) - 1:
                # Last (best) mood
                b_lower = level + 0.5
                b_upper = level + 1.01
            else:
                b_lower = level + 0.5
                b_upper = level + 1.5

            boundaries = (b_lower, b_upper)

            mood = Mood(name, level + 1, color, boundaries)

            self.moods.append(mood)
            self.__map[name] = mood
