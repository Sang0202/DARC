import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import datetime as dtt
import os

from pandas.core.arrays.integer import Int64Dtype

"""
For each week, let's get a list of ids used, i'll get that in a 69x69 matrix form probably.

"""

#We will use a bijection so that every id is in the range 0, 69
#I'll use their order of apparitions in the original db to do that
#for that I used data/ID_Apparitions.csv
#I'll use a list to get both the index/position and id nb. 
bijection =  np.genfromtxt("./data/np_bijection.txt",dtype=int).tolist()

#---------------------------------------- Creating Matrix if she dont exist

if not os.path.exists("./data/np_matrix_id.txt") : 
    matrix = np.zeros((10,69))                                                  #Let's create the matrix within we'll stock our results.

    for k in range(10) : 
        week = pd.read_csv(f"./data/Week/week{10+k}")                            #For each week df we got
        idf = week["ID"].drop_duplicates()
        print(f"For week {10+k} the ids found are :")
        print(idf)                                                              #Let's print ids list

        for id in idf : 
            i = bijection.index(id)
            matrix[k][i] = 1                                                   #Let's represent the id i in week number w by the coefficient on row i and column w (one if the id's present this week 0 otherwise)

    np.savetxt("./data/np_matrix_id.txt",matrix)
#--------------------------------------- Else we download the file
else : 
    matrix = np.genfromtxt("./data/np_matrix_id.txt",dtype =int)

#------------------------------------- Once we got the Matrix, we know what IDs are present each week
# Dynamic consultation for each week 

loop = True
while loop :
    print("Please enter the week number (0-9) to know the database content of this week  (q for quit) : ", end="")
    wk_nb = input("")
    if not (wk_nb in ['0','1','2','3','4','5','6','7','8','9']) : 
        loop = False
        break
    
    wk_nb = int(wk_nb)
    print("IDs of this week are :")
    for k in  range(68):
        if int(matrix[wk_nb][k]) == 1 :
            print(f"- {bijection[k]}")

