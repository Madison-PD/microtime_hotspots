# Micro-Time Hotspot Identification

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

## Dependencies


## Usage

```python
from microtime_hotspots import MTHS

points = [(0, 0), (1, 1), (2, 2), (3, 3)]
mths_instance = MTHS(points, events=3, radius=1000)
mths = mths_instance.process()
print(mths)
```
