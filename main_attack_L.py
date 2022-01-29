"""
Program which : 
    -initialize db
    -create and formate to json the attack file 

#Louis Descamps
"""
import pandas as pd 
import numpy as np 
import sys
import json
import time

import Reindentification.constant as cst
from Reindentification.frequential_analysis import compatibility
from Reindentification.closest import zone, d, score

start = time.process_time_ns()
#-------------------------------------------------Constant and initialization-------------------------------------------


#All IDs list
ID_list = cst.ID_list
#week_list[k] is the list of week in which ID
week_list = cst.week_list
#A fitting dictionnary which looks like the json files
final_dic = {ID_list[k] : {week : [] for week in week_list[k]} for k in range(len(ID_list)) }



#Look for an argument in the command line (which is the bath to the anonimized db)
if len(sys.argv) != 2 :
    print("Usage : py -3 main_attack_L.py [Path to anonimized database]")
    exit()
anon_df_path = sys.argv[1]

#reading databases 
df = pd.read_csv("./INSAnonym/bd.csv", sep="\t", names=["ID","date","lat","lon"] )
anon_df = pd.read_csv(anon_df_path, sep="\t", names=["ID","date","lat","lon"] )



print(f"fin de la lecture des dataframes: {time.process_time_ns() - start}.")


#                                   formatting dataframes
#        ===========================================================================        #Anon df from here  
Adf = anon_df.loc[anon_df["ID"]!="DEL"].copy()                                              #
del anon_df                                                                                 #
Adf.loc[:,"date"] = pd.to_datetime(Adf["date"], format ="%Y-%m-%d %H:%M:%S")                #
Adf.loc[:, ["lon","lat"]] = Adf.astype({"lon" : "float64", "lat" : "float64"})              #
Aweek = Adf["date"].dt.isocalendar().week.astype('object')                                                    #
for k in range(11):                                                                         #
    Aweek.replace(10+k,f"2015-{k:02d}",inplace= True)                                       #
Adf["week"] = Aweek                                                                         #To here
del Aweek

#        ===========================================================================        #Original df from here   
Odf = df                                                                                   #
Odf.loc[:,"date"] = pd.to_datetime(Odf["date"], format= "%Y-%m-%d %H:%M:%S")                #
Odf.loc[:, ["lon","lat"]] = Odf.astype({"lon" : "float64", "lat" : "float64"})              #
week = Odf["date"].dt.isocalendar().week.astype('object')                                   #
for k in range(11):                                                                         #
    week.replace(10+k,f"2015-{k:02d}",inplace= True)                        #
Odf["week"] = week                                                                          #To here
del week




print(f"Fin de l'initialisation : {time.process_time_ns() - start}")




#------------------------------------------------Calling the other algorithms---------------------------------------------




#Write your code here
compatibility(Odf, Adf,final_dic)
print(f"Fin de l'étude frequentielle : {time.process_time_ns() - start}")

#From now on we will work on a particular week : 
for w in cst.WEEKS :
    print(f"week {w} : {time.process_time_ns() - start}")
    weekdf =  Odf[Odf["week"]==w]
    listids = weekdf["ID"].drop_duplicates().tolist()
    weekAdf = Adf[Adf["week"]==w]                                                    #We can use index to update and distance later 

    #Now let's check what ID we have to study closer : 
    for id in listids : 
        print(f"id : {id}")
        if len(final_dic[id][w]) == 0 : #If there is any Aid fitting the current studied Id we just pass our turn 
            final_dic[id][w] = ["DEL"]
            continue
        
        desirables=[desirableAId for (desirableAId,_) in final_dic[id][w]]
        Fdf_score = pd.DataFrame({'score' : np.zeros(len(desirables))}, index = desirables )
        sampledWeek = weekdf[weekdf["ID"] == id].sample(cst.smpl)             #I'll study only a few points out of this 

        for k in range(len(sampledWeek)) : 
            current_row = sampledWeek.iloc[k]
            #print(f"current row : {current_row} ")
            researchZone = zone(current_row,weekAdf, desirables )
            #print(f"researchzone :  { researchZone}")
            if researchZone.empty : 
                del researchZone, current_row
                continue
            researchZone["d"] = researchZone.apply(d, args=(current_row, ),axis = 1 )
            researchZone["score"] = researchZone["d"].apply(score)
            df_score = researchZone.loc[:, ["ID","score"]].groupby("ID").mean() #groupby aid 
            Fdf_score = Fdf_score.add(df_score,axis = 0,fill_value = 0)
            del researchZone,df_score, current_row
        
        Fdf_score = Fdf_score.mul(np.full(len(desirables), 1/cst.smpl), axis = 0, fill_value = 0) #On fait une moyenne
        doublets = final_dic[id][w]

        for doublet in doublets : 
            aid, freq_score = doublet 
            if aid not in desirables : 
                continue
            Fdf_score.at[aid,"score"] *= freq_score
        
        if len(Fdf_score[Fdf_score["score"]> 0.90]) >0: 
            final_dic[id][w] = Fdf_score[Fdf_score["score"]> 0.90].index.tolist()
        elif len(Fdf_score[Fdf_score["score"]> 0.55]) >3  :
            final_dic[id][w] = Fdf_score.sort_values(by="score", ascending=False).iloc[:3].index.tolist()
        elif 0 < len(Fdf_score[Fdf_score["score"]> 0.55]) <=3  : 
            final_dic[id][w] = Fdf_score[Fdf_score["score"]> 0.49].index.tolist()
        elif len(Fdf_score[Fdf_score["score"]> 0.15]) : 
            final_dic[id][w] = Fdf_score.sort_values(by="score", ascending=False).iloc[:3].index.tolist()
        else : 
            final_dic[id][w] = ["DEL"]

        











print(f"fin du traitement : {time.process_time_ns() - start}")




#-----------------------------------------------Formatting the output file ----------------------------------------------

json_obj = json.dumps(final_dic, indent=4)
print(json_obj)
with open(f"{ anon_df_path}_attack.json", 'w') as f: 
        f.write(json.dumps(final_dic,indent=4))

end = time.process_time_ns()
print(f"Fin du traitement : {end-start}ns")  
