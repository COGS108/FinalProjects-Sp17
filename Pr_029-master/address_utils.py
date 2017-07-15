import numpy as np
from pyproj import Proj, transform

def toMercator(lon,lat):
    inProj = Proj(init='epsg:3857')
    outProj = Proj(init='epsg:4326')
    x,y = transform(outProj,inProj,lon,lat)
    return x,y

strdirExpand = {'E':'East', 'S':'South', 'N':'North', 'W':'West'}
strTypeExpand = {'ST':'Street', 'AV':'Avenue', 'DR':'Drive', \
                 'RD':'Road', 'BL':'Boulevard', 'WY':'Way', 'CT':'Court', \
                 'PL':'Place', 'LN':'Lane', 'PY':'Parkway', 'HY':'Highway'}

strTypeKeys = strTypeExpand.keys()
strDirKeys = strdirExpand.keys()
                     


def CompileAddressString(stno, stdir, street, streetType):
    if stno is None:
        stno_str = ''
    else:
        stno_str = str(stno) + ' '
    
    if street is None:
        return None
    
    # Expand Street direction
    if stdir in strDirKeys:
        strdir_str = strdirExpand[stdir] + ' '
    else:
        strdir_str =  ''
    
    
    if streetType in strTypeKeys:
        streetType_str = strTypeExpand[streetType]
    else:
        streetType_str = streetType
    
    addressString = '%s%s%s %s' % (stno_str, strdir_str, street, streetType_str)
    return addressString


    