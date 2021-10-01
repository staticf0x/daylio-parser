"""Test config.py"""

from unittest import TestCase

from daylio_parser.config import (
    DEFAULT_COLOR_PALETTE,
    DEFAULT_MOODS,
    Mood,
    MoodConfig,
    MoodNotFound,
)


class TestConfig(TestCase):
    def test_default_mood_list(self):
        """Test that the default config contains 5 moods with known boundaries."""

        m = MoodConfig()

        self.assertEqual(m.moods[0].name, 'awful')
        self.assertEqual(m.moods[0].level, 1)
        self.assertEqual(m.moods[0].boundaries, (1, 1.5))
        self.assertEqual(m.moods[0].color, DEFAULT_COLOR_PALETTE[0])

        self.assertEqual(m.moods[1].name, 'bad')
        self.assertEqual(m.moods[1].level, 2)
        self.assertEqual(m.moods[1].boundaries, (1.5, 2.5))
        self.assertEqual(m.moods[1].color, DEFAULT_COLOR_PALETTE[1])

        self.assertEqual(m.moods[2].name, 'meh')
        self.assertEqual(m.moods[2].level, 3)
        self.assertEqual(m.moods[2].boundaries, (2.5, 3.5))
        self.assertEqual(m.moods[2].color, DEFAULT_COLOR_PALETTE[2])

        self.assertEqual(m.moods[3].name, 'good')
        self.assertEqual(m.moods[3].level, 4)
        self.assertEqual(m.moods[3].boundaries, (3.5, 4.5))
        self.assertEqual(m.moods[3].color, DEFAULT_COLOR_PALETTE[3])

        self.assertEqual(m.moods[4].name, 'rad')
        self.assertEqual(m.moods[4].level, 5)
        self.assertEqual(m.moods[4].boundaries, (4.5, 5.01))
        self.assertEqual(m.moods[4].color, DEFAULT_COLOR_PALETTE[4])

    def test_custom_moods(self):
        """Here we test that custom moods have correctly computed boundaries."""

        moods = [
            (1, 'bad'),
            (2, 'almost bad'),
            (3, 'neutral'),
            (4, 'almost good'),
            (5, 'good'),
        ]

        m = MoodConfig(moods)

        self.assertEqual(m.moods[0].name, 'bad')
        self.assertEqual(m.moods[0].level, 1)
        self.assertEqual(m.moods[0].boundaries, (1, 1.5))

        self.assertEqual(m.moods[1].name, 'almost bad')
        self.assertEqual(m.moods[1].level, 2)
        self.assertEqual(m.moods[1].boundaries, (1.5, 2.5))

        self.assertEqual(m.moods[2].name, 'neutral')
        self.assertEqual(m.moods[2].level, 3)
        self.assertEqual(m.moods[2].boundaries, (2.5, 3.5))

        self.assertEqual(m.moods[3].name, 'almost good')
        self.assertEqual(m.moods[3].level, 4)
        self.assertEqual(m.moods[3].boundaries, (3.5, 4.5))

        self.assertEqual(m.moods[4].name, 'good')
        self.assertEqual(m.moods[4].level, 5)
        self.assertEqual(m.moods[4].boundaries, (4.5, 5.01))

    def test_validation(self):
        """Test wrong mood lists."""

        # Only 1 mood
        moods = [
            (1, 'bad', 'red'),
        ]

        with self.assertRaises(ValueError):
            MoodConfig(moods)

        # Bad formatting
        moods = [
            ('bad',),
            ('almost bad',),
            ('neutral',),
            ('almost good',),
            ('good',),
        ]

        with self.assertRaises(ValueError):
            MoodConfig(moods)

        # Missing level
        moods = [
            (1, 'bad'),
            (2, 'almost bad'),
            (3, 'neutral'),
            (4, 'almost good'),
            (4, 'good'),
        ]

        with self.assertRaises(ValueError):
            MoodConfig(moods)

        # Wrong level
        moods = [
            (1, 'bad'),
            (2, 'almost bad'),
            (3, 'neutral'),
            (4, 'almost good'),
            (5, 'good'),
            (6, 'rad'),
        ]

        with self.assertRaises(ValueError):
            MoodConfig(moods)

        # Wrong palette
        colors = [
            'red',
        ]

        with self.assertRaises(ValueError):
            MoodConfig(DEFAULT_MOODS, colors)

    def test_custom_colors(self):
        """Test custom color palette."""

        colors = [
            'black',
            'red',
            'orange',
            'yellow',
            'green',
        ]

        m = MoodConfig(DEFAULT_MOODS, colors)

        self.assertEqual(m.moods[0].color, 'black')
        self.assertEqual(m.moods[1].color, 'red')
        self.assertEqual(m.moods[2].color, 'orange')
        self.assertEqual(m.moods[3].color, 'yellow')
        self.assertEqual(m.moods[4].color, 'green')

    def test_get_mood(self):
        """Test getter by mood name."""

        m = MoodConfig()

        expected = Mood('good', 4, '#4CA369', (3.5, 4.5))

        self.assertEqual(m.get('good'), expected)

    def test_get_mood_missing(self):
        m = MoodConfig()

        with self.assertRaises(MoodNotFound):
            m.get("this does not exist")
