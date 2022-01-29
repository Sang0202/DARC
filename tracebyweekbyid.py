import pathlib
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import datetime as dtt
import os

df = pd.read_csv('c:/Users/valen/projet/darc-gr2/INSAnonym/bd.csv', sep="\t", names=["ID","date","lat","lon"] )
 
weeknum = pd.to_datetime(df["date"]).dt.isocalendar().week                                                                
df["week"] = weeknum
for k in range(11) :                                                                                  
    #print("week number "+str(k))
    d_week = df[df["week"]== 10+k]
    for i in range(111):
        #print("number"+str(i))
        d_id=d_week[d_week["ID"]==i]
        if not d_id.empty:
            d_id.to_csv("c:/Users/valen/projet/darc-gr2/data/Week2/week"+str(k)+"/id"+str(i)+".csv", sep = "\t",index=False,header=False,columns=["ID","date","lat","lon"])