"""Test config.py"""

import pytest

from daylio_parser.config import (
    DEFAULT_COLOR_PALETTE,
    DEFAULT_MOODS,
    Mood,
    MoodConfig,
    MoodNotFoundError,
)


def test_default_mood_list():
    """Test that the default config contains 5 moods with known boundaries."""
    m = MoodConfig()

    assert m.moods[0] == Mood(
        name="awful",
        level=1,
        boundaries=(1, 1.5),
        color=DEFAULT_COLOR_PALETTE[0],
    )
    assert m.moods[1] == Mood(
        name="bad",
        level=2,
        boundaries=(1.5, 2.5),
        color=DEFAULT_COLOR_PALETTE[1],
    )
    assert m.moods[2] == Mood(
        name="meh",
        level=3,
        boundaries=(2.5, 3.5),
        color=DEFAULT_COLOR_PALETTE[2],
    )
    assert m.moods[3] == Mood(
        name="good",
        level=4,
        boundaries=(3.5, 4.5),
        color=DEFAULT_COLOR_PALETTE[3],
    )
    assert m.moods[4] == Mood(
        name="rad",
        level=5,
        boundaries=(4.5, 5.01),
        color=DEFAULT_COLOR_PALETTE[4],
    )


def test_custom_moods():
    """Here we test that custom moods have correctly computed boundaries."""
    moods = [
        (1, "bad"),
        (2, "almost bad"),
        (3, "neutral"),
        (4, "almost good"),
        (5, "good"),
    ]

    m = MoodConfig(moods)

    assert m.moods[0] == Mood(
        name="bad",
        level=1,
        boundaries=(1, 1.5),
        color=DEFAULT_COLOR_PALETTE[0],
    )
    assert m.moods[1] == Mood(
        name="almost bad",
        level=2,
        boundaries=(1.5, 2.5),
        color=DEFAULT_COLOR_PALETTE[1],
    )
    assert m.moods[2] == Mood(
        name="neutral",
        level=3,
        boundaries=(2.5, 3.5),
        color=DEFAULT_COLOR_PALETTE[2],
    )
    assert m.moods[3] == Mood(
        name="almost good",
        level=4,
        boundaries=(3.5, 4.5),
        color=DEFAULT_COLOR_PALETTE[3],
    )
    assert m.moods[4] == Mood(
        name="good",
        level=5,
        boundaries=(4.5, 5.01),
        color=DEFAULT_COLOR_PALETTE[4],
    )


def test_custom_colors():
    """Test custom color palette."""
    colors = [
        "black",
        "red",
        "orange",
        "yellow",
        "green",
    ]

    m = MoodConfig(DEFAULT_MOODS, colors)

    assert m.moods[0].color == "black"
    assert m.moods[1].color == "red"
    assert m.moods[2].color == "orange"
    assert m.moods[3].color == "yellow"
    assert m.moods[4].color == "green"


def test_get_mood():
    """Test getter by mood name."""
    m = MoodConfig()

    assert m.get("good") == Mood(name="good", level=4, color="#4CA369", boundaries=(3.5, 4.5))


def test_get_mood_missing():
    m = MoodConfig()

    with pytest.raises(MoodNotFoundError, match="Mood 'this does not exist' is not configured"):
        m.get("this does not exist")


def test_validation():
    """Test wrong mood lists."""
    # Only 1 mood
    moods = [
        (1, "bad", "red"),
    ]

    with pytest.raises(ValueError):
        MoodConfig(moods)

    # Bad formatting
    moods = [
        ("bad",),
        ("almost bad",),
        ("neutral",),
        ("almost good",),
        ("good",),
    ]

    with pytest.raises(ValueError):
        MoodConfig(moods)

    # Missing level
    moods = [
        (1, "bad"),
        (2, "almost bad"),
        (3, "neutral"),
        (4, "almost good"),
        (4, "good"),
    ]

    with pytest.raises(ValueError):
        MoodConfig(moods)

    # Wrong level
    moods = [
        (1, "bad"),
        (2, "almost bad"),
        (3, "neutral"),
        (4, "almost good"),
        (5, "good"),
        (6, "rad"),
    ]

    with pytest.raises(ValueError):
        MoodConfig(moods)

    # Wrong palette
    colors = [
        "red",
    ]

    with pytest.raises(ValueError):
        MoodConfig(DEFAULT_MOODS, colors)
