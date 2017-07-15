import pandas as pd
import shapefile
import sys,argparse,csv
from shapely import geometry
from beat_from_coord import *

#read in the shape file
sf = shapefile.Reader(r'Drain_Structure')
shapes = sf.shapes()
records = sf.records()
myList = []
#create a list of all the lon/lat coordinates of the storm drains
for shape,record in zip(shapes,records):
	shape_points = geometry.asShape(shape)
	myList.append((shape_points[0].x,shape_points[0].y))

#write the beat number and name of all the coordinates to a csv file
with open('st_beats.csv','w') as f:
	for i in myList:
		beat,name = beat_from_coord(i[1],i[0])
		f.write(str(beat))
		f.write(',')
		f.write(str(name))
		f.write('\n')
		f.flush()
		print(beat,name)
