# MTHS Package

A Python package for identifying Micro-Time Hot Spots (MTHS) using Shapely and other Python libraries.

## Installation

Install the package via pip:

```
pip install mths_package
```

or from source:

```
git clone https://github.com/yourusername/mths_package.git
cd mths_package
python setup.py install
```

## Usage

```python
from mths.mths import MTHS

points = [(0, 0), (1, 1), (2, 2)]
mths_instance = MTHS(points)
circles = mths_instance.process()
print(circles)
```
