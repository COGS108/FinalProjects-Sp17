import csv
from pylab import *

def read_ascii_boundary(filestem):
    '''
    Reads polygon data from an ASCII boundary file.
    Returns a dictionary with polygon IDs for keys. The value for each
    key is another dictionary with three keys:
    'name' - the name of the polygon
    'polygon' - list of (longitude, latitude) pairs defining the main 
    polygon boundary 
    'exclusions' - list of lists of (lon, lat) pairs for any exclusions in
    the main polygon
    '''
    metadata_file = filestem + 'a.dat'
    data_file = filestem + '.dat'
    # Read metadata
    lines = [line.strip().strip('"') for line in open(metadata_file)]
    polygon_ids = lines[::6]
    polygon_names = lines[2::6]
    polygon_data = {}
    for polygon_id, polygon_name in zip(polygon_ids, polygon_names):
        # Initialize entry with name of polygon.
        # In this case the polygon_name will be the 5-digit ZIP code.
        polygon_data[polygon_id] = {'name': polygon_name}
    del polygon_data['0']
    # Read lon and lat.
    f = open(data_file)
    for line in f:
        fields = line.split()
        if len(fields) == 3:
            # Initialize new polygon
            polygon_id = fields[0]
            polygon_data[polygon_id]['polygon'] = []
            polygon_data[polygon_id]['exclusions'] = []
        elif len(fields) == 1:
            # -99999 denotes the start of a new sub-polygon
            if fields[0] == '-99999':
                polygon_data[polygon_id]['exclusions'].append([])
        else:
            # Add lon/lat pair to main polygon or exclusion
            lon = float(fields[0])
            lat = float(fields[1])
            if polygon_data[polygon_id]['exclusions']:
                polygon_data[polygon_id]['exclusions'][-1].append((lon, lat))
            else:
                polygon_data[polygon_id]['polygon'].append((lon, lat))
    return polygon_data

# Main script starts here

# Read in ZIP code boundaries for California
d = read_ascii_boundary('../data/zip5/zt06_d00')

# Read in data for number of births by ZIP code in California
f = csv.reader(open('../data/CA_2007_births_by_ZIP.txt', 'rb'))
births = {}
# Skip header line
f.next()
# Add data for each ZIP code
for row in f:
    zipcode, totalbirths = row
    births[zipcode] = float(totalbirths)
max_births = max(births.values())
    
# Create figure and two axes: one to hold the map and one to hold
# the colorbar
figure(figsize=(5, 5), dpi=30)
map_axis = axes([0.0, 0.0, 0.8, 0.9])
cb_axis = axes([0.83, 0.1, 0.03, 0.6])

# Define colormap to color the ZIP codes.
# You can try changing this to cm.Blues or any other colormap
# to get a different effect
cmap = cm.PuRd

# Create the map axis
axes(map_axis)
axis([-125, -114, 32, 42.5])
gca().set_axis_off()

# Loop over the ZIP codes in the boundary file
for polygon_id in d:
    polygon_data = array(d[polygon_id]['polygon'])
    zipcode = d[polygon_id]['name']
    num_births = births[zipcode] if zipcode in births else 0.
    # Define the color for the ZIP code
    fc = cmap(num_births / max_births)
    # Draw the ZIP code
    patch = Polygon(array(polygon_data), facecolor=fc,
        edgecolor=(.3, .3, .3, 1), linewidth=.2)
    gca().add_patch(patch)
title('Births per ZIP Code in California (2007)')

# Draw colorbar
cb = mpl.colorbar.ColorbarBase(cb_axis, cmap=cmap,
    norm = mpl.colors.Normalize(vmin=0, vmax=max_births))
cb.set_label('Number of births')

# Change all fonts to Arial
for o in gcf().findobj(matplotlib.text.Text):
    o.set_fontname('Arial')

# Export figure to bitmap    
savefig('../images/ca_births.png')

