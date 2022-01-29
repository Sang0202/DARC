import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import datetime as dtt

import module.project as project
from math import floor
import random as rd

""" A set of functions to anonymize positions (columns lon and lat)
    - Louis 
"""

def Anon_pos(df,column = "lon") : 
    sp = df[column]

    # The border of positions for this week
    min_pos = sp.min()
    print(f"min : {min_pos}")
    max_pos = sp.max()

    # The set in which our delta_p can be
    min_dp =0.01                                                             
    max_dp =0.09                                                             

    #  Our partition of space 
    P_partition = []

    #  The current value of position 
    P_current = min_pos                                                         
    delta_P = min_dp                                                            
    var_P = 0.01                                                             

    # count how many Id in the delta_p
    count_nb_id = 0 

    while min_pos <= P_current <= max_pos : 
        #Let's find an adaptative partition
        P_partition.append(P_current)

        #reset for every space interval
        count_nb_id = 0
        delta_P = min_dp
         
        while count_nb_id < 3 and delta_P <= max_dp : 

            # ------------------------------------------ In first place I check that a solution exist 

            index_pos = sp[ (P_current <= sp) & ( sp < P_current + max_dp ) ].index.to_list()
            count_nb_id = df.loc[index_pos, "ID"].drop_duplicates().count() 
            if count_nb_id < 3 : 
                print(f"delete {count_nb_id} IDs next to {P_current} ")
                project.deleteRows(df, index_pos)
                P_current += max_dp
                break

            # ------------------------------------------ End Test
            

            #Here we count until we found a partition 
            index_pos = sp[ (P_current <= sp) & ( sp < P_current + delta_P ) ].index.to_list()
            count_nb_id = df.loc[index_pos, "ID"].drop_duplicates().count() 
            
            #success
            if count_nb_id >= 3 : 
                print(f"Anonymization of {count_nb_id} IDs next to {P_current}")
                meanP = floor(P_current + delta_P/2)
                df.loc[index_pos, column] = df.loc[index_pos, column].apply(project.modif_pos,args=(meanP,))
                P_current += delta_P
                break
            #faillure  
            elif delta_P > max_dp:
                print(f"delete {count_nb_id} IDs next to {P_current} ")
                project.deleteRows(df, index_pos)
                P_current += delta_P
                break

            else : 
                print("increase")
                delta_P += var_P
    return df


if __name__ == "__main__" : 
    df = pd.read_csv("./data/Week/week18")
    print("start Anon")
    df2 = Anon_pos(df)
    print(df)
    df.to_csv("./data/Anon/pos_test.csv")

