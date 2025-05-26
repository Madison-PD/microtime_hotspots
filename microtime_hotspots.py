import itertools
import math
from operator import itemgetter
from shapely.geometry import Point, Polygon, LineString, MultiPoint
from shapely import STRtree, minimum_bounding_circle, minimum_bounding_radius


class MTHS():
    """Initializes the Micro-Time Hot Spots (MTHS) class.

    Micro-Time Hot Spots are defined by user-defined inputs of minimum number of crimes, maximum radius of circle, and chosen number of days. For this class, the assumption is that the points provided are selected from the number
    of days to consider. Points may be provided as a list of lists or tuples representing x/y coordinates, or a list of shapely points. After considering all possible circles from the input points, only those with the minimum events
    and maximum radius survive. Then any circles that overlap with the same input points are removed. 

    :param points: List of tuples/lists representing coordinates or Shapely Point objects.
    :param events: Number of events needed to trigger MTHS.
    :param radius: Radius in feet for the MTHS circle.
    :param keep_overlapping: Boolean flag indicating whether overlapping circles should be kept.
    
    """
    def __init__(self, points: list, events: int=3, radius: float=1320, keep_overlapping: bool=False):
        if not isinstance(points, list):
            raise ValueError("Points must be a list.")
        
        if len(points) < 2:
            raise ValueError("At least two points are required to form a circle.")
        
        self.events = events
        self.radius = radius
        self.points = [Point(point[0], point[1]) if not isinstance(point, Point) else point for point in points]
        self.keep_overlapping = keep_overlapping
        self.tree = STRtree(self.points)
        self.min_points_circle = 2
        

    def _remove_circles_with_same_indices(self, data):
        """
        Removes circles from the dataset that have the same 'point_indices' and keeps only the one with the smallest radius
        
        :param data: (list of dict) A list where each element is a dictionary representing a circle. Each dictionary must contain
                             at least two keys: 'point_indices', an identifier for the point, and 'radius', the size of the circle.
        :return: A filtered list of dictionaries with circles
        :rtype: list of dict
        """
        result = []
        for _, group in itertools.groupby(sorted(data, key=itemgetter('point_indices')), key=itemgetter('point_indices')):
            min_radius_circle = min(group, key=lambda x: x['radius'])
            result.append(min_radius_circle)
            
        # First, sort the entire dataset by point_indices to ensure grouping works correctly.
        #sorted_data = sorted(data, key=itemgetter('point_indices'))
        
        #result = []
        #for _, group in itertools.groupby(sorted_data, key=itemgetter('point_indices')):
            # Convert group iterator to list and sort by radius
        #    group_list = sorted(group, key=itemgetter('radius'))
            
            # Append only the item with the smallest radius to the result list
        #    result.append(min(group_list, key=itemgetter('radius')))
        
        return result

    def _do_overlap(self, circle1, circle2):
        """
        Determines if two circles have overlapping point indices.
    
        :param circle1: (dict) A dictionary representing a circle with keys 'point_indices'
        :param circle2: (dict) Another dictionary representing a circle with keys 'point_indices'
        :return: True if the circles overlap (i.e., share at least one point index), False otherwise
        :rtype: bool
        """
        return set(circle1['point_indices']).intersection(set(circle2['point_indices'])) != set()

    
    def process(self) -> list:
        """
        This function generates all possible pairs of coordinates, then uses the user input minimum events and maximum radius to find minimally overlapping circle polygons.

        :return: list of circles with attributes
        :rtype: list
        """
        
        mths = []
        
        # Generate all coordinate pairs using itertools.combinations
        pairs = list(itertools.combinations(self.points, self.min_points_circle))

        # Loop through all pairs of coordinates
        for pair in pairs:

            # Calculate distance between the pair of points
            distance = pair[0].distance(pair[1])

            # If the distance is less than the diameter of the desired circle, then proceed to find its other attributes
            # If distance is greater than the diameter, the pair can be ignored
            if 0 < distance <= self.radius * 2:
                
                # Find the minimum bounding circle for the pair of coordinates
                mbc = minimum_bounding_circle(MultiPoint(list(pair)))
                
                # Create polygon circle from the mbc centroid with a buffer of the provided radius
                circle = Point(mbc.centroid.x, mbc.centroid.y).buffer(self.radius)
                
                # Count the number of points contained within the mbc
                n_points_contained = len(self.tree.query(circle, predicate='contains'))

                # If the number of points contained is greater than the user provided number of events, then continue processing the MTHS
                if n_points_contained >= self.events:

                    # Find associated attributes of the MTHS and append to the list
                    mths.append({
                            'geometry': circle,
                            'radius': minimum_bounding_radius(MultiPoint([self.points[idx] for idx in self.tree.query(circle, predicate='contains')])),
                            'centroid_x': mbc.centroid.x,
                            'centroid_y': mbc.centroid.y,
                            'area': round(circle.area,4),
                            'n_points_contained': n_points_contained,
                            'point_indices': self.tree.query(circle, predicate='contains'),
                    })

            # Need to handle situation when points have the same coordinates
            elif distance == 0:
                
                # Points with the same coordinates can use the point itself as the centroid with an arbitrary radius length
                circle = Point(pair[0].x,pair[0].y).buffer(self.radius)

                # Count the number of points contained within the mbc
                n_points_contained = len(self.tree.query(circle, predicate='contains'))
                
                # If the number of points contained is greater than the user provided number of events, then continue processing the MTHS
                if n_points_contained >= self.events:

                    # Find associated attributes of the MTHS and append to the list
                    mths.append({
                            'geometry': circle,
                            'radius': minimum_bounding_radius(MultiPoint([self.points[idx] for idx in self.tree.query(circle, predicate='contains')])),
                            'centroid_x': pair[0].x,
                            'centroid_y': pair[0].y,
                            'area': round(circle.area,4),
                            'n_points_contained': n_points_contained,
                            'point_indices': self.tree.query(circle, predicate='contains'),
                    })

        # If keep_overlapping is True, use a different function to remove only MTHS that have the exact same point indices
        # This may result in MTHS polygons with a lot of overlap when there are several points in common
        if self.keep_overlapping:
            selected_mths = self._remove_circles_with_same_indices(mths)
                    
        # If keep_overlapping is False, there may still be parts of MTHS polygons that overlap, but it will be much less
        else:
            # Sort the potential MTHS by the number of points contained (desc) and radius (asc)
            sorted_mths = sorted(mths, key=lambda x: (-x['n_points_contained'], x['radius']))

            # Create list to hold the selection
            selected_mths = []

            # Iterate over all sorted MTHS and select those that do not overlap with any already selected MTHS
            for i in range(len(mths)):
                if all(not self._do_overlap(sorted_mths[i], selected) for selected in selected_mths):
                    selected_mths.append(sorted_mths[i])

        self.mths = selected_mths
        return
