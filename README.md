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
Shapely >= 2.0.0
GEOS >= 3.8
NumPy >= 1.26.4

## Usage
Provide a list of coordinate points as input. The points should be a list/tuple of x,y coordinates. 
```python
from microtime_hotspots import MTHS

points = [(0, 0), (1, 1), (2, 2), (3, 3)]
mths_instance = MTHS(points, events=3, radius=1000)
mths = mths_instance.process()
print(mths)
```

If you have a dataframe or geodataframe with x and y, you may supply the points as seen here. The class will convert them to Shapely Points.
```python
points = [x for x in zip(df['x'], df['y'])]
```

If GeoPandas is install, you can easily view a geodataframe of any resulting MTHS (be sure to set the CRS for your data)
```python
mths_gdf = gpd.GeoDataFrame(pd.DataFrame(mths.mths), geometry=pd.DataFrame(mths.mths)['geometry'], crs='EPSG:8193')
```
And explore the results on a map
```python
mths_gdf.explore()
```
