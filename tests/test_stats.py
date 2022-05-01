import datetime
import pathlib

import numpy as np
import pytest

from daylio_parser.parser import Parser
from daylio_parser.stats import Stats


@pytest.fixture()
def entries():
    here = pathlib.Path(__file__).parent.resolve()
    parser = Parser()
    return parser.load_csv(here / "data" / "test_data.csv")


def test_average_moods(entries):
    """Test computing average moods (day by day) from the CSV."""
    stats = Stats(entries)
    avg_moods = stats.average_moods()

    expected = [
        (datetime.date(2020, 5, 25), 2.0),
        (datetime.date(2020, 5, 27), 4.3),
        (datetime.date(2020, 5, 28), 4.6),
        (datetime.date(2020, 5, 29), 5.0),
        (datetime.date(2020, 5, 30), 5.0),
    ]

    assert avg_moods == expected


def test_activity_moods(entries):
    """Test mood averages for each activity."""
    stats = Stats(entries)
    moods = stats.activity_moods()

    assert pytest.approx(moods["work"][0]) == 4.0
    assert pytest.approx(moods["work"][1], 0.01) == 0.89

    assert pytest.approx(moods["programming"][0]) == 5.0
    assert pytest.approx(moods["programming"][1]) == 0


def test_mean(entries):
    stats = Stats(entries)
    mean, std = stats.mean()

    assert pytest.approx(mean, 0.00001) == 4.15625
    assert pytest.approx(std, 0.0001) == 1.2275


@pytest.mark.skip(reason="TODO: implement Stats.stability")
def test_stability(entries):
    """Test stability on some real world data."""
    stats = Stats(entries)

    assert stats.stability([3]) == 100
    assert stats.stability([4, 3, 4, 2, 3, 2, 4, 3]) == 68
    assert stats.stability([4, 3, 4, 2, 3, 2, 4, 3, 4, 4, 4]) == 81


def test_rolling_mean_2(entries):
    """Test rolling mean of data for N=2."""
    stats = Stats(entries)

    data = stats.rolling_mean(2)

    expected_data = [
        (datetime.date(2020, 5, 25), np.nan),
        # Missing day in CSV
        (datetime.date(2020, 5, 27), 3.15),
        (datetime.date(2020, 5, 28), 4.45),
        (datetime.date(2020, 5, 29), 4.8),
        (datetime.date(2020, 5, 30), 5.0),
    ]

    __assert_mood_data_equal(data, expected_data)


def test_rolling_mean_5(entries):
    """Test rolling mean of data for N=5."""
    stats = Stats(entries)

    data = stats.rolling_mean(5)

    expected_data = [
        (datetime.date(2020, 5, 25), np.nan),
        # Missing day in CSV
        (datetime.date(2020, 5, 27), np.nan),
        (datetime.date(2020, 5, 28), np.nan),
        (datetime.date(2020, 5, 29), np.nan),
        (datetime.date(2020, 5, 30), 4.18),
    ]

    __assert_mood_data_equal(data, expected_data)


def __assert_mood_data_equal(data, expected_data):
    """Compare two arrays of (datetime, avg_mood)."""
    assert len(list(data)) == len(list(expected_data))

    for first, second in zip(data, expected_data):
        assert first[0] == second[0]

        if np.isnan(first[1]):
            assert np.isnan(first[1])
            assert np.isnan(second[1])
        else:
            assert pytest.approx(first[1], 0.001) == pytest.approx(second[1], 0.001)
