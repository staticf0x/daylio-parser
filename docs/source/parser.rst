Parser
======

.. py:class:: Entry

    A class that holds data for an entry in the diary.
    One day can have multiple entries.

    .. py:attribute:: datetime
        :type: datetime.datetime

    .. py:attribute:: mood
        :type: Mood

    .. py:attribute:: activities
        :type: List[str]

    .. py:attribute:: notes
        :type: str

.. py:class:: Parser(config = None)

    Parser for the CSV file. If config is not provided, a default one
    will be created.

    :param MoodConfig config: MoodConfig for the parser

    .. py:method:: load_csv(path) -> List[Entry]

        Load entries from a CSV file.

        :param str path: Path to the CSV file

    .. py:method:: load_from_buffer(f) -> List[Entry]

        Actually reads the entries from a CSV file.

        :param f: A file-like object
