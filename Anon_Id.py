import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import datetime as dtt

import module.project as project
import random as rd

#Only serves to select the plot theme. can be commented 
import seaborn as sns
sns.set_theme()

#--------------------------- Init
def ids_density_anon(df : pd.DataFrame) :
    """Anonymisations of id density for a week by changing the density function to a step-function.
    """
    id = df["ID"]
    total = len(id)
    data = id.value_counts(sort = True)
    data.name = "count"
    data.index.name = "ID"

    #What we need for our algorithm
    n = len(data)                                                           #This is a constant for the length of the dataset
    i = 0                                                                   #This will be our counter
    step_currentStep = data.iloc[n - (i+1)]                                 #This is the current value of our step function
    ids_currentStep = [data.iloc[[n - (i+1)]].index.tolist()[0]]            #Complicated way of saying we're adding the id which correspond to the count in this list
    count_currentStep = step_currentStep

    #----------------------------   Main algorithm

    while i < n-1 : #While we didn't processed all the ids / datas
        i += 1 
        count_id = data.iloc[n - (i+1)]                                                    #Because the datalist is sorted, we will go through ids in order (from the less present to the more present)
        
        if (n - (i+1)) / n < 0.1: 
            ids_currentStep.append(data.iloc[[n - (i+1)]].index.tolist()[0])
            count_currentStep += count_id
            continue
        
        if ((count_id - step_currentStep )/ step_currentStep) <0.45 :                  #If the difference between two ids' count is not too important, we group them together to create a set of similar count id
            ids_currentStep.append(data.iloc[[n - (i+1)]].index.tolist()[0])
            #We're also updating the number of datas in this step
            count_currentStep += count_id
        elif len(ids_currentStep) < 3 :                                             #If there is too few IDs in a group
            if (count_currentStep / total) < 0.003 :                                 #Either we delete them because they're really insignificant (less than 7% of total datas of this week)
                project.delete(df, ids_currentStep)
                print(f"Delete : {ids_currentStep}")
                step_currentStep = count_id
                count_currentStep = 0 
                ids_currentStep = [data.iloc[[n - (i+1)]].index.tolist()[0]]
            else : 
                p=rd.randint(72,88)*0.01
                for id in ids_currentStep :                                         #Either we reduce them anyway but to a random value (~80%)
                    project.reduceID_to(df,id,round(step_currentStep*p))
                print(f"Rand reduce : {ids_currentStep}")
                step_currentStep = count_id
                count_currentStep = 0 
                ids_currentStep = [data.iloc[[n - (i+1)]].index.tolist()[0]]
        else : 
            print(f"Reduce : {ids_currentStep}")
            for id in ids_currentStep :
                project.reduceID_to(df,id,step_currentStep - 9)
            
            step_currentStep = count_id
            count_currentStep = 0 
            ids_currentStep = [data.iloc[[n - (i+1)]].index.tolist()[0]]
    print(ids_currentStep)

    if len(ids_currentStep) != 0 : 
        print(f"Reduce : {ids_currentStep}")
        for id in ids_currentStep :
                project.reduceID_to(df,id,step_currentStep - 9)
    #-----------------------------  Ending


    id = df["ID"]
    data_end = id.value_counts(sort = True)
    data_end.name = "count end"
    data_end.index.name = "ID"
    print( f"Number of removed rows :  { data_end['DEL'] }, which is { data_end['DEL']/ total * 100}% of the initial database " )
    print(f"Number of ids removed : {n - len(data_end)+1}, which is {(n - len(data_end)+1)/n * 100}% of the initial database")
    data_end.loc["DEL"] = 0


    #-----------------------------  Display result 

    return df