import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import datetime as dtt

import module.project as projects
from math import floor
import random as rd

""" A set of functions to anonymize date and hours (date column)
    - Louis 
    """ 

def hour_manip(fhour) : 
    """ To manipulate easier hour format, Let's convert a string from strformat to a seconds homogeneous integer

        fhour : "%H:%M:%S"
        """
    count = 0
    L = fhour.split(':')                            #I absolutely don't handle errors, be careful
    count += int(L[0])* 3600                         #hours
    count += int(L[1])* 60                          #minutes
    count += int(L[2])                              #seconds
    return count


        

def Anon_hour_density(df) :  
    """Anonymize hours by regrouping, deleting and moving in a range of -3 +3hours 
    """             
    #We'll anonymize data by regrouping hours and days. Let's try to stay into the same 

    #--------------------------------------------------------------------------------- Initialization 
    
    hours = pd.to_datetime(df["date"]).dt.strftime("%H:%M:%S")                                  #modulo 24 basis 
    dfH = pd.DataFrame({'readable' : hours, 'manip' : hours.apply(hour_manip)}) 

    # The set in which our delta_t can be
    min_dt = hour_manip("00:45:00")                                                             #dtt.datetime(minutes = 30)
    max_dt = hour_manip("01:45:00")                                                             #dtt.datetime(hours = 1, minutes= 45)

    #  Our partition of time 
    T_partition = []

    #  The current value of time 
    T_current = hour_manip(hours.min())                                                          #minimum hour time in the df 
    delta_T = hour_manip("00:45:00")                                                             #dtt.datetime(minutes = 25)
    var_T = hour_manip("00:15:00")                                                               #dtt.datetime(minutes= 10)

    # count how many Id in the delta_t
    count_nb_id = 0 

    #---------------------------------------------------------------------------------- Main Loop

    loop24 = True
    loopDelta = True
    print("End Init")
    while loop24 :                                         #While we didn't do the 24h - loop 
        print(f"Current time = {T_current}")

        T_partition.append(T_current)                      #We add the current value (edge of the interval for each delta_t) 
        
        count_nb_id = 0                                    #We reset used variables
        delta_T = hour_manip("00:45:00") 

        while loopDelta : 
            
            index_hours = dfH[ (T_current <= dfH['manip']) & ( dfH['manip'] < T_current + delta_T ) ].index.to_list()
            count_nb_id = df.loc[index_hours, "ID"].drop_duplicates().count()

            # ---------------- Halt Cases Delta Loop 
            # Success 
            if count_nb_id >= 4 and delta_T >= min_dt :                          # ----- ⚠ ----- Parameters : can be changed to calibrate the algorithm
                """
                If there is enough density, let's regroup the datas on the same tiles 
                """
                print(f"Anonymization : Number of ID {count_nb_id}")
                meanH = floor( T_current + delta_T/2 ) 
                df.loc[index_hours,'date'] = df.loc[index_hours,'date'].apply(projects.modif_hour, args=(meanH,))
                T_current += delta_T 
                break
            
            # Failure
            elif delta_T > max_dt :                                              # ----- ⚠ ----- Same
                """
                If the density is too weak aka delta_T too large for a count_nb_id too small, then we delete every concerned row 
                """
                print(f"Deleting {count_nb_id} ids")
                projects.deleteRows(df,index_hours)   
                T_current += delta_T 
                break

            # ---------------    
            
            #If there is no stop I increase my interval 
            delta_T += var_T 
        
        if T_current > hour_manip("23:59:59") : 
            print(T_current)
            loop24 = False
    
    return df, T_partition


def Anon_days_density(df,T_Partition) :
    """Anonymize 'df' by changing days in a range of +-2 days, so there is enough density in each segment of T_Partition
    """
    #Let's check the density evaualting by hours and day not just by hours. 
    hours = pd.to_datetime(df["date"]).dt.strftime("%H:%M:%S")
    dfD = pd.DataFrame({'hour' : hours.apply(hour_manip), 'day' : pd.to_datetime(df['date']).dt.dayofweek})      #We create a dataframe 

    #Var I'll be using
    count_nb_id = 0
    state_matrix = np.full((7,len(T_Partition)+2), -100)   #Let's create an array to optimize complexity (and to avoid doing twice the same count)
    index_matrix = np.frompyfunc(list, 0, 1)(np.empty((7,len(T_Partition)+2), dtype=object))
    """
    the (m,n) coefficient of the matrix will turn to True(1 or more) if and only if there is more than enough ids in that time interval (for the day nb 'm' and interval number 'n')
    It'll be equal to disponible_ids = count_nb_ids - 5 (so if there is just enough value ) 
    """

    # ------------ Here, I handle edge effects
    T_Partition.append( hour_manip("23:59:59") +1)

    for d in range(7) : #For every day in a week
        for ih in range(len(T_Partition) -1) :

            # ------------ Reset local variables
            count_nb_id = 0


            index_days = dfD[ (T_Partition[ih] <= dfD['hour']) & ( dfD['hour'] < T_Partition[ih+1]) & (dfD["day"] == d) ].index.to_list()    #We choose every value for a day AND in an hour interval
            count_nb_id = df.loc[index_days, "ID"].drop_duplicates().count()                                                 #Int which is number of IDs present on that time. 

            # On this step we just fill the matrixes           
            state_matrix[d][ih] = count_nb_id - 5   
            if (count_nb_id - 5) <0 : 
                index_matrix[d][ih] = index_days

    print(state_matrix)

    #let's now check on the matrix 
    for d in range(7) : 
        for ih in range(len(T_Partition)-1) : 

            #--------------- There is enough density 
            if state_matrix[d][ih] >= 0 : 
                pass
            
            #-------------- There is too few IDs
            else : 
                okay = False     #That's the case where it's not okay 
                Ls = [[1,2],[-1,1,2],[-2,-1,1,2],[-2,-1,1],[-2,-1],[1],[-1]] #List of possibles moves for a day  (for day nb d possibles moves are Ls[d])

                L = Ls[d] 
                rd.shuffle( L ) # I randomly choose the order of search 

                index_days = index_matrix[d][ih] # I gonna need that soon 

                for k in L :
                    if state_matrix[d + k][ih] + state_matrix[d][ih] >= 0 : 
                        tdelta = pd.to_timedelta(f"{k}d")
                        df.loc[index_days,'date'] = df.loc[index_days,'date'].apply( lambda d : pd.to_datetime(d) + tdelta)
                        okay = True

                        #We must update our matrix 
                        state_matrix[d + k][ih] += state_matrix[d][ih] + 5 
                        print(f"Anonymized {d},{ih}")
                        break
                if not okay :  
                    projects.deleteRows(df,index_days)
                    print(f"Delete {d},{ih}")
                
                #In any case, at the end, there is no more ids in that time interval 
    
                state_matrix[d][ih] = -5 
    
    return df

                        

    
if __name__ == "__main__" : 
    df = pd.read_csv("./data/Week/week18")
    df2 , T_Partition = Anon_hour_density(df)
    print(T_Partition)
    print(len(T_Partition))
    Anon_days_density(df,T_Partition)
    df.to_csv("./data/Anon/Date_test.csv")
    
