Stats
=====

.. py:class:: MoodPeriod

    This class represents a period of moods.

    .. py:attribute:: start_date
        :type: datetime.datetime

    .. py:attribute:: end_date
        :type: datetime.datetime

    .. py:attribute:: duration
        :type: int

        Length of the period as a number of days.

    .. py:attribute:: avg_mood
        :type: float

        Average mood for the whole period.

.. py:class:: Stats(entries, config = None)

    A class for computing various stats from the entries.

    :param entries: A list of parsed entries
    :param MoodConfig config: MoodConfig for the parser (if none is provided, a default one will be created)

    :type entries: List[Entry]

    .. py:method:: average_moods() -> List[Tuple[datetime.date, float]]

        Computes average mood for each day.

    .. py:method:: activity_moods() -> Dict[str, Tuple[float, float]]

        Computes average mood and standard deviation for each activity.
        The returned dict has mood name as a key and (mean, std) as value.

    .. py:method:: mean() -> Tuple[float, float]

        Returns (mean, std) for all entries.

    .. py:method:: rolling_mean(N = 5)

        Computes a rolling mean for the entries.

        :param int N: Window size

    .. py:method:: find_high_periods(threshold = 4, min_duration = 4) -> List[MoodPeriod]

        Find all periods of high moods.

        :param float threshold: Find moods higher than this
        :param int min_duration: Find periods longer than this

    .. py:method:: find_low_periods(threshold = 3, min_duration = 5) -> List[MoodPeriod]

        Find all periods of low moods.

        :param float threshold: Find moods higher than this
        :param int min_duration: Find periods longer than this
