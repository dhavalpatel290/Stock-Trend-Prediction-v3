# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 13:08:57 2018

@author: Dhaval
"""

import pandas as pd
import datetime

year=2008
cmpindex=4
csvfiles=['','RELIANCEEQN','INFYEQN','HDFCEQN','DRREDDYEQN']
#csvfiles=['RELIANCEEQN']


gotcmpeqn=csvfiles[cmpindex]

feature_df=pd.read_csv("./All_year_Feature_"+gotcmpeqn+".csv")
final_matrix=[]



in_date=feature_df.iloc[0,0]     # Date column
split_year=in_date.split('-')
prev_year=int(split_year[2])

today_c=float(feature_df.iloc[0,1])
min_c=float(feature_df.iloc[0,3])
max_c=float(feature_df.iloc[0,5])
add_feature=0   # Just to initialize
if(today_c<min_c):
    add_feature=0
elif(today_c<max_c):
    add_feature=(today_c-min_c)/(max_c-min_c)
else:
    add_feature=1
one=[]
one.append(in_date)
one.append(add_feature)

final_matrix.append(one)


for i in range(1,feature_df.shape[0]):
    in_date=feature_df.iloc[i,0]     # Date column
    split_year=in_date.split('-')
    current_year=int(split_year[2])
    if(current_year==prev_year):
        today_c=float(feature_df.iloc[i,1])
        min_c=float(feature_df.iloc[i,3])
        max_c=float(feature_df.iloc[i,5])
        add_feature=0
        if(today_c<min_c):
            add_feature=0
        elif(today_c<max_c):
            add_feature=(today_c-min_c)/(max_c-min_c)
        else:
            add_feature=1
        one=[]
        one.append(in_date)
        one.append(add_feature)      
        final_matrix.append(one)
    else:
        labels = ['Date', 'MinMax_Feature']
        print("Made year  "+str(prev_year))
        df = pd.DataFrame.from_records(final_matrix, columns=labels)  
        df.to_csv("./Dataset/NewFeature_01-01-"+str(prev_year)+"-TO-31-12-"+str(prev_year)+gotcmpeqn+".csv",index=False)
        final_matrix=[]
        
        in_date=feature_df.iloc[i,0]     # Date column
        split_year=in_date.split('-')
        prev_year=int(split_year[2])
        
        today_c=float(feature_df.iloc[i,1])
        min_c=float(feature_df.iloc[i,3])
        max_c=float(feature_df.iloc[i,5])
        add_feature=0
        if(today_c<min_c):
            add_feature=0
        elif(today_c<max_c):
            add_feature=(today_c-min_c)/(max_c-min_c)
        else:
            add_feature=1
        one=[]
        one.append(in_date)
        one.append(add_feature)
        
        final_matrix.append(one)
        
        prev_year=current_year
    

labels = ['Date', 'MinMax_Feature']
print("Made year  "+str(current_year))
df = pd.DataFrame.from_records(final_matrix, columns=labels)  
df.to_csv("./Dataset/NewFeature_01-01-"+str(current_year)+"-TO-31-12-"+str(current_year)+gotcmpeqn+".csv",index=False)
 