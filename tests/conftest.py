"""Test fixtures."""
import pathlib

import pytest

from daylio_parser.parser import Parser


@pytest.fixture()
def test_csv():
    """Path to the test CSV."""
    here = pathlib.Path(__file__).parent.resolve()
    return here / "data" / "test_data.csv"


@pytest.fixture()
def entries(test_csv):
    """Return parsed entries from data/test_data.csv."""
    parser = Parser()
    return parser.load_csv(test_csv)
