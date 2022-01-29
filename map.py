import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import datetime as dtt
import sys
import os
import time
import matplotlib.colors as colors 
start = time.time()
pd.set_option("display.max_rows", 400) #We set that options to see a bit more clearly what's happening. 


#--------------------------- Warning ! / Disclaimer ! 
# This script is extremely long to execute, it is only done to be run once. 
# If you want to do the same things, you may use the ./data/np_count.txt array which contains the result for those parameters (ie 100x100 matrix / Lattice)

def mapping(df,Mx_lon,Mx_lat,mn_lon,mn_lat) : 
    delta_lon = (Mx_lon - mn_lon) * 1/100
    delta_lat = (Mx_lat - mn_lat) *1/100

    lon_tile = np.arange(mn_lon,Mx_lon+2 *delta_lon,delta_lon)
    lat_tile = np.arange(mn_lat,Mx_lat+2 * delta_lat,delta_lat)
    print(f"length lon_tile = {len(lon_tile)} \nlength lat_tile = {len(lat_tile)}")
    if len(lon_tile) != len(lat_tile) : 
        sys.exit()


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

    end = time.time()
    print(f"time for executing the script : {end-start} seconds ")
    np.savetxt("./data/np_counts.txt",counts)
    xtile, ytile = np.meshgrid(lon_tile,lat_tile)
    print(xtile)
    print(ytile)
    print(counts)
    plt.pcolormesh(ytile, xtile, counts, shading="auto", norm = colors.LogNorm() )
    plt.xlabel("lat")
    plt.ylabel("lon")
    plt.colorbar()
    plt.show()


#-------------------------------------- for the entire db with constant view (Aka no zoom allowed) Don't forget to comment if not used
#Importing database 
df = df = pd.read_csv("./INSAnonym/bd.csv", sep="\t", names=["ID","date","lat","lon"] )

#Finding min and max of our map
Mx_lon = 67.8942716666667                   #df['lon'].max() = 67.8942716666667
mn_lon = 14.7070466666667                   #df['lon'].min() = 14.7070466666667
print(f"Maximum longitude : {Mx_lon},\nMinimum longitude : {mn_lon}")

Mx_lat = 121.805258333333                   # df['lat'].max() = 121.805258333333
mn_lat = -97.770815                   #df['lat'].min()  = -97.770815
print(f"Maximum latitude : {Mx_lat}, \nMinimum latitude : {mn_lat}")



#--------------------------------------------- To change the params : Comment / Uncomment to use
"""
path = input("Enter Path to the db : ")
df = pd.read_csv(path)
#Finding min and max of our map
Mx_lon = int(input("Enter the max longitude : "))
mn_lon = int(input("Enter the min longitude : "))
print(f"Maximum longitude : {Mx_lon},\nMinimum longitude : {mn_lon}")

Mx_lat = int(input("Enter the max latitude : "))
mn_lat = int(input("Enter the min latitude : "))
print(f"Maximum latitude : {Mx_lat}, \nMinimum latitude : {mn_lat}")
"""

mapping(df,Mx_lon,Mx_lat,mn_lon,mn_lat)