# -*- coding: utf-8 -*-
"""
Created on Tue May  1 18:32:44 2018

@author: Dhaval
"""

import numpy as np
import os
import pandas as pd



def compute_all_fmea(mode,noofepoch,noofnode,fold):
    All_final=0
    for i in range(len(noofepoch)):        
        #print(noofnode[i])
        if(mode==0):
            putpath=fold+'\Results\Epoch_'+str(noofepoch[i])+'\\Nodes_'+str(noofnode[0])+'\\Nodes_'+str(noofnode[0])+'_Epoch_'+str(noofepoch[i])+'_All_Efficiency_Of_Training.csv'
        elif(mode==1):
            putpath=fold+'\Results\Epoch_'+str(noofepoch[i])+'\\Nodes_'+str(noofnode[0])+'\\Nodes_'+str(noofnode[0])+'_Epoch_'+str(noofepoch[i])+'_All_Efficiency_Of_Testing.csv'
        
        #print(putpath)
        df=pd.read_csv(putpath)
        #print(df)
        final=df.iloc[3:4,:]
        for j in range(1,10):
            
            if(mode==0):
                putpath=fold+'\Results\Epoch_'+str(noofepoch[i])+'\\Nodes_'+str(noofnode[j])+'\\Nodes_'+str(noofnode[j])+'_Epoch_'+str(noofepoch[i])+'_All_Efficiency_Of_Training.csv'
            elif(mode==1):
                putpath=fold+'\Results\Epoch_'+str(noofepoch[i])+'\\Nodes_'+str(noofnode[j])+'\\Nodes_'+str(noofnode[j])+'_Epoch_'+str(noofepoch[i])+'_All_Efficiency_Of_Testing.csv'
            
            print(putpath)
            df=pd.read_csv(putpath)
            df=df.iloc[3:4,:]
            final = pd.concat([final, df], axis=0)
        final=final.reset_index()
        #print("Display before : ")
        #print(final)
        final=final.iloc[:,1:]
        #print("Display after : ")
        #print(final)
        
        
        
        if(mode==0):
            path = fold+'/All_Results/Training'   # if folder doesn't exists then create new folder
        elif(mode==1):
            path = fold+'/All_Results/Testing'   # if folder doesn't exists then create new folder
           
        if not os.path.exists(path):
            os.makedirs(path)    
        
        if(mode==0):
            final.to_csv(path+'/ALL_Results_for_Epoch_'+str(noofepoch[i])+'.csv', sep=',',index=False) 
        elif(mode==1):
            final.to_csv(path+'/ALL_Results_for_Epoch_'+str(noofepoch[i])+'.csv', sep=',',index=False) 
        

        if(i==0):  # for first initiallization
            All_final=final
        else:
            All_final = pd.concat([All_final, final], axis=0)
        
    if(mode==0):
        All_final.to_csv(path+'/ALL_Combined_Results_Of_Training.csv', sep=',',index=False) 
    elif(mode==1):
        All_final.to_csv(path+'/ALL_Combined_Results_Of_Testing.csv', sep=',',index=False) 
    
    result=np.array(All_final)
    return result


