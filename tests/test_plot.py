"""Test plot.py"""

import datetime

import numpy as np
import pytest

from daylio_parser.plot import PlotData


def test_split_into_bands(entries):
    plotdata = PlotData(entries)
    filtered_data = plotdata.split_into_bands(np.array([1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]))

    assert list(filtered_data["awful"][~filtered_data["awful"].mask].data) == [1.0]
    assert list(filtered_data["bad"][~filtered_data["bad"].mask].data) == [1.5, 2.0]
    assert list(filtered_data["meh"][~filtered_data["meh"].mask].data) == [2.5, 3.0]
    assert list(filtered_data["good"][~filtered_data["good"].mask].data) == [3.5, 4.0]
    assert list(filtered_data["rad"][~filtered_data["rad"].mask].data) == [4.5, 5.0]


def test_interpolate(entries):
    plotdata = PlotData(entries)

    dates, moods = plotdata.interpolate()

    first_date = dates[0].date()
    first_day = []

    for date, mood in zip(dates, moods):
        if date.date() == first_date:
            first_day.append((date, mood))

    first_entry = first_day[0]
    last_entry = first_day[-1]

    # First entry: midnight on the starting date, mood avg for the day is 2
    assert first_entry[0] == datetime.datetime(2020, 5, 25, 0, 0, 0)
    assert first_entry[1] == 2

    # Last entry: because we use 360 steps per day, one step == 4 minutes
    # therefore the last entry will be at 23:56
    # Next day mood avg is 4.3, so the last entry will be:
    #   Step size: (4.3 - 2) / (360)
    #   Last step no.: 359
    #   Last mood level: (start level) + (step size) * (1 step before next midnight)
    #     = 359 * (4.3 - 2) / (360) = 2.2936
    assert last_entry[0] == datetime.datetime(2020, 5, 25, 23, 56, 0)
    assert pytest.approx(last_entry[1], 0.0001) == 4.2936


def test_max_interpolate_steps(entries):
    plotdata = PlotData(entries)

    with pytest.raises(ValueError):
        plotdata.interpolate(None, 9999)
