import pathlib
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import datetime as dtt
import os
import plotly.express as px
import random as r

#df = pd.read_csv("c:/Users/valen/projet/darc-gr2/data/Week2/week0/id1.csv", sep="\t",names=["ID","date","lat","lon"])
#f=px.scatter(df,x=df["lon"],y=df["lat"])
#f.show()
def floutagetrace(df):
    d_lat = df["lat"].map(lambda t: t + np.random.uniform(-1,1)/100)
    d_lon = df["lon"].map(lambda t: t + np.random.uniform(-1,1)/100)
    df["lat"]=d_lat
    df["lon"]=d_lon
    """for i in range(t):
        
        pllon=r.randint(0,1)
        pllat=r.randint(0,1)
        if (pllon==1):
            df["lon"][i]=df["lon"][i]+x
        else:
            df["lon"][i]=df["lon"][i]-x
        if(pllat==1):
            df["lat"][i]=df["lat"][i]+y
        else:    
            df["lat"][i]=df["lat"][i]-y"""
#df.to_csv("c:/Users/valen/projet/darc-gr2/data/Week2/testmetric/floupar10.csv",sep="\t",index=False,header=False)
#d=px.scatter(df,x=df["lon"],y=df["lat"])
#d.show()
