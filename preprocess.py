#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'Rachel Green'
__contact__ = 'rachel.green@geog.ucsb.edu'
__copyright__ = '(c) Rachel Green 2019'

__license__ = 'MIT'
__date__ = 'Thu Aug 22 14:17:07 2019'
__version__ = '1.0'
__status__ = 'initial release'
__url__ = ''


"""

Name:           filename.py
Compatibility:  Python 3.7.0
Description:    Description of what program does

URL:            https://

Requires:       list of libraries required

Dev ToDo:       None

AUTHOR:         Rachel Green
ORGANIZATION:   University of California, Santa Barbara
Contact:        rachel.green@geog.ucsb.edu
Copyright:      (c) Rachel Green 2019


"""


#%% IMPORTS

import os
import rasterio
from rasterio.mask import mask
from rasterio.plot import show
from rasterio.plot import show_hist
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.windows import Window
import pandas as pd
import geopandas as gpd
from shapely.geometry import box
import numpy as np
import matplotlib.pyplot as plt
from fiona.crs import from_epsg
import pycrs
import pathlib

#%% FUNCTIONS

def getFeatures(gdf):
    """Function to parse features form GeoDataFrame in such a manner that rasterio wants them """
    import json
    return [json.loads(gdf.to_json())['features'][0]['geometry']]

def maskImages(tiff_directory, mask_dir):
    #Get all GeoTiff filenames
    files = np.array(os.listdir(tiff_directory))
    tiffs = pd.Series(files).str.contains('.tiff')
    files = files[tiffs]
    
#Loop over files
    for filename in files:
        print(filename)
        
        #open raster in read mode
        data = rasterio.open(tiff_directory + filename)
        #print filenames
        #print('filename:' + filename + '\n' + 'image name:' + image_name)
      
        #make directory to store new images
        #pathlib.Path(mask_dir).mkdir(parents=True, exist_ok=True)
        
        #insert the bbox into a GeoDataFrame
        geo = gpd.GeoDataFrame({'geometry': bbox}, index=[0], crs=from_epsg(4326))

        #reprojectinto the same coordinate system as raster data
        geo = geo.to_crs(crs=data.crs.data)
  
        #get geometry coordinates by using getFeatures function
        coords = getFeatures(geo)

        #mask raster
        out_img, out_transform = mask(data, shapes=coords, crop=True)

        #modify metadata
        #copy metadata
        out_meta = data.meta.copy()

        #Parse EPSG code
        epsg_code = int(data.crs.data['init'][5:])

        #update metadata with new dimensions, transform (affine) and CRS (as Proj4 text)
        out_meta.update({"driver": "GTiff",
                   "height": out_img.shape[1],
                    "width": out_img.shape[2],
                    "transform": out_transform,
                    "crs": pycrs.parse.from_epsg_code(epsg_code).to_proj4()}
                             )
        #Get image name to usefor creating directory
        image_name = filename.split(".tiff")[0]
        
        #save clipped raster to disk
        with rasterio.open((mask_dir + image_name + '_mask.tiff'), "w", **out_meta) as dest: 
            dest.write(out_img)
        
        
#%% MAIN
def main():
#%%    

#specify input and output filepath
filename = '/Users/rgreen/Documents/UCSB/Research/Data/eMODIS_NDVI/data.2008.081.tiff'
image_name = 'data.2008.081'
#out_tif = r"/Users/rgreen/NDVI_masked_data.2008.081.tiff"

#open raster in read mode
#data = rasterio.open(filename)

#plot data
#show(data)

#%%

#create bounding box with shapely 
#WGS84 coordinates
minx, miny = 28, -12
maxx, maxy = 52, 15
bbox = box(minx, miny, maxx, maxy)
    

maskImages(tiff_directory = '/Volumes/Elements/eMODIS.ndvi_c6_v2/Africa/', mask_dir = '/Volumes/Elements/eMODIS.ndvi_c6_v2/EastAfrica/')       
#maskImages(tiff_directory = '/Users/rgreen/Documents/UCSB/Research/Data/eMODIS_NDVI/', mask_dir = '/Users/rgreen/Documents/UCSB/Research/Data/eMODIS_NDVI/')   
#%%

