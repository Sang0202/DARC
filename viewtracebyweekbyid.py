import pathlib
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import datetime as dtt
import os
import plotly.express as px

week=input("numéro week ")
id=input("numéro id ")

df = pd.read_csv("c:/Users/valen/projet/darc-gr2/data/Week2/week"+str(week)+"/id"+str(id)+".csv", sep="\t")
f=px.scatter(df,x=df["lon"],y=df["lat"])
f.show()