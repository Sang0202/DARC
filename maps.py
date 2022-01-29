""" maps.py
Creates a set of 10 maps for each weeks reprensenting entries positions for this week. 
The map is shaped with max and min value of the dataset, it is always a 100 x 100 matrix.  

not much than a copy-paste from map.py with a loop  
"""

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import datetime as dtt
import sys
import os
import time
import matplotlib.colors as colors 

#Only serves to select the plot theme. can be comment 
import seaborn as sns
sns.set_theme()


plots = []
for k in range(10) : 
    plot = plt.subplots()
    plots.append(plot)

for k in range(10) : 
    fig, ax = plots[k]
    df = df = pd.read_csv(f"./data/Week/week1{k}" )
    
    #Finding min and max of our map
    Mx_lon = df['lon'].max()                   #df['lon'].max() = 67.8942716666667
    mn_lon = df['lon'].min()                   #df['lon'].min() = 14.7070466666667
    print(f"Maximum longitude : {Mx_lon},\nMinimum longitude : {mn_lon}")

    Mx_lat = df['lat'].max()                   # df['lat'].max() = 121.805258333333
    mn_lat = df['lat'].min()                   #df['lat'].min()  = -97.770815
    print(f"Maximum latitude : {Mx_lat}, \nMinimum latitude : {mn_lat}")

    delta_lon = (Mx_lon - mn_lon) * 1/100
    delta_lat = (Mx_lat - mn_lat) *1/100

    lon_tile = np.arange(mn_lon,Mx_lon+2 *delta_lon,delta_lon)
    lat_tile = np.arange(mn_lat,Mx_lat+2 * delta_lat,delta_lat)
    print(f"length lon_tile = {len(lon_tile)} \nlength lat_tile = {len(lat_tile)}")

    if len(lon_tile) != len(lat_tile) : 
        lon_tile = lon_tile[:101]                                                      #CORRECTION
        lat_tile = lat_tile[:101] 


    #Let's count the number of entry for a tile (The bottom left point of the tile is (x,y) in the graph )
    #tiles = pd.DataFrame({'lon' : [] ,'lat' : [], 'count' : [] }) #It's an alternate method I left here. We never if it could be useful. 
    counts = np.zeros( (len(lon_tile), len(lat_tile))  )
    for n in range(len(lon_tile)) :
        x = lon_tile[n] 
        for m in range(len(lat_tile)) :
            y = lat_tile[m] 
            count = df[(x < df['lon'])&(df['lon'] <= (x+delta_lon) )&(y< df['lat'])&(df['lat'] <= y + delta_lat)]['ID'].count()
            counts[m][n] = count
            print(f"({n},{m}), count = {count}")
            #tiles = tiles.append({'lon' : x,'lat' : y, 'count' : count}, ignore_index = True) #Let's append the count we just found at the end of the df

    np.savetxt("./data/np_counts.txt",counts)
    xtile, ytile = np.meshgrid(lon_tile,lat_tile)
    print(xtile)
    print(ytile)
    print(counts)
    plot =ax.pcolormesh(ytile, xtile, counts, shading="auto", norm = colors.LogNorm() )
    ax.set_xlabel("lat")
    ax.set_ylabel("lon")
    ax.set_title(f"week 1{k}")
    fig.colorbar(plot, ax = ax)


plt.show()

    
