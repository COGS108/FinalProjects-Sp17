# Import this file where needed:
# from beat_from_coord import *
#
# Then call with lat,lon as args: i.e.
# beat,name = beat_from_lat_lon(32.73368,-117.15597)

import pandas as pd
import shapefile
from shapely import geometry

def beat_from_coord(lat,lon):
    # Read beats data from shapefile
    sf = shapefile.Reader("data/beats/SDPD_BEATS")
    shapes = sf.shapes()
    records = sf.records()

    # Search for neighborhood containing lon/lat point
    point = geometry.Point(lon, lat) # longitude, latitude for shapely order
    name = 'Not Found'
    for shape, record in zip(shapes,records):
        shape_points = geometry.asShape(shape)
        if shape_points.contains(point):
            name = record[0].lower().strip()
            name = name[:name.find('\x00')]
            name = exception_lookup(name)
            break

    # Translate name to beat number
    beat_names = pd.read_csv('data/beats/beat_names.csv')
    beat_names['Neighborhood'] = beat_names['Neighborhood'].str.lower().str.strip()
    beat = beat_names[beat_names['Neighborhood'] == name]['Beat'].tolist() 
    beat = beat[0] if beat != [] else -1

    return beat, name

def exception_lookup(name):
    if name == 'mission bay':
        return 'mission beach'
    else:
        return name
