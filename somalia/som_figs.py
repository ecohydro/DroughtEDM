#!usr/bin/env python
# -*- coding: utf-8 -*-
#––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

__author__ = 'Bryn Morgan'
__contact__ = 'bryn.morgan@geog.ucsb.edu'
__copyright__ = '(c) Bryn Morgan 2020'

__license__ = 'MIT'
__date__ = 'Thu 13 Aug 20 11:06:21'
__version__ = '1.0'
__status__ = 'initial release'
__url__ = ''

"""

Name:           som_figs.py
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
import datetime

import numpy as np
import pandas as pd


from scipy import stats
from scipy import spatial
import seaborn as sns

import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as mdates

%matplotlib qt


#%% FUNCTIONS



#%% MAIN
def main():
    
#%% DATA IMPORT

    unhcr_in = pd.read_excel('UNHCR_Displacement_Coords.xlsx', usecols=range(1,17))


#%% PRE-PROCESSING

    unhcr = unhcr_in.copy()

    # Month
    #unhcr.MONTH.apply(lambda x: datetime.datetime.strptime(x, "%b").month)
    # Year
    #unhcr.YR_WK.astype(str).str.slice(stop=4).astype(int)
    # Week number
    #unhcr.YR_WK.astype(str).str.slice(4).astype(int)

    # ADD A DATE COLUMN
    # First day of the week
    unhcr.insert(2,'WK_OF', pd.to_datetime(unhcr.YR_WK.astype(str) + '1', format='%Y%W%w') )
    # Change to last day of the week (can omit, but better when plotting)
    unhcr.WK_OF = unhcr.WK_OF + datetime.timedelta(days=6)
    # Sort
    unhcr.sort_values(by=['WK_OF','ARR_REGION','ARR_DISTRICT',],inplace=True)
    # Reset index
    #unhcr.reset_index(inplace=True,drop=True)
    unhcr.set_index('WK_OF',inplace=True,drop=True)





#%% A FEW QUICK PLOTS

    # 1. Plot of # displaced over time by reason
    # Note: both of these should really be bar graphs, but this takes way too long
    fig,ax = plt.subplots()

    for reason in sorted(unhcr.REASON.unique()):
        df = unhcr[unhcr.REASON == reason]
        plt.plot(df.index,df.N_INDV,label=reason,alpha=0.7)

    ax.set_ylabel('# of people displaced')

    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_minor_locator(mdates.MonthLocator())    
    ax.set_xlim(datetime.date(2015,12,1),datetime.date(2020,1,1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))   
    plt.gcf().autofmt_xdate()

    plt.legend(bbox_to_anchor=(1.02,1), loc='upper left')


    # 2. Plot of # displaced over time by departure region
    fig,ax = plt.subplots()

    for region in sorted(unhcr.DEP_REGION.unique()):
        df = unhcr[unhcr.DEP_REGION == region]
        plt.plot(df.index,df.N_INDV, label=region, alpha=0.7)

    ax.set_ylabel('# of people displaced')

    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_minor_locator(mdates.MonthLocator())    
    ax.set_xlim(datetime.date(2015,12,1),datetime.date(2020,1,1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))   
    plt.gcf().autofmt_xdate()

    plt.legend(bbox_to_anchor=(1.02,1), loc='upper left')


#%% MONTHLY


    # 3. Monthly totals
    fig,ax = plt.subplots()

    plt.bar(pd.date_range(start='2016-01',end='2019-11',freq='MS'),
             unhcr.N_INDV.groupby([unhcr.index.year,unhcr.index.month]).sum(),width=10)

    ax.set_ylabel('# of people displaced')

    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_minor_locator(mdates.MonthLocator())    
    ax.set_xlim(datetime.date(2015,12,1),datetime.date(2020,1,1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))   
    plt.gcf().autofmt_xdate()






#%%
if __name__ == "__main__":
    main()