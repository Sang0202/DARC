import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import datetime as dtt

#Only serves to select the plot theme. can be comment 
import seaborn as sns
sns.set_theme()


#Let's iterate for everyweek 
for k in range(10): 
    df = pd.read_csv(f"./data/Week/week1{k}" )
    data = df["ID"].value_counts(sort = True)
    data.name = "count"
    data.index.name = "ID"
    data.plot(kind="bar", title = f"Apparition by ID | Week 1{k}", xlabel = "ID", ylabel = "Apparitions", color="limegreen", figsize= (15,8))
    plt.savefig(f"./Image/ID_Week1{k}")
    plt.clf()