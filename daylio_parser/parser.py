"""Export CSV parser."""

import csv
import datetime
from typing import List

from pydantic import BaseModel

from .config import Mood, MoodConfig


class Entry(BaseModel):
    """Data for one day."""

    datetime: datetime.datetime
    mood: Mood
    activities: List[str]
    notes: str = ""


class Parser:
    """Parser for the CSV file."""

    def __init__(self, config=None):
        """Create the object. If config is None, a default MoodConfig is created."""
        if not config:
            self.config = MoodConfig()
        else:
            self.config = config

    def load_csv(self, path):
        """Load data from a CSV file."""
        with open(path, "r") as fread:
            return self.load_from_buffer(fread)

    def load_from_buffer(self, f):
        """Load data from any file-like object."""
        entries = []
        csv_reader = csv.DictReader(f, delimiter=",", quotechar='"')

        for row in csv_reader:
            mood = self.config.get(row["mood"])

            # Create entry object
            dt = datetime.datetime.strptime(row["full_date"], "%Y-%m-%d")

            try:
                t = datetime.datetime.strptime(row["time"], "%I:%M %p")
            except ValueError:
                t = datetime.datetime.strptime(row["time"], "%H:%M")

            # TODO: There has to be a better way
            t = datetime.time(hour=t.hour, minute=t.minute)
            dt = dt.combine(dt, t)

            entry = Entry(
                datetime=dt,
                mood=mood,
                activities=[] if row["activities"] == "" else row["activities"].split(" | "),
                notes=row["note"],
            )

            entries.append(entry)

        # Will be oldest to newest
        entries.reverse()

        return entries
