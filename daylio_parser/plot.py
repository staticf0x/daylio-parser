"""Utilities to prepare data for plotting."""

import datetime
from typing import List

import numpy as np

from . import stats
from .config import MoodConfig
from .parser import Entry


class PlotData:
    """Class to operate on Entries and prepare them for plotting with matplotlib."""

    def __init__(self, entries: List[Entry], config: MoodConfig = None):
        """Create the object. If config is None, a default MoodConfig is created."""
        self.entries = entries
        self.config = config

        if not self.config:
            self.config = MoodConfig()

        self.__stats = stats.Stats(entries, config)

    def split_into_bands(self, moods):
        """Split input entries into bands given by config."""
        # {mood_name: masked_array}
        split_data = dict.fromkeys([mood.name for mood in self.config.moods])

        for mood in self.config.moods:
            # Upper bound
            masked_data = np.ma.masked_where(moods >= mood.boundaries[1], moods)

            # Lower bound
            masked_data = np.ma.masked_where(moods < mood.boundaries[0], masked_data)

            split_data[mood.name] = masked_data

        return split_data

    def interpolate(self, avg_moods=None, interpolate_steps: int = 360):
        """Interpolate missing values between midnights."""
        if avg_moods is None:
            avg_moods = self.__stats.average_moods()

        steps = int(interpolate_steps)

        if steps > 1440:
            raise ValueError("Max number of steps is 1440")

        dates = []
        moods = []
        step = 1440 // steps  # Step size in minutes

        # Add one day with the same mood, so that we have
        # the last day included in the charts too
        last_point = avg_moods[-1]
        new_point = (datetime.timedelta(days=1) + last_point[0], last_point[1])

        if isinstance(avg_moods, list):
            avg_moods.append(new_point)
        else:
            np.append(avg_moods, new_point)

        for i in range(len(avg_moods)):  # pylint: disable=consider-using-enumerate
            current_point = avg_moods[i]

            if np.isnan(current_point[1]):
                continue

            try:
                next_point = avg_moods[i + 1]
            except IndexError:
                # Add last day as the date on midnight
                next_time = datetime.time(hour=0, minute=0)
                next_dt = datetime.datetime.combine(current_point[0], next_time)

                dates.append(next_dt)
                moods.append(current_point[1])

                break

            value_diff = next_point[1] - current_point[1]  # Mood difference between days
            time_diff = steps  # Time difference a.k.a. number of buckets
            coef = value_diff / time_diff  # How much the mood changes in one step

            for step_n in range(0, steps):
                # Simple linear interpolation
                next_value = step_n * coef + current_point[1]

                # step*step_n == number of minutes in the current day
                # just split it into hours and minutes for time object
                hour = 0 if step_n == 0 else (step * step_n) // 60
                minute = 0 if step_n == 0 else (step * step_n) % 60

                next_time = datetime.time(hour=int(hour), minute=int(minute))
                next_dt = datetime.datetime.combine(current_point[0], next_time)

                dates.append(next_dt)
                moods.append(next_value)

        return np.array(dates), np.array(moods)
