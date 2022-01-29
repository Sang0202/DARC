import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import datetime as dtt
import os
pd.set_option("display.max_rows", 400) #We set that options to see a bit more clearly what's happening. 

"""
"""

# --------------------------------------Reading Dataframe-------------------------------------------------
df = pd.read_csv("./INSAnonym/bd.csv", sep="\t", names=["ID","date","lat","lon"] )
print(df)
print("-------------")

# --------------------------------------Founding all IDs in the df-------------------------------------------------
id = df["ID"].drop_duplicates()
print(id)
data = df["ID"].value_counts(sort = False)
data.name = "count"
data.index.name = "ID"
data.plot(kind="bar", title = "Apparition by ID", xlabel = "ID", ylabel = "Apparitions", color="limegreen")
F_id = pd.DataFrame(id).join(pd.DataFrame(data), on = "ID") #Creating a db with each ID count
F_id.to_csv("./data/ID_Apparitions.csv") #In that file you'll find the IDs that we just displayed
print("--------------")

# --------------------------------------Manipulating dates-------------------------------------------------
dd = pd.to_datetime(df["date"])                                                                     #Modifying times data to manipulates them more easily
df["date"] = dd 
if os.path.exists("./data/Entries_per_day.csv") : 
    F_dates = pd.read_csv("./data/Entries_per_day.csv")
    F_dates = F_dates.set_index("original_index")
else :
    dd2 = dd.dt.strftime("%Y-%m-%d")                                                                # We'll be looking for a number of entries for each days
    date_df = pd.DataFrame(dd2.drop_duplicates())                                                   # Group By Day with the first index of each day
    date_df.index.name = "original_index"                                                             
    data = dd2.value_counts(sort=False)                                                             
    data.name = 'count'                                                                             
    freq_df = pd.DataFrame(data)                                                                    # Count the number of entries for each days
    freq_df.index.name = "date"                                                                     
    F_dates = date_df.join(freq_df, on="date")                                                      # Creating a dataframe which sum up everything

F_dates.plot(x = "date", y ="count", title="Entries per day", kind = "bar", color ="lightgreen")    # Creating a plot


#-----------------

dr = df[["ID","date"]]                                                                              # We'll be looking for a number of ID by days (And which IDs)
dd2 = dr["date"].dt.strftime("%Y-%m-%d")                                                            # Again, Grouping by days (PS. I prbly shall find an optimized way to do that because it's quite long )
dr.loc[:,"date"] = dd2
dr.drop_duplicates()
dr = dr.sort_values("date")
dr.groupby("date").count().plot(kind="bar",color = "lightgreen",title = "Ids per day", ylabel = "Nb of IDs")
dr.to_csv("./data/ID_per_day.csv")


#-----------------


print("First Date : ", dd.min() )                                                                   # The first day of the df is 2015-03-04 00:00:00
print("-------------")
print(F_dates)
F_dates.to_csv("./data/Entries_per_day.csv")
plt.show()

#-------------------------------------Sequencing by week------------------------------------------------

weeknum = df["date"].dt.isocalendar().week                                                                  #It goes from 10 to 20, there is a total of 10 differents weeks
df["week"] = weeknum
for k in range(11) :                                                                                #For each week 
    print(f"week number {k}")
    d_week = df[df["week"]== 10+k]
    print(f"This week we have {d_week.shape[0]} entries for {d_week['ID'].drop_duplicates().count()} ids")
    print("---------------------")
    d_week.drop(labels="week",axis= 1 )                                                             # Let's drop the useless columns with the same week number
    d_week.to_csv(f"./data/Week/week{10+k}")

