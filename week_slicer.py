import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import datetime as dtt
import os

"""
This code is used at the end of "simple_stats.py" to isolate every weeks, it may be bugged for now bc i've just copy-pasted it :eyes:. 
However it's working quite well in the original file. I'll do some debugging later. 

"""

df = pd.read_csv("./INSAnonym/bd.csv", sep="\t", names=["ID","date","lat","lon"] )

weeknum = pd.to_datetime(df["date"]).dt.isocalendar().week                                                                  #It goes from 10 to 20, there is a total of 10 differents weeks
df["week"] = weeknum
for k in range(11) :                                                                                #For each week 
    print(f"week number {k}")
    d_week = df[df["week"]== 10+k]
    print(f"This week we have {d_week.shape[0]} entries for {d_week['ID'].drop_duplicates().count()} ids")
    print("---------------------")
    d_week.drop(labels="week",axis= 1 )                                                             # Let's drop the useless columns with the same week number
    d_week.to_csv(f"./data/Week/week{10+k}")