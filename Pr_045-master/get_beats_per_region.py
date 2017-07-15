# Import this file where needed:
# from beat_from_coord import *
#
# Then call with lat,lon as args: i.e.
# beat,name = beat_from_lat_lon(32.73368,-117.15597)

import pandas as pd
import shapefile
from shapely import geometry

def get_beats_per_region():
    # Read beats data from shapefile
    sf = shapefile.Reader("data/beats/SDPD_BEATS")
    shapes = sf.shapes()
    records = sf.records()

    # Search for neighborhood containing lon/lat point
    # Translate name to beat number
    beat_names = pd.read_csv('data/beats/beat_names.csv')
    beat_names['Neighborhood'] = beat_names['Neighborhood'].str.lower().str.strip()
    centers = []
    for shape, record in zip(shapes,records):
        bbox = shape.bbox
        lats = bbox[0::2]
        longs = bbox[1::2]

        ctr = (sum(lats)/2.0,sum(longs)/2.0)
        name = record[0].lower().strip()
        name = name[:name.find('\x00')]
        beat = beat_names[beat_names['Neighborhood'] == name]['Beat'].tolist() 
        beat = beat[0] if beat != [] else -1
        centers.append((ctr,beat,name))

    # Translate region to beat list
    regions = pd.read_csv('data/health/RegionBoundaries.csv')
    all_regions_beats = []
    for region in regions.iterrows():
        region = region[1]
        region_beats = []
        tl_lon = region['Top Left Lat']
        tl_lat = region['Top Left Lon']
        tr_lon = region['Top Right Lat']
        tr_lat = region['Top Right Lon']
        bl_lon = region['Bottom Left Lat']
        bl_lat = region['Bottom Left Lon']
        br_lon = region['Bottom Right Lat']
        br_lat = region['Botton Right Lon']
        poly = geometry.Polygon([(tl_lon, tl_lat),(tr_lon, tr_lat),(bl_lon, bl_lat),(br_lon, br_lat)])
        for beatc in centers:
            cpoint = geometry.Point(beatc[0][1], beatc[0][0]) # longitude, latitude for shapely order
            if poly.contains(cpoint):
                region_beats.append((beatc[1],beatc[2]))
        all_regions_beats.append(region_beats)

    print all_regions_beats
    return all_regions_beats

get_beats_per_region()