# Alabama - zt01_d00_ascii.zip (1,337,894 bytes)
# Alaska - zt02_d00_ascii.zip (2,422,373 bytes)
# Arizona - zt04_d00_ascii.zip (671,250 bytes)
# Arkansas - zt05_d00_ascii.zip (1,075,188 bytes)
# California - zt06_d00_ascii.zip (2,384,051 bytes)
# Colorado - zt08_d00_ascii.zip (716,993 bytes)
# Connecticut - zt09_d00_ascii.zip (151,649 bytes)
# Delaware - zt10_d00_ascii.zip (66,719 bytes)
# District of Columbia - zt11_d00_ascii.zip (5,622 bytes)
# Florida - zt12_d00_ascii.zip (1,411,382 bytes)
# Georgia - zt13_d00_ascii.zip (1,277,994 bytes)
# Hawaii - zt15_d00_ascii.zip (96,927 bytes)
# Idaho - zt16_d00_ascii.zip (945,922 bytes)
# Illinois - zt17_d00_ascii.zip (1,113,702 bytes)
# Indiana - zt18_d00_ascii.zip (633,872 bytes)
# Iowa - zt19_d00_ascii.zip (739,942 bytes)
# Kansas - zt20_d00_ascii.zip (549,856 bytes)
# Kentucky - zt21_d00_ascii.zip (1,126,044 bytes)
# Louisiana - zt22_d00_ascii.zip (2,004,513 bytes)
# Maine - zt23_d00_ascii.zip (823,805 bytes)
# Maryland - zt24_d00_ascii.zip (458,410 bytes)
# Massachusetts - zt25_d00_ascii.zip (267,826 bytes)
# Michigan - zt26_d00_ascii.zip (1,069,536 bytes)
# Minnesota - zt27_d00_ascii.zip (1,379,067 bytes)
# Mississippi - zt28_d00_ascii.zip (883,573 bytes)
# Missouri - zt29_d00_ascii.zip (1,263,140 bytes)
# Montana - zt30_d00_ascii.zip (1,049,799 bytes)
# Nebraska - zt31_d00_ascii.zip (479,941 bytes)
# Nevada - zt32_d00_ascii.zip (355,712 bytes)
# New Hampshire - zt33_d00_ascii.zip (214,635 bytes)
# New Jersey - zt34_d00_ascii.zip (377,427 bytes)
# New Mexico - zt35_d00_ascii.zip (575,545 bytes)
# New York - zt36_d00_ascii.zip (1,534,728 bytes)
# North Carolina - zt37_d00_ascii.zip (1,350,374 bytes)
# North Dakota - zt38_d00_ascii.zip (378,917 bytes)
# Ohio - zt39_d00_ascii.zip (955,139 bytes)
# Oklahoma - zt40_d00_ascii.zip (1,007,513 bytes)
# Oregon - zt41_d00_ascii.zip (1,373,757 bytes)
# Pennsylvania - zt42_d00_ascii.zip (1,442,746 bytes)
# Rhode Island - zt44_d00_ascii.zip (38,161 bytes)
# South Carolina - zt45_d00_ascii.zip (1,032,777 bytes)
# South Dakota - zt46_d00_ascii.zip (503,723 bytes)
# Tennessee - zt47_d00_ascii.zip (1,235,351 bytes)
# Texas - zt48_d00_ascii.zip (2,989,249 bytes)
# Utah - zt49_d00_ascii.zip (558,052 bytes)
# Vermont - zt50_d00_ascii.zip (185,521 bytes)
# Virginia - zt51_d00_ascii.zip (1,350,179 bytes)
# Washington - zt53_d00_ascii.zip (1,269,377 bytes)
# West Virginia - zt54_d00_ascii.zip (856,311 bytes)
# Wisconsin - zt55_d00_ascii.zip (1,259,540 bytes)
# Wyoming - zt56_d00_ascii.zip (625,937 bytes)
# Puerto Rico - zt72_d00_ascii.zip (118,729 bytes)
