"""Test plot.py"""

import datetime

import pytest

from daylio_parser.plot import PlotData


@pytest.mark.skip(reason="TODO: test this method")
def test_split_into_bands(entries):
    plotdata = PlotData(entries)
    _ = plotdata.split_into_bands()


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
