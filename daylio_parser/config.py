"""Configuration objects for the parser and others."""

from dataclasses import dataclass
from typing import List, Tuple

DEFAULT_MOODS = [
    (1, 'awful'),
    (2, 'bad'),
    (3, 'meh'),
    (4, 'good'),
    (5, 'rad'),
]

DEFAULT_COLOR_PALETTE = [
    '#6C7679',
    '#5579A7',
    '#9454A3',
    '#4CA369',
    '#FF8500',
]


@dataclass
class Mood:
    """A class representing a mood level."""

    name: str
    level: int
    color: str
    boundaries: Tuple[float, float]


class MoodConfig:
    """Configure mood levels and their properties."""

    def __init__(self, mood_list: List[Tuple[int, str]] = None, color_palette: List[str] = None):
        """Create the config with a list of moods: [(level, name), ...].

        If no moods are provided, then the config is created
        with a default set of 5 moods.
        """
        self.moods: List[Mood] = []
        self.__map = {}

        if not mood_list:
            mood_list = DEFAULT_MOODS

        if not color_palette:
            color_palette = DEFAULT_COLOR_PALETTE

        self.__load_moods(mood_list, color_palette)

    def from_list(self, mood_list: List[Tuple[int, str]], color_palette: List[str] = None):
        """
        Update the config with a list of moods: [(level, name), ...].

        Optionally pass also a color_palette, if not provided, the default palette is used.
        """
        if not color_palette:
            color_palette = DEFAULT_COLOR_PALETTE

        self.__load_moods(mood_list, color_palette)

    def get(self, mood_name: str) -> Mood:
        """Return a Mood by its name."""
        return self.__map[mood_name]

    def __load_moods(self, mood_list: List[Tuple[int, str]], color_palette: List[str] = None):
        self.__validate_mood_list(mood_list)
        self.__validate_color_palette(color_palette)

        self.moods = []
        self.__map = {}

        for level, name in mood_list:
            if level == 1:
                # First (worst) mood
                b_lower = 1
                b_upper = 1.5
            elif level == 5:
                # Last (best) mood
                b_lower = 4.5
                b_upper = 5.01
            else:
                b_lower = level - 1 + 0.5
                b_upper = level - 1 + 1.5

            boundaries = (b_lower, b_upper)

            mood = Mood(name, level, color_palette[level - 1], boundaries)

            self.moods.append(mood)
            self.__map[name] = mood

    def __validate_mood_list(self, mood_list: List[Tuple[int, str, str]]):
        """Validate the provided mood list."""
        for mood in mood_list:
            if not len(mood) == 2:
                raise ValueError('Moods have to be (level, name)')

            level = mood[0]

            if level not in range(1, 6):
                raise ValueError(f'Mood level {level} is not valid')

        all_levels = set([mood[0] for mood in mood_list])

        if all_levels != set(range(1, 6)):
            raise ValueError('There has to be at least one mood for each level of {1..6}')

    def __validate_color_palette(self, color_palette: List[str] = None):
        """Validate the provided color palette."""
        if not len(color_palette) == 5:
            raise ValueError('Color palette must contain exactly 5 colors')
