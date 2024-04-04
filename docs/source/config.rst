Config
======

daylio-parser comes with a default config that works for the
default Daylio setup after installing the app. That is, there's
just 5 moods, called ``awful, bad, meh, good, rad``.

Each mood has its class:

.. py:class:: Mood

    .. py:attribute:: name
        :type: str

        Name of the mood, must correspond with mood name in the exported CSV.

    .. py:attribute:: level
        :type: int

        Assigned numeral level for the mood (higher = better mood).
        The allowed levels are 1 to 5.

    .. py:attribute:: color
        :type: str

        Any hex color.

    .. py:attribute:: boundaries
        :type: Tuple[float, float]

        A tuple with lower and upper bound for the mood.
        Any average mood that falls withing these boundaries
        will be colored using the :py:attr:`Mood.color`.

The whole mood config for your app will be constructed using the
:py:class:`MoodConfig` class.

.. py:class:: MoodConfig(mood_list = None, color_palette = None)

    Creates a config with mood_list. If the mood list isn't provided,
    ``DEFAULT_MOODS`` will be used. All moods are automatically
    colored using ``color_palette`` and boundaries are also calculated.
    Each boundary is exactly 1 in size, with the first one and the last one
    being only 0.5 in size.

    :param mood_list: A list of moods with (level, name)
    :param color_palette: A list of colors (hex values or common names)

    :type mood_list: List[Tuple[int, str]]
    :type color_palette: List[str]

    .. py:method:: from_list(mood_list, color_palette = None) -> None

        Updates the config with a new list of moods.

        :param mood_list: A list of moods with (level, name)
        :param color_palette: A list of colors (hex values or common names)

        :type mood_list: List[Tuple[str, str]]
        :type color_palette: List[str]

    .. py:staticmethod:: from_file(path) -> MoodConfig

        Loads the MoodConfig from a JSON file.
        The file structure is:

        .. code-block::

            {
                "moods": [(level, name), ...],
                "colors": [value, ...],
            }

        :type path: str

    .. py:method:: get(mood_name) -> Mood

        Returns a :py:class:`Mood` by its name.

        Raises :py:class:`MoodNotFoundError` if the ``mood_name`` doesn't exist.

        :param str mood_name: Mood name


.. py:exception:: MoodNotFoundError

    Raised in cases when attempting to retrieve a non-existing :py:class:`Mood`.
