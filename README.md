[![ci-badge][]][ci-link] [![docs-badge][]][docs-link]
[![py-versions-badge][]][pypi-link] [![pypi-badge][]][pypi-link]

# daylio-parser

A Python module to parse Daylio CSV exports

## Development

Install `poetry`, `tox` and `tox-poetry`.

Installing the virtual env:

`$ poetry install`

Switching into the venv:

`$ poetry shell`

Running test for the current python version:

`$ pytest -v --cov=daylio_parser --cov-report term-missing tests`

Running all checks with tox prior to running GitHub actions:

`$ tox`

## TODO

- [x] Parse CSV into entries (parser.py)
- [x] Implement MoodConfig (config.py) to allow multiple moods
    - [x] Plus a default config for clean Daylio installs
- [ ] Stats
    - [ ] Mood stability algorithm
    - [x] Average moods by day
    - [x] Average mood by activity
    - [x] Find mood periods — aka periods of moods meeting certain criteria
    - [ ] Extend mood period search — search above, below and in between thresholds
- [x] Prepare data for plotting
    - [x] Splitting entries into bands
    - [x] Interpolating data for smooth charts
    - [x] Calculating rolling mean
- [ ] Re-export data into other formats
    - [ ] JSON

[ci-link]: https://github.com/staticf0x/daylio-parser/actions/workflows/check.yml
[ci-badge]: https://img.shields.io/github/workflow/status/staticf0x/daylio-parser/Check/master
[docs-link]: https://daylio-parser.readthedocs.io/en/latest/
[docs-badge]: https://img.shields.io/readthedocs/daylio-parser/latest
[py-versions-badge]: https://img.shields.io/pypi/pyversions/daylio-parser
[pypi-link]: https://pypi.org/project/daylio-parser/
[pypi-badge]: https://img.shields.io/pypi/v/daylio-parser