def compute_all_results(mode,noofepoch,noofnode,fold):
    All_final=0
    for i in range(len(noofepoch)):        
        #print(noofnode[i])
        if(mode==0):
            putpath=fold+'\Results\Epoch_'+str(noofepoch[i])+'\\Nodes_'+str(noofnode[0])+'\\Nodes_'+str(noofnode[0])+'_Epoch_'+str(noofepoch[i])+'_All_Efficiency_Of_Training.csv'
        elif(mode==1):
            putpath=fold+'\Results\Epoch_'+str(noofepoch[i])+'\\Nodes_'+str(noofnode[0])+'\\Nodes_'+str(noofnode[0])+'_Epoch_'+str(noofepoch[i])+'_All_Efficiency_Of_Testing.csv'
        
        #print(putpath)
        df=pd.read_csv(putpath)
        #print(df)
        final=df.iloc[0:1,:]
        for j in range(1,10):
            
            if(mode==0):
                putpath=fold+'\Results\Epoch_'+str(noofepoch[i])+'\\Nodes_'+str(noofnode[j])+'\\Nodes_'+str(noofnode[j])+'_Epoch_'+str(noofepoch[i])+'_All_Efficiency_Of_Training.csv'
            elif(mode==1):
                putpath=fold+'\Results\Epoch_'+str(noofepoch[i])+'\\Nodes_'+str(noofnode[j])+'\\Nodes_'+str(noofnode[j])+'_Epoch_'+str(noofepoch[i])+'_All_Efficiency_Of_Testing.csv'
            
            print(putpath)
            df=pd.read_csv(putpath)
            df=df.iloc[0:1,:]
            final = pd.concat([final, df], axis=0)
        final=final.reset_index()
        final=final.iloc[:,1:]   
        
        if(mode==0):
            path = fold+'/All_Results/Training'   # if folder doesn't exists then create new folder
        elif(mode==1):
            path = fold+'/All_Results/Testing'   # if folder doesn't exists then create new folder
           
        if not os.path.exists(path):
            os.makedirs(path)    
        
        if(mode==0):
            final.to_csv(path+'/ALL_Results_for_Epoch_'+str(noofepoch[i])+'.csv', sep=',',index=False) 
        elif(mode==1):
            final.to_csv(path+'/ALL_Results_for_Epoch_'+str(noofepoch[i])+'.csv', sep=',',index=False) 
        

        if(i==0):  # for first initiallization
            All_final=final
        else:
            All_final = pd.concat([All_final, final], axis=0)
        
    if(mode==0):
        All_final.to_csv(path+'/ALL_Combined_Results_Of_Training.csv', sep=',',index=False) 
    elif(mode==1):
        All_final.to_csv(path+'/ALL_Combined_Results_Of_Testing.csv', sep=',',index=False) 
    
    result=np.array(All_final)
    return result

#-------------------------------------------
#-------------------------------------------
#-------------------------------------------
#-------------------------------------------
#-------------------------------------------
#-------------------------------------------


