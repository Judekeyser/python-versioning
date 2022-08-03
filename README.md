# python-versioning

A minimalist Python versioning tool, for semi-automated versioning of GIT projects.
The script does not proceed to any side-effect on the repository, nor fetches. This is beyond the scope of this script to alter your local state.

## Versioning convention

A version is a string of the form `{major}.{minor}.{patch}` where major, minor and patch are numeric symbols (greedily identified).

The versioning is semi-automated, in the sense that `{major}.{minor}` follows the specification of a local file.
The `{patch}` version is automatically incremented, based on the GIT repository tag list.

## Install

In order to make it easy to fork, modify and extend the tool, we kept it as minimal as possible, as a unique python file.
There is no install nor Pypi repository, for now at least.

### Python version

Should be good with any of Python 3.

### Dependencies

- `GitPython` : see https://gitpython.readthedocs.io/en/stable/ 

## Usage example

Each line represents a run of the script.
```
HEAD_COMMIT | HIGHEST TAG IN GIT | COMMIT OF HIGHEST TAG | MANUAL VERSION | RESULT OF SCRIPT
    1bf7316 |                  / |                     / |            0.0 |            0.0.1
    1bf7316 |             v0.0.1 |               1bf7316 |            0.0 |            0.0.1
    a05b2d8 |             v0.0.1 |               1bf7316 |            0.0 |            0.0.2
    a05b2d8 |             v0.0.1 |               1bf7316 |            0.1 |            0.1.1
    f917346 |             v0.0.1 |               1bf7316 |            0.1 |            0.1.1
    5f3f5e5 |             v0.1.1 |               f917346 |            0.1 |            0.1.2
    5f3f5e5 |             v0.2.1 |               5f3f5e5 |            0.1 |            0.2.1
```