#load LC map

lc_file = '/Users/rgreen/Documents/UCSB/Research/Data/LC_EA_sen2/LC_EA_sen2.tiff'
lc = rasterio.open(lc_file)
show(lc)

#reproject to EPSG 4326
# =============================================================================
# 
# 
# reproject(inpath = '/Users/rgreen/Documents/UCSB/Research/Data/LC_EA_sen2.tiff',
#           outpath = '/Users/rgreen/Documents/UCSB/Research/Data/LC_EA_sen2_reproj.tiff',
#           new_crs = 'EPSG:4326')
# =============================================================================

dst_crs = 'EPSG:4326'

inputfile = '/Users/rgreen/Documents/UCSB/Research/Data/LC_EA_sen2/LC_EA_sen2.tiff'
outputfile = '/Users/rgreen/Documents/UCSB/Research/Data/LC_EA_sen2/LC_EA_sen2_reproject.tiff'


with rasterio.open(inputfile) as src:

    transform, width, height = calculate_default_transform(
        src.crs, dst_crs, src.width, src.height, *src.bounds)
    kwargs = src.meta.copy()
    kwargs.update({
        'crs': dst_crs,
        'transform': transform,
        'width': width,
        'height': height
    })

    with rasterio.open(outputfile, 'w', **kwargs) as dst:
        for i in range(1, src.count + 1):
            reproject(
                source=rasterio.band(src, i),
                destination=rasterio.band(dst, i),
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=transform,
                dst_crs=dst_crs,
                resampling=Resampling.nearest)

lc_84 = rasterio.open(outputfile)
show(lc_84)

#maskImages(tiff_directory = '/Users/rgreen/Documents/UCSB/Research/Data/LC_EA_sen2/', mask_dir = '/Users/rgreen/Documents/UCSB/Research/LC_EA_sen2/')   
#%%

#Windowed reading large geotiff

with rasterio.open('/Users/rgreen/Documents/UCSB/Research/Data/ESACCI-LC-L4-LC10-Map-20m-P1Y-2016-v1/ESACCI-LC-L4-LC10-Map-20m-P1Y-2016-v1.0.tif') as src:
    w = src.read(1, window=Window(0,0,512,256))

print(w.shape)


lc_full = '/Users/rgreen/Documents/UCSB/Research/Data/ESACCI-LC-L4-LC10-Map-20m-P1Y-2016-v1/ESACCI-LC-L4-LC10-Map-20m-P1Y-2016-v1.0.tif'
lc_africa = rasterio.open(lc_full)

print(lc_africa.is_tiled)
lc_africa.block_shapes

import xarray as xr
lc_africa = xr.open_rasterio('/Users/rgreen/Documents/UCSB/Research/Data/ESACCI-LC-L4-LC10-Map-20m-P1Y-2016-v1/ESACCI-LC-L4-LC10-Map-20m-P1Y-2016-v1.0.tif', chunks={'band':1, 'x': 512, 'y': 512})


maskImages(tiff_directory = '/Users/rgreen/Documents/UCSB/Research/Data/ESACCI-LC-L4-LC10-Map-20m-P1Y-2016-v1/', mask_dir = '/Users/rgreen/Documents/UCSB/Research/Data/ESACCI-LC-L4-LC10-Map-20m-P1Y-2016-v1/')

lc_africa_m = '/Users/rgreen/Documents/UCSB/Research/Data/ESACCI-LC-L4-LC10-Map-20m-P1Y-2016-v1/ESACCI-LC-L4-LC10-Map-20m-P1Y-2016-v1.0_mask.tiff'
lc_africa_m = rasterio.open(lc_africa_m)
show(lc_africa_m)
#%%
if __name__ == "__main__":
    main()



#%%
