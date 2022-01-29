import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import datetime as dtt
import random as rd

"""
Module gathering several functions to use anytime.  

inspired by INSAnonym-utils
"""

#--------------------------------------------------- To Delete Rows
def delete(df, ids_list) : 
    """Replace all the id in ids_list by "DEL"
    df: dataframe to modify
    ids_list: list
    """
    ids = df["ID"].replace(ids_list, "DEL")
    df["ID"] = ids


def reduceID_to(df,id,n) : 
    """Reduce the number of entries in the dataframe "df" for the "id" to "step"

        df: dataframe to modify
        id: id to modify
        n: final number of entries
    """
    index_list = df[df["ID"] == id].index.to_list()
    index_to_delete = rd.sample(index_list,len(index_list) - n)                   #We're randomly choosing the rows to delete, they are all considered as important (Maybe we could handle an exclusion a several rows which would be important)
    df.loc[index_to_delete, "ID"] = "DEL"

def deleteRows(df, index_list) : 
    """Replace all the rows from "df" where index in "index_list" by "DEL"

        df : dataframe to modify
        index_list : object as df[expr].index.to_list()
    """
    df.loc[index_list, "ID"] = "DEL"

def deleteClean(df) : 
    """Clean the df "DEL" Rows so you don't give informations to the attacker 
    """
    index_list = df[df["ID"] == "DEL"].index.to_list()
    df.loc[index_list, ["lat","lon"]] = 0
    random_day = pd.to_datetime(df.sample()["date"]).dt.strftime("%Y-%m-%d 19:19:42").iloc[0]
    df.loc[index_list, "date"] = random_day



#-------------------------------------------------- For Date and hours manipulation 
def hour_manip(fhour) : 
    """ To manipulate easier hour format, Let's convert a string from strformat to a seconds homogeneous integer

        fhour : "%H:%M:%S"
        """
    count = 0
    L = fhour.split(':')                            #I absolutely don't handle errors, be careful
    count += int(L[0])* 3600                        #hours
    count += int(L[1])* 60                          #minutes
    count += int(L[2])                              #seconds
    return count

def inv_hour_manip(phour) :
    hours = phour// 3600
    phour -= hours * 3600
    minutes = phour// 60
    phour -= minutes * 60
    seconds = phour

    return f"{hours}:{minutes}:{seconds}"

def modif_hour(date, pshour) : 
    """Modify a 'date' which is actually an hour so it is close to 'pshour' 
    """
    phour = hour_manip(pd.to_datetime(date).strftime("%H:%M:%S")) 
    modif = rd.choice(list(range(-150,0)) + list(range(1,151)))                                                              #I had a bit of interference
    delta = pd.to_timedelta(inv_hour_manip(phour - pshour + modif ))
    return pd.to_datetime(date) - delta

#------------------------------------------------------------ For position manipulations

def modif_pos(pos, spos) : 
    """Modify a 'pos' in columns lon or lat so it is close to 'spos' 
    """
    modif = rd.choice(list(range(-90,0)) + list(range(1,91)))                                                              #I had a bit of interference
    return spos - modif * 0.0001

    