for modelin in range(1,2):

    
    noofepoch=[1000,2000,3000,4000,5000,6000,7000,8000,9000,10000]
    #noofepoch=[1000,2000,3000,4000,5000,6000,9000]
    
    #-------------------------------------------
    #-------------------------------------------
    getTop=5
    mode=1    # MODE 0 FOR Training # MODE 1 FOR Testing #  MODE 2 FOR AVG   
    putnode=10
    modelindex=modelin    # 1 for random weights 2 for pearson 3 for pearson absolute 
    cmpindex=4
    putyear=2008    ## 2003 or 2008
    #-------------------------------------------
    #-------------------------------------------
    putcmp=['','Reliance','Infosys','HDFC','DrReddy']   # Reliance, Infosy
    putmodel=['','Random Weights','Pearson Weights','Pearson Weights ABSOLUTE']
    
    
    #-------------------------------------------
    #-------------------------------------------
    #-------------------------------------------
    #-------------------------------------------
    #-------------------------------------------
    #-------------------------------------------
    
    
    putfold='.\\'+str(putyear)+'\\'+putcmp[cmpindex]+'\\'+putmodel[modelindex]
    noofnode=[]
       
    
    for i in range(10):
        noofnode.append(putnode)
        putnode+=10
    
              
    if(mode==2):
        result0=compute_all_results(0,noofepoch,noofnode,putfold)
        fmea0=compute_all_fmea(0,noofepoch,noofnode,putfold)
        result1=compute_all_results(1,noofepoch,noofnode,putfold)
        fmea1=compute_all_fmea(1,noofepoch,noofnode,putfold)
        result=np.add(result0,result1)
        fmea=np.add(fmea0,fmea1)
        result=result/2
        fmea=fmea/2
    else:
        result=compute_all_results(mode,noofepoch,noofnode,putfold)
        fmea=compute_all_fmea(mode,noofepoch,noofnode,putfold)
        
    print(result.shape)
    putresultacc=np.reshape(result, (1, result.shape[0]*result.shape[1]))
    print(putresultacc.shape)
    
    acc=putresultacc[0].tolist()
    z=np.argsort(acc)[(-1*getTop):][::-1]
    print(z)
    
    
    
    
    
    
    if(mode==0):
        saveFile = open(putfold+'/All_Results/Top_'+str(getTop)+'_Of_Training.txt','w')
    elif(mode==1):
        saveFile = open(putfold+'/All_Results/Top_'+str(getTop)+'_Of_Testing.txt','w')
    else:
        saveFile = open(putfold+'/All_Results/Top_'+str(getTop)+'_Of_Both.txt','w')
        
    print("Epoch :  Node : momentum constant")
    
    saveFile.write("\n\n "+putcmp[cmpindex]+" "+putmodel[modelindex]+" as Weights")    
    saveFile.write("\n\nEpoch :  Node : momentum constant")    
       
    ans=[]
    
    for i in range(getTop):
        #xi=int((z[i]+1)/9)-1
        #xj=((z[i]+1)%9)-1
        xi=int((z[i])/9)
        xj=((z[i])%9)
        epochx=int(xi/10)
        nodex=int(xi%10)
        putstr=" "
        
        if(noofnode[nodex]==100):
            putstr=putstr+str(noofnode[nodex])+"  :  "
        else:
            putstr=putstr+str(noofnode[nodex])+"    :  "
        
        if(noofepoch[epochx]==10000):
            putstr=putstr+str(noofepoch[epochx])+"  :  "
        else:
            putstr=putstr+str(noofepoch[epochx])+"   :  "
    
        putstr=putstr+str((xj+1)/10)
    
        
        
        f=[]
        #f.append(putstr)
        #putnum='%.3f' % result[xi][xj]
        putacc=round(result[xi][xj],2)
        putfmea=round(fmea[xi][xj]*100,2)
       
        
        f.append(putstr)
        f.append(putacc)
        f.append(putfmea)
        ans.append(f)
        print(putstr)
        print(putacc)
        print(putfmea)
        saveFile.write("\n\n"+putstr+"\n\t")    
        saveFile.write("\n\t"+str(putacc))
        saveFile.write("\n\t"+str(putfmea))
        
        
    saveFile.close()
    
    #print(ans)
    
    
    
    ansAdd=ans
    ans=pd.DataFrame(ans,columns = [' neurons : epochs : mc & lr = 0.1','Accuracy','F-Measure'])
    
    #print(ans)
    meanAcc=ans["Accuracy"].mean()
    meanFMea=ans["F-Measure"].mean()
    ansAdd.append(['Mean',meanAcc,meanFMea])
    
    medianAcc=ans["Accuracy"].median()
    medianFMea=ans["F-Measure"].median()
    ansAdd.append(['Median',medianAcc,medianFMea])

    #print(ansAdd)
    stdAcc=ans["Accuracy"].std()
    stdFMea=ans["F-Measure"].std()
    ansAdd.append(['Standard deviation',stdAcc,stdFMea])


    ans=pd.DataFrame(ansAdd)
       

    
    putheader=[' neurons : epochs : mc & lr = 0.1','Accuracy','F-Measure']
    
    if(mode==0):
        ans.to_csv(putfold+'/All_Results/Top_'+str(getTop)+'_Of_Training.csv', sep=',',index=False,header=putheader) 
    elif(mode==1):
        ans.to_csv(putfold+'/All_Results/Top_'+str(getTop)+'_Of_Testing.csv', sep=',',index=False,header=putheader) 
    else:
        ans.to_csv(putfold+'/All_Results/Top_'+str(getTop)+'_Of_Both.csv', sep=',',index=False,header=putheader) 
        
        
        