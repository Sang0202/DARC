# Statistic study of the data base



## Basic considerations

There is **any missing value** in the Database. 

There is a total of ==34551849== rows. 



## Participation 

There is ==69 distincts participants== in the study. They are randomly numeroted from 1 to 110

![Apparition_By_Id](C:\Users\louis\Desktop\Cours\STI 4A\Projet Anon\Image\Apparition_By_Id.png)

There is a huge difference in IDs distribution with the 4th ID having way more value than any other

----------------------------------------

## Time considerations 

### By days

The study [spans 70 days]() with data ==irregularly distributed== over time. 



![Entries per day](C:\Users\louis\Desktop\Cours\STI 4A\Projet Anon\Image\Entries per day.png)

It lasts exactly ==10 weeks==. [The first week is the 10th]() of 2015 and [the last one is the 20th](). 



**IDs are not uniform** neither through times. There is no day where all the 69 IDs are together and there is some days where  there is less than 20 IDs sending datas. 

![ID_per_day](C:\Users\louis\Desktop\Cours\STI 4A\Projet Anon\Image\ID_per_day.png)

----------------------

## Space distribution 

All data space distribution : 

![Space_distr](C:\Users\louis\Desktop\Cours\STI 4A\Projet Anon\Image\Space_distr.PNG)

Most the value are concentrated in the center of the graph (ie [-5 ; 25] lat and [35 ; 50] lon )

## Weeks 



### 1st week

| Number of Entries | Number of IDs |
| :---------------: | :-----------: |
|      4423812      |      64       |

![ID_Week10](C:\Users\louis\Desktop\Cours\STI 4A\Projet Anon\Git_rep\Image\ID_Week10.png)

![Week10_loc](C:\Users\louis\Desktop\Cours\STI 4A\Projet Anon\Image\Week10_loc.png)

More than 90% of the values for this weeks are in this interval (41 : 47 lon / -1 : 6 lat )

==99.99% of the value in the range  : -6 / 17 lat 40 / 51 lon (only one value missing )==

Missing value : 

```
         Unnamed: 0  ID                 date        lat        lon  week
1054258     6977422  42  2015-03-05 16:53:32 -46.863902  19.586862    10
```



![Week10_loc2](C:\Users\louis\Desktop\Cours\STI 4A\Projet Anon\Image\Week10_loc2.png)

---------------------------------------

First week Map : 
![Week10](C:\Users\louis\Desktop\Cours\STI 4A\Projet Anon\Git_rep\Image\Week10.png)



### 2nd week

| Number of Entries | Number of IDs |
| :---------------: | :-----------: |
|      5323266      |      59       |

![ID_Week11](C:\Users\louis\Desktop\Cours\STI 4A\Projet Anon\Git_rep\Image\ID_Week11.png)

![Week11](C:\Users\louis\Desktop\Cours\STI 4A\Projet Anon\Git_rep\Image\Week11.png)

### 3rd week

| Number of Entries | Number of IDs |
| :---------------: | :-----------: |
|      3953157      |      51       |

![ID_Week12](C:\Users\louis\Desktop\Cours\STI 4A\Projet Anon\Git_rep\Image\ID_Week12.png)

![Week12](C:\Users\louis\Desktop\Cours\STI 4A\Projet Anon\Git_rep\Image\Week12.png)

### 4th week

| Number of Entries | Number of IDs |
| :---------------: | :-----------: |
|      4779681      |      48       |

![ID_Week13](C:\Users\louis\Desktop\Cours\STI 4A\Projet Anon\Git_rep\Image\ID_Week13.png)

![Week13](C:\Users\louis\Desktop\Cours\STI 4A\Projet Anon\Git_rep\Image\Week13.png)

### 5th week 

| Number of Entries | Number of IDs |
| :---------------: | :-----------: |
|      3335285      |      42       |

![ID_Week14](C:\Users\louis\Desktop\Cours\STI 4A\Projet Anon\Git_rep\Image\ID_Week14.png)

![Week14](C:\Users\louis\Desktop\Cours\STI 4A\Projet Anon\Git_rep\Image\Week14.png)

### 6th week 

| Number of Entries | Number of IDs |
| :---------------: | :-----------: |
|      3409012      |      37       |

![ID_Week15](C:\Users\louis\Desktop\Cours\STI 4A\Projet Anon\Git_rep\Image\ID_Week15.png)

![Week15](C:\Users\louis\Desktop\Cours\STI 4A\Projet Anon\Git_rep\Image\Week15.png)

### 7th week 

| Number of Entries | Number of IDs |
| :---------------: | :-----------: |
|      2669607      |      38       |

![ID_Week16](C:\Users\louis\Desktop\Cours\STI 4A\Projet Anon\Git_rep\Image\ID_Week16.png)

![Week16](C:\Users\louis\Desktop\Cours\STI 4A\Projet Anon\Git_rep\Image\Week16.png)

### 8th week 

| Number of Entries | Number of IDs |
| :---------------: | :-----------: |
|      2091657      |      31       |

![ID_Week17](C:\Users\louis\Desktop\Cours\STI 4A\Projet Anon\Git_rep\Image\ID_Week17.png)

![Week17](C:\Users\louis\Desktop\Cours\STI 4A\Projet Anon\Git_rep\Image\Week17.png)

### 9th week 

| Number of Entries | Number of IDs |
| :---------------: | :-----------: |
|      2027239      |      30       |

![ID_Week18](C:\Users\louis\Desktop\Cours\STI 4A\Projet Anon\Git_rep\Image\ID_Week18.png)

![Week18](C:\Users\louis\Desktop\Cours\STI 4A\Projet Anon\Git_rep\Image\Week18.png)

### 10th week

| Number of Entries | Number of IDs |
| :---------------: | :-----------: |
|      2241444      |      30       |

![ID_Week19](C:\Users\louis\Desktop\Cours\STI 4A\Projet Anon\Git_rep\Image\ID_Week19.png)

<img src="C:\Users\louis\Desktop\Cours\STI 4A\Projet Anon\Git_rep\Image\Week19.png" alt="Week19" style="zoom:100%;" />

## Sum up 

![Id_per_week](C:\Users\louis\Desktop\Cours\STI 4A\Projet Anon\Image\Id_per_week.png)

![Entries_per_week](C:\Users\louis\Desktop\Cours\STI 4A\Projet Anon\Image\Entries_per_week.png)

​	

The disparity in Id's data by week must absolutely be handle. By attacking with those data (% of apparitions for each id we can easily detect which Anon-Id correspond to which Id  = [frequency analysis]() ) 

IDEA : Bring the Apparitions by Ids and Week a scale function : ie regroup ID that have roughly the same magnitude (for example Week 19 we could regroup the 8 les dense IDs). 

