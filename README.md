# EasyCV

Computer Vision made easy.

[![Build Status](https://travis-ci.org/Resi-Coders/easycv.svg?branch=master)](https://travis-ci.org/easycv/easycv)
[![Documentation Status](https://readthedocs.org/projects/easycv/badge/?version=latest)](https://easycv.readthedocs.io/en/latest/?badge=latest)

## Installation

You can install **EasyCV** using [pip](https://pip.pypa.io/en/stable/) or from source.

### Using Pip

First ensure that you have the latest pip version to avoid dependency errors
```
pip install --upgrade pip
```
Then install **EasyCV** and all its dependencies using [pip](https://pip.pypa.io/en/stable/)
```
pip install easycv
```
### From Source

Clone the repository from [github](https://github.com/easycv/easycv)
```
git clone https://github.com/Resi-Coders/easycv.git
cd easycv
pip install .
```
You can view the list of all dependencies within the ``install_requires`` field
of ``setup.py``.

## Running the tests

### Test EasyCV with ``pytest``

If you don't have ``pytest`` installed run
```
pip install pytest
```
To run all tests just run
```
cd easycv
pytest .
```
## Versioning

[SemVer](http://semver.org/) is used for versioning. For available versions see the [tags on this repository](https://github.com/easycv/easycv/tags). 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
