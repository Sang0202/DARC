import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import datetime as dtt
import hashlib

#ids hash example 

# original_df = pd.read_csv("./data/Week/week18")                                                                              #I choose this week because of the low data density. 
# df = original_df[:1000000]                                                                                                   #Let's choose a subset of our dataframe



#-------------------------------------------- Let's work with a function
def hash_id(df, key) : 
    df['ID'] = df["ID"].astype(str)                                                                                 #First we convert our IDs to strings 
    df['ID'] = df["ID"].apply(
        lambda x : 
            hashlib.sha256((x+key).encode()).hexdigest()
    )
#-----------------------------------------------------------------------



# hash_id(df,"key")                                                                                                          #Doing our test
# print(df)                                                                                                              
# print("-------------------------------------")
# print(df['ID'].drop_duplicates())                                                                                          #On a first sight it's working
