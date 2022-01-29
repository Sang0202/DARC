from numpy.lib.function_base import append
from numpy.random.mtrand import rand
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import datetime as dtt
import os
import time

"""
"""

# --------------------------------------Reading Dataframe-------------------------------------------------
df = pd.read_csv("./INSAnonym/bd_test.csv", sep="\t", names=["ligne","ID","date","lat","lon"])  # ici je fais cat -n bd.csv > bd_test.csv donc il y a column de #lignes

print("-------------")
# print(df)
print("-------------")

# --------------------------------------Manipulating dates-------------------------------------------------
dd = pd.to_datetime(df["date"])                                                                     #Modifying times data to manipulates them more easily
df["date"] = dd

#-------------------------------------Sequencing by week------------------------------------------------
weeknum = df["date"].dt.isocalendar().week                              #get numero de semain  
df["week"] = weeknum

for k in range(1) :                                                                                #For each week 
    print(f"week number {k}")
    week = df[df["week"]== 10+k]
    
    # week=week.drop(columns=["week"])                            # Let's drop the useless columns with the same week number                                                          
    # week.to_csv(f"./data/Week/bd_week{10+k}",sep="\t")

    week_day = week["date"].dt.isocalendar().day                #get day of week to manipulate
    week["week_day"] = week_day

    js= week[week["week_day"] <= 5]                                 # jour de travail
    wk= week.drop(week[week["week_day"] <= 5].index)                # wk

    #---------Modify hours-----------------------------------------------
    # week["date"] = week["date"].map(lambda t: t + pd.Timedelta(minutes = np.random.randint(-60*3,3*60)))   # je fais un rand -3h,+3h pour tous valeur
    
    for i in wk.index:
        if (wk.at[i,"date"].hour >= 10) & (wk.at[i,"date"].hour < 13):
            wk.at[i,"date"] = wk.at[i,"date"] + pd.Timedelta(seconds =  np.random.randint(0, 3*60*60))
        else:
            if (wk.at[i,"date"].hour >= 15) & (wk.at[i,"date"].hour < 18):
                wk.at[i,"date"] = wk.at[i,"date"] + pd.Timedelta(seconds =  np.random.randint(-3*60*60, 0))  
            else:
                wk.at[i,"date"] = wk.at[i,"date"] + pd.Timedelta(seconds =  np.random.randint(-3*60*60, 3*60*60))  
    
    for i in js.index:
        if ((js.at[i,"date"].hour >= 9) & (js.at[i,"date"].hour < 12)) | ((js.at[i,"date"].hour >= 22) | (js.at[i,"date"].hour < 1)):
            js.at[i,"date"] = js.at[i,"date"] + pd.Timedelta(seconds =  np.random.randint(0, 3*60*60))
        else:
            if ((js.at[i,"date"].hour >= 13) & (js.at[i,"date"].hour < 16)) | ((js.at[i,"date"].hour >= 3) & (js.at[i,"date"].hour < 6)):
                js.at[i,"date"] = js.at[i,"date"] + pd.Timedelta(seconds =  np.random.randint(-3*60*60, 0))
            else:
                js.at[i,"date"] = js.at[i,"date"] + pd.Timedelta(seconds =  np.random.randint(-3*60*60, 3*60*60))

    week = wk.append(js)
    week.sort_values("ligne", inplace= True)

    #--------- Check if modifying hours faire depasse "date"---------------------------
    #----------------------------------------------------------------------------------#
    new_week_day = week["date"].dt.isocalendar().day
    week["new_week_day"] = new_week_day
    week["diff_date"] = np.int32(week["new_week_day"]) - np.int32(week["week_day"])

    # week.to_csv(f"./data/Week/week_test_initial{10+k}",sep="\t")

    diff_date_week= pd.Series(data= (pd.Timedelta(days = i) for i in week["diff_date"]),index=week["diff_date"].index)

    for i in week.index:
        week.at[i,'date']= week.at[i,'date'] - diff_date_week[i]   # parce qu'on veut la date initial donc "-"

    weeknum2 = week["date"].dt.isocalendar().week                              #get numero de semain  
    week["week_new"] = weeknum2

    for i in week.index:
        if week.at[i,"week"] != week.at[i,"week_new"]:
            week.at[i,"date"] = week.at[i,"date"] + pd.Timedelta(days = 7 * (np.int32(week.at[i,"week"]) -np.int32(week.at[i,"week_new"])))

    # week.to_csv(f"./data/Week/week_test{10+k}",sep="\t")

    #------------------------------------------------------------------------------------#
    #--------- Manipulating days. ------------------------------------
    js= week[week["week_day"] <= 5]                                 # jour de travail
    wk= week.drop(week[week["week_day"] <= 5].index)            # weekend

    #----------------Modify days--------------------------------------------------------
    wk["new_week_day"] = np.random.randint(6,8, size=(len(wk)))                 #new_week_day is the day after changement
    # js["new_week_day"] = np.random.randint(1,6, size=(len(js)))                  #***ici je faire le changement tout dans la range [Lundi, Vendredi] donc il risque des jours diff plus que 2
    
    wk["diff_date"] = wk["new_week_day"] - wk["week_day"]
    # js["diff_date"] = js["new_week_day"] - js["week_day"]
    

    diff_date_wk= pd.Series(data= (pd.Timedelta(days = i) for i in wk["diff_date"]),index=wk["diff_date"].index)
    for i in wk.index:
        wk.at[i,'date']= wk.at[i,'date'] + diff_date_wk[i]

    diff_date_js= pd.Series(data= (pd.Timedelta(days = i) for i in js["diff_date"]),index=js["diff_date"].index) 
    for i in js.index:
        if js.at[i,"week_day"] == 1:
            js.at[i,"date"] = js.at[i,"date"] + pd.Timedelta(days = np.random.randint(0,3))
        else:
            if js.at[i,"week_day"] == 2:
                js.at[i,"date"] = js.at[i,"date"] + pd.Timedelta(days= np.random.randint(-1,3))
            else:
                if js.at[i,"week_day"] == 2:
                    js.at[i,"date"] = js.at[i,"date"] + pd.Timedelta(days= np.random.randint(-2,3))
                else: 
                    if js.at[i,"week_day"] == 3:
                        js.at[i,"date"] = js.at[i,"date"] + pd.Timedelta(days= np.random.randint(-2,3))
                    else:
                        if js.at[i,"week_day"] == 4:
                            js.at[i,"date"] = js.at[i,"date"] + pd.Timedelta(days= np.random.randint(-2,2))
                        else:
                            js.at[i,"date"] = js.at[i,"date"] + pd.Timedelta(days= np.random.randint(-2,1))
        # js.at[i,'date']= js.at[i,'date'] + diff_date_js[i]
    
    wk = wk.drop(columns=["week_day","new_week_day","diff_date"])
    js = js.drop(columns=["week_day","new_week_day","diff_date"])
    # print("----------------weekend------------------")
    # print(wk)
    # print("----------------jour de travail------------------")
    # print(js)

    result = wk.append(js)                              #combine 2 dataframe into 1 df with the size initial
    result = result.sort_values("ligne")                #sort by numero de ligne
    
    # print("----------------result------------------")

    result.reset_index(drop = True, inplace = True)
    result.drop([i for i in result.columns.tolist() if i not in ['ligne','ID', 'date', 'lat', 'lon'] ], axis = 1,inplace = True)
    result.to_csv(f"./data/Week/test2_week_days{10+k}",sep="\t")
    # print(result)

