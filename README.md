# python-versioning

A minimalist Python versioning tool, for semi-automated versioning of GIT projects.
The script does not proceed to any side-effect on the repository, nor fetches. This is beyond the scope of this script to alter your local state.

## Versioning convention

In a future work, we plan to comply with PEP440 : https://peps.python.org/pep-0440/.
The following versioning strategy is used for now.

A version is a string of the form `{major}.{minor}.{patch}{remaining}` where major, minor and patch are numeric symbols (greedily identified).
The versioning proposed by this utility uses a remaining scheme that is:
- empty for production builds
- prefixed with `a` for alpha-releases, then followed by a pseudo-unique identifier
- prefixed with `b` for beta-releases, then followed by a pseudo-unique identifier

The versioning is semi-automated, in the sense that `{major}.{minor}` follows the specification of a local file. The `{patch}` version is automatically
incremented.

## Install

In order to make it easy to fork, modify and extend the tool, we kept it as minimal as possible, as a unique python file.
There is no install nor Pypi repository, for now at least.

### Python version

Should be good with any of Python 3.

### Dependencies

- `GitPython` : see https://gitpython.readthedocs.io/en/stable/ 

## Usage

Assuming `version.txt` contains a `{major}.{minor}` version:

Production build:
```py
python python_versioning.py version.txt production
```
Alpha build:
```py
python python_versioning.py version.txt alpha
```
Beta build:
```py
python python_versioning.py version.txt beta
```

## Examples

## Use case scenario 1

Given a repository for which `git tag -l` yields an old tag:
```
(pyver) D:\projects\pyver>git tag -l
v0.0.0
```
Given also a `version.txt` file containing:
```
0.1
```
The next version is the one of the file (because file is higher):
```
(pyver) D:\projects\pyver>python pyver.py version.txt beta
0.1.1b+66110d0
```
Let us push this tag:
```
git tag v0.1.1b+66110d0
```
Next version is unchanged (because head commit is the highest tag and it matches the file):
```
(pyver) D:\projects\pyver>python pyver.py version.txt beta
0.1.1b+66110d0
```
Do a simple commit, and recompute the versioning: it changes because the head commit is not tagged:
```
(pyver) D:\projects\pyver>python pyver.py version.txt beta
0.1.2b+e9fa8aa
```
