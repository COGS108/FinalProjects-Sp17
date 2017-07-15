import shapefile as shp #download at https://github.com/GeospatialPython/pyshp
import pandas as pd
import urllib
import zipfile
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

YOURFILE = 'wowee.csv'

BEATS = 'data/beats/SDPD_BEATS'
WIDTH = 10
HEIGHT = 5

def gen_heatmap(df):
    ##read shapefile
    sf = shp.Reader(BEATS)

    ###PLOT
    ##get the shapes
    patches=[]
    fig, ax = plt.subplots()
    matplotlib.rcParams['figure.figsize'] = (WIDTH, HEIGHT)
    for shape in sf.shapeRecords(): #loop over polygon
        x = [i[0] for i in shape.shape.points[:]] #get all x coord of one polygon
        y = [i[1] for i in shape.shape.points[:]] #get all y coord of one polygon
        plt.plot(x,y,"k") #draw contours in black
        polygon = Polygon(np.array([x,y]).T, closed=True) #get one single polygon
        patches.append(polygon) #add it to a final array
                            
    ##get the population density as color code
    records = sf.records()
    desired_order = get_order(records)

    coloring = [df[df['Beat'] == bt]['Value'].values.tolist() for bt in desired_order]
    coloring = [c[0] if c != [] else 0 for c in coloring]
    coloring = [abs(float(c)) for c in coloring]
    coloring = np.array(coloring) #Must be floats

    colors = coloring/max(coloring) #normalize color

    ##now plot    
    p = PatchCollection(patches, cmap="Blues")
    p.set_array(colors)
    ax.add_collection(p)
    ax.set_xlim([-117.3,-116.88])
    ax.set_ylim([32.65,33.15])
    fig.colorbar(p, ax=ax)
    plt.show()


def get_order(records):
    # Translate name to beat number
    beat_names = pd.read_csv('data/beats/beat_names.csv')
    beat_names['Neighborhood'] = beat_names['Neighborhood'].str.lower().str.strip()

    ordered = []
    for record in records:
        name = record[0].lower().strip()
        name = name[:name.find('\x00')]

        beat = beat_names[beat_names['Neighborhood'] == name]['Beat'].tolist() 
        beat = beat[0] if beat != [] else -1

        ordered.append(beat)

    ordered.remove(-1)
    return ordered


df = pd.read_csv(YOURFILE)
gen_heatmap(df)
