"""Configuration objects for the parser and others."""

import json
from typing import List, NewType, Tuple

from pydantic import BaseModel, ValidationError, validator
from pydantic.types import conint

DEFAULT_MOODS = [
    (1, "awful"),
    (2, "bad"),
    (3, "meh"),
    (4, "good"),
    (5, "rad"),
]

DEFAULT_COLOR_PALETTE = [
    "#6C7679",
    "#5579A7",
    "#9454A3",
    "#4CA369",
    "#FF8500",
]

MoodList = NewType("MoodList", List[Tuple[int, str]])


class Mood(BaseModel):
    """A class representing a mood level."""

    name: str
    level: conint(ge=1, le=5)
    color: str
    boundaries: Tuple[float, float]

    @validator("boundaries")
    def greater_than_previous(cls, v):
        """Validate that the boundaries are always (lower, higher)."""
        lower, higher = v

        if lower >= higher:
            raise ValidationError(f"Boundary {lower} must be lower than {higher}")

        return (lower, higher)


class MoodNotFound(Exception):
    """Exception for moods not being configured yet used in the CSV."""

    pass


class MoodConfig:
    """Configure mood levels and their properties."""

    def __init__(self, mood_list: MoodList = None, color_palette: List[str] = None):
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

    def from_list(self, mood_list: MoodList, color_palette: List[str] = None):
        """
        Update the config with a list of moods: [(level, name), ...].

        Optionally pass also a color_palette, if not provided, the default palette is used.
        """
        if not color_palette:
            color_palette = DEFAULT_COLOR_PALETTE

        self.__load_moods(mood_list, color_palette)

    @classmethod
    def from_file(cls, path: str):
        """Load MoodConfig from a JSON file.

        The file structure is:
        {
            "moods": [(level, name), ...],
            "colors": [value, ...],
        }
        """
        with open(path, "r") as fread:
            data = json.load(fread)
            moods = data.get("moods")
            colors = data.get("colors")

            return cls(moods, colors)

    def get(self, mood_name: str) -> Mood:
        """Return a Mood by its name."""
        try:
            return self.__map[mood_name]
        except KeyError:
            raise MoodNotFound(f"Mood '{mood_name}' is not configured")

    def __load_moods(self, mood_list: MoodList, color_palette: List[str] = None):
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

            mood = Mood(
                name=name, level=level, color=color_palette[level - 1], boundaries=boundaries
            )

            self.moods.append(mood)
            self.__map[name] = mood

    def __validate_mood_list(self, mood_list: MoodList):
        """Validate the provided mood list."""
        for mood in mood_list:
            if not len(mood) == 2:
                raise ValueError("Moods have to be (level, name)")

            level = mood[0]

            if level not in range(1, 6):
                raise ValueError(f"Mood level {level} is not valid")

        all_levels = set([mood[0] for mood in mood_list])

        if all_levels != set(range(1, 6)):
            raise ValueError("There has to be at least one mood for each level of {1..6}")

    def __validate_color_palette(self, color_palette: List[str] = None):
        """Validate the provided color palette."""
        if not len(color_palette) == 5:
            raise ValueError("Color palette must contain exactly 5 colors")
