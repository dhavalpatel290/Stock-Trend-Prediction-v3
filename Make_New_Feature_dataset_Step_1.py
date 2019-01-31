# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 11:32:29 2018

@author: Dhaval
"""

import pandas as pd
import datetime

year=2008
cmpindex=4
csvfiles=['','RELIANCEEQN','INFYEQN','HDFCEQN','DRREDDYEQN']
#csvfiles=['RELIANCEEQN']


gotcmpeqn=csvfiles[cmpindex]
ini_df=df=pd.read_csv("./Dataset/01-01-"+str(year-1)+"-TO-31-12-"+str(year-1)+gotcmpeqn+".csv")

for i in range(10):    
    getyear=year+i
    print(getyear,i)
    df=pd.read_csv("./Dataset/01-01-"+str(getyear)+"-TO-31-12-"+str(getyear)+gotcmpeqn+".csv")
    
    ini_df = [ini_df, df]
    ini_df = pd.concat(ini_df)
    
all_df=ini_df
all_df=all_df.reset_index(drop=True)


ini_df=df=pd.read_csv("./Dataset/01-01-"+str(year)+"-TO-31-12-"+str(year)+gotcmpeqn+".csv")
ini_df=ini_df[['Date']]

for i in range(9):
    getyear=year+i+1
    print(getyear)
    df=pd.read_csv("./Dataset/01-01-"+str(getyear)+"-TO-31-12-"+str(getyear)+gotcmpeqn+".csv")
    df=df[['Date']]
    ini_df=[ini_df,df]
    ini_df=pd.concat(ini_df)
    
all_date_df=ini_df
all_date_df=all_date_df.reset_index(drop=True)

#dic={'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}



final_matrix=[]
for i in range(all_date_df.shape[0]):
    gotdate=all_date_df.ix[i,0]
    lis=gotdate.replace('-','/')
    #print(lis)
    startdate =lis 
    date_1 = datetime.datetime.strptime(startdate, "%d/%b/%Y")
    start_date = date_1 - datetime.timedelta(days=365)
    end_date = date_1 - datetime.timedelta(days=1)
    #print(start_date)
    #print(end_date)
    got_own_open_price=0
    min_close=100000000
    max_close=-1
    min_date=gotdate
    max_date=gotdate
    
    for j in range(all_df.shape[0]):
        in_date=all_df.ix[j,2]     # date column
        lis=in_date.replace('-','/')
        my_date = datetime.datetime.strptime(lis, "%d/%b/%Y")
        
        if(my_date>=start_date and my_date<=end_date):
            my_close=float(all_df.ix[j,8])   # close price column
            if(my_close>=max_close):
                max_close=my_close
                max_date=in_date
            if(my_close<=min_close):
                min_close=my_close
                min_date=in_date
        
        if(date_1==my_date):
            got_own_open_price=float(all_df.ix[j,4])    #open price column
        
        if(my_date>end_date):
            break
        
    
    final_row_to_append=[]
    final_row_to_append.append(gotdate)
    final_row_to_append.append(got_own_open_price)
    final_row_to_append.append(min_date)
    final_row_to_append.append(min_close)
    final_row_to_append.append(max_date)
    final_row_to_append.append(max_close)
    print(final_row_to_append)
    final_matrix.append(final_row_to_append)
    
    
    
    
#print(final_matrix)  
labels = ['Date', 'Today_Open','Min_Date', 'Min_Close', 'Max_Date','Max_Close']
df = pd.DataFrame.from_records(final_matrix, columns=labels)  

df.to_csv("All_year_Feature_"+gotcmpeqn+".csv",index=False)

    
  