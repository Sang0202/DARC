import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import datetime as dtt

import Anon_Id
import hash_id
import floutagetrace
import random as rd

"""This file aims to regroup different methods to create a full anonymisation
    - Louis
"""


#-------------------------------------------- Initialization

#Let's create an array containing different dataframes
Anon_df_week = []
for k in range(11) : 
    df = pd.read_csv(f"./data/Week/week{10+k}")             #As I don't have anonymized df I use the originals ones
    Anon_df_week.append(df) 


#------------------------------------------- Anonymisation

#--------------------------------------------------Warning !!!!------------------------------------------------------------------
# Here are the keys for the hash, it must be hidden before sharing
keys = ["Sous le pont Mirabeau coule la Seine et nos Amours, Faut-il qu'il m'en souvienne, la joie venait toujours après la peine.","Mains dans les mains restons face à face Tandis que sous Le pont de nos bras passe Des éternels regards l'onde si lasse", "L'amour s'en va comme cette eau courante L'amour s'en va Comme la vie est lente Et comme l'Espérance est violente","Passent les jours et passent les semaines Ni le temps passé Ni les amours reviennent Sous le pont Mirabeau coule la Seine", \
"L'anémone et l'ancolie Ont poussés dans le jardin Où dort la mélancolie Entre l'amour et le dédain", "Il y vient aussi nos ombres Que la nuit dissiperas Le soleil qui les rends sombres Avec elles disparaîtra", "Les déités des eaux vives Laissent couler leurs cheveux Passe il faut que tu poursuives Cette belle ombre que tu veux", \
"On aime d'abord par hasard, par jeu, par curiosité Pour avoir dans un regard Lu des possibilités", "Et puis comme au fond de soi même On s'aime beaucoup Si quelqu'un vous aime, on l'aime par conformité de gout", "On se rend grâce et on s'invite A partager ses moindres maux On prend l'habitude vite, de s'échanger de petits mots", "Quand on a longtemps dit les mêmes On les redit sans y penser et alors, mon Dieu, on aime Parce qu'on a commencé"]
#--------------------------------------------------------------------------------------------------------------------------------

for df in Anon_df_week : 
    hash_id.hash_id(df,keys.pop())
    floutagetrace.floutagetrace(df)
    Anon_Id.ids_density_anon(df)                                                #id density must be anonymized at the very end.  



#------------------------------------------- Formatting data
#Let's concatenate all the anons dataframe together
final_df = pd.concat(Anon_df_week)

#And then we'll sort our dataframe by using the ex index column and clean the dataframe 
def cleaning(df) : 
    df.sort_values("Unnamed: 0",inplace = True)
    df.reset_index(drop = True, inplace = True)
    df.drop([i for i in df.columns.tolist() if i not in ['ID', 'date', 'lat', 'lon'] ], axis = 1,inplace = True)

cleaning(final_df)

final_df.to_csv("./data/Anon_test", header= False, index= False, sep = "\t")  # The output files IS NOT a csv, it is separated by tabulations 
