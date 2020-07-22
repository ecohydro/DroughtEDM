#!usr/bin/env python
# -*- coding: utf-8 -*-
#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

__author__ = 'Bryn Morgan'
__contact__ = 'bryn.morgan@geog.ucsb.edu'
__copyright__ = '(c) Bryn Morgan 2020'

__license__ = 'MIT'
__date__ = 'Sat 04 Jul 20 18:26:44'
__version__ = '1.0'
__status__ = 'initial release'
__url__ = ''

"""

Name:           somalia.py
Compatibility:  Python 3.7.0
Description:    Description of what program does

URL:            https://

Requires:       list of libraries required

Dev ToDo:       None

AUTHOR:         Bryn Morgan
ORGANIZATION:   University of California, Santa Barbara
Contact:        bryn.morgan@geog.ucsb.edu
Copyright:      (c) Bryn Morgan 2020


"""


#%% IMPORTS

import os
import math

import numpy as np
import pandas as pd


from scipy import stats
from scipy import spatial
import seaborn as sns

import matplotlib.pyplot as plt
import matplotlib as mpl


%matplotlib qt


#%% FUNCTIONS



#%% MAIN
def main():
    
#%% DATA IMPORT

    os.chdir('/Users/brynmorgan/Research/DroughtEDM/somalia/')

    unhcr = pd.read_excel('UNHCR-PRMN-Displacement-Dataset.xlsx', skiprows=1, \
            names=['MONTH','YR_WK','ARR_REGION','ARR_DISTRICT','DEP_REGION', \
                   'DEP_DISTRICT','REASON','PRIORITY_NEED','N_INDV'])

    som_centroids = pd.read_csv('SOM_Centroids.csv')



#%%

    som_centroids.ADM1_NAME.unique()
    dist = sorted(list(som_centroids.ADM2_NAME.unique()))

    ad = sorted(list(unhcr.ARR_DISTRICT.unique()))
    dd = sorted(list(unhcr.DEP_DISTRICT.unique()))


    #dep_dist = []
    #arr_dist = []
    #dep_i = []
    #arr_i = []
    #for i,d in enumerate(ad):
    #    if d in dist:
    #        print('Yes')
    #    else:
    #        print(i)
    #        arr_i.append(i)
            #dep_dist.append(d)

    for i,d in enumerate(dist):
        if d in dd:
            print('YES')
        else:
            print(d)

#%%
    # Index of districts with known aliases in som_centroids
    dep_i = [0, 6, 9, 10, 12, 13, 16, 18, 20, 27, 34, 40, 43, 52, 55, 56, 57, 60, 65, 68, 69, 70]
    # Index of som_centroids district name corresponding to dep_i
    dist_i = [0, 10, 56, 8, 12, 11, 15, 17, 19, 26, 5, 41, 38, 50, 5, 5, 53, 57, 62, 65, 66, 67]
    # Index of districts with unknown aliases
    #dep_i_unk = [6,9,34,55,56] # 10, 56, 5, 5, 5

    # Regions with unknown aliases:
        #Baidoa
        #Banadir
        #Dhahar
        #Laasqoray
        #Lasqoray

    # Initialize empty list for som_centroid aliases
    dist_vals = []
    # Iterate through district names
    for i,d in enumerate(dd):
        if d in dist:
            # For districts with the same name, add name to list.
            dist_vals.append(d)
        elif i in dep_i:
            # For districts with known aliases, add alias to list.
            dist_ind = dict(zip(dep_i,dist_i))[i]
            dist_vals.append(dist[dist_ind])
        else:
            # For unknown districts, insert '?'
            dist_vals.append('??')
    # Generate dictionary
    dist_dict = dict(zip(dd,dist_vals))

    unhcr['DEP_ALIAS'] = 'NA'
    unhcr['DEPARTURE_X'] = 0
    unhcr['DEPARTURE_Y'] = 0
    unhcr['ARR_ALIAS'] = 'NA'
    unhcr['ARRIVAL_X'] = 0
    unhcr['ARRIVAL_Y'] = 0


    for dep in dd:
        # Departure + arrival district aliases
        unhcr.DEP_ALIAS[unhcr.DEP_DISTRICT == dep] = dist_dict[dep]
        unhcr.ARR_ALIAS[unhcr.ARR_DISTRICT == dep] = dist_dict[dep]
        # Departure and arrival district coordinates
        if dist_dict[dep] != '??':
            unhcr.DEPARTURE_X[unhcr.DEP_DISTRICT == dep] = som_centroids.xcoord[som_centroids.ADM2_NAME == dist_dict[dep]].values[0]
            unhcr.DEPARTURE_Y[unhcr.DEP_DISTRICT == dep] = som_centroids.ycoord[som_centroids.ADM2_NAME == dist_dict[dep]].values[0]
            unhcr.ARRIVAL_X[unhcr.ARR_DISTRICT == dep] = som_centroids.xcoord[som_centroids.ADM2_NAME == dist_dict[dep]].values[0]
            unhcr.ARRIVAL_Y[unhcr.ARR_DISTRICT == dep] = som_centroids.ycoord[som_centroids.ADM2_NAME == dist_dict[dep]].values[0]
        else: 
            unhcr.DEPARTURE_X[unhcr.DEP_DISTRICT == dep] = np.nan
            unhcr.DEPARTURE_Y[unhcr.DEP_DISTRICT == dep] = np.nan
            unhcr.ARRIVAL_X[unhcr.ARR_DISTRICT == dep] = np.nan
            unhcr.ARRIVAL_Y[unhcr.ARR_DISTRICT == dep] = np.nan        


#%%
    unhcr.to_excel('UNHCR_Displacement_Coords.xlsx')

#%%
if __name__ == "__main__":
    main()