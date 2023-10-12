Example usage
=============

Load entries from CSV
---------------------

.. code-block:: python

    from daylio_parser.parser import Parser

    parser = Parser()
    entries = parser.load_csv("daylio_export_2023_10_12.csv")


Print some statistics
---------------------

.. code-block:: python

    from daylio_parser.parser import Parser
    from daylio_parser.stats import Stats

    parser = Parser()
    entries = parser.load_csv("daylio_export_2023_10_12.csv")

    stats = Stats(entries)

    avg_moods = stats.average_moods()  # Average mood value per day
    activity_moods = stats.activity_moods()  # Mean and standard deviation for each activity


Custom mood config
------------------

.. code-block:: python

    from daylio_parser.config import MoodConfig
    from daylio_parser.parser import Parser

    moods = [
        (1, "bad"),
        (2, "almost bad"),
        (3, "neutral"),
        (4, "almost good"),
        (5, "good"),
    ]

    colors = [
        "black",
        "red",
        "orange",
        "yellow",
        "green",
    ]

    config = MoodConfig(moods, colors)

    parser = Parser(config)
    entries = parser.load_csv("daylio_export_2023_10_12.csv")
