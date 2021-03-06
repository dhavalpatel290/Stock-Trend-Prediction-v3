# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 23:48:59 2018
@author: Dhaval
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 12:39:47 2018
@author: Dhaval
"""
import keras
import os
import scipy
import numpy as np
import pandas as pd
from tqdm._tqdm_notebook import tqdm_notebook
from sklearn.metrics import confusion_matrix
from sklearn import metrics
from sklearn.model_selection import train_test_split
from keras import optimizers
from keras.wrappers.scikit_learn import KerasRegressor
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.models import model_from_json
import os
import random

def pl(pp):
    print("\n\t------"+pp+"-------\n\t-----\n\t-----")

def get_run_time(stime,etime):
    millis=etime-stime
    allmilli=millis
    seconds=int(millis/1000)
    minutes=int(seconds/60)
    hours=int(minutes/60)
    puth=hours%24
    putm=minutes%60
    puts=seconds%60
    putmilli=millis-(seconds*1000)
    putstr="Time to train -->   "+str(puth)+" Hours :  "+str(putm)+" Minutes : "+str(puts)+" Seconds : "+str(putmilli)+" Milliseconds"
    return putstr,puth,putm,puts,putmilli,allmilli


def saveAllInCSV(putyear,putcmp,putmodel,node,epoch,companyName,EfficiencyToSave,PrecisionToSave,RecallToSave,FMeasureToSave,HHToSave,MMToSave,SSToSave,MSToSave,AllMSToSave):
    EfficiencyToSave=np.array(EfficiencyToSave)
    PrecisionToSave=np.array(PrecisionToSave)
    RecallToSave=np.array(RecallToSave)
    FMeasureToSave=np.array(FMeasureToSave)
    HHToSave=np.array(HHToSave)
    MMToSave=np.array(MMToSave)
    SSToSave=np.array(SSToSave)
    MSToSave=np.array(MSToSave)
    AllMSToSave=np.array(AllMSToSave)
    FinalSave=[]
    for i in range(9):
        temp=[]
        temp.append(EfficiencyToSave[i])
        temp.append(PrecisionToSave[i])
        temp.append(RecallToSave[i])
        temp.append(FMeasureToSave[i])
        temp.append(HHToSave[i])
        temp.append(MMToSave[i])
        temp.append(SSToSave[i])
        temp.append(MSToSave[i])
        temp.append(AllMSToSave[i])
        FinalSave.append(temp)    
    FinalSave=np.array(FinalSave)
    FinalSave=FinalSave.transpose()
    
    putfold='./'+str(putyear)+'/'+putcmp+'/'+putmodel+'/'
    path = putfold+'Results/Epoch_'+str(epoch)+'/Nodes_'+str(node)+'/'   # if folder doesn't exists then create new folder
    #print("Made folder : "+putfold)
    #print("Made folder : "+path)
    
    import os
    if not os.path.exists(path):
        os.makedirs(path)  
        
    np.savetxt(path+'Nodes_'+str(node)+'_Epoch_'+str(epoch)+'_All_Efficiency_Of_Testing.csv',FinalSave, fmt='%.10f',delimiter=',', header='Momentum01,02,03,04,05,06,07,08,09')
    

def savemodel(stime,etime,allnu,nu,onecsvfile,onecm,oneeffi,noofnodes,noofepoch,noofbatchsize,noofsplitinratio):    
    saveFile = open(allnu+'_Of_Testing.txt','a')
    saveFile.write("\n"+nu)    
    saveFile.write("\n\n\t"+onecsvfile)
    saveFile.write("\n\t")
    saveFile.write(str(onecm[0])+"\n\t")
    saveFile.write(str(onecm[1]))
    saveFile.write("\n\n")
    saveFile.write("\n\t\tEfficiency : "+str(oneeffi)+"\n")
    saveFile.write("\n\n")
    putstr,puth,putm,puts,putmilli,putallmilli=get_run_time(stime,etime)
    saveFile.write("\n\t\t "+putstr+"\n")
    saveFile.write("\n\n--------------------------------------------------------------------------\n\n")
    saveFile.close()


def GiveFoldersAccordingToCustomChoice(putyear,putcmp,putmodel,putcompany,putcustom,putactivation,putoptimizer,putlr,putmc,noofsplitinratio,noofbatchsize,noofnodes,noofepoch):
    
    # NodesAndEpochs  or   OptimizerMethod   or Company  
    p2='Epoch'+str(noofepoch)+'/Node'+str(noofnodes)+'/MC'+str(putmc*100)  
    #p2='Updated_Node'+str(noofnodes)+'_Epoch'+str(noofepoch)  
    p3='ANN'
    
    if(putcustom):
        p3=p3+'_C'
        if(putoptimizer=='sgd'):
            p3=p3+'_SGD'
            putinnu='_LR'+str(int(putlr*100))+'MC'+str(int(putmc*100))+'SR1to'+str(noofsplitinratio)+'_BSZ'+str(noofbatchsize)
            putfoldername='/'+p3+'/'+p2+'/'
        elif(putoptimizer=='adam'):
            p3=p3+'_Adam'
            putinnu='_LR'+str(int(putlr*100))+'MC_NotDefine_'+'SR1to'+str(noofsplitinratio)+'_BSZ'+str(noofbatchsize)
            putfoldername='/'+p3+'/'+p2+'/' 
    else:
        p3=p3+'_default'
        p3=p3+'_'+putoptimizer
        if(putoptimizer=='adam'):
            putinnu='_LR_0_001'+'MC_NotDefine_'+'SR1to'+str(noofsplitinratio)+'_BSZ'+str(noofbatchsize)
        else:    
            putinnu='_LR_NotDefine'+'MC_NotDefine_'+'SR1to'+str(noofsplitinratio)+'_BSZ'+str(noofbatchsize)
        putfoldername='/'+p3+'/'+p2+'/' 


    putfold='./'+str(putyear)+'/'+putcmp+'/'+putmodel+putfoldername
    #print("Made folder : "+putfold)
    putfold_for_csv="./Dataset/"
    
    return putfold_for_csv,putfold,putinnu

def get_one_year_filter_data(year,noofnodes,noofepoch,noofbatchsize,noofsplitinratio):
    #print(year+"\n--------")
    
    #import os
    #os.chdir("Stock-Trend-Prediction-Google-Colab")
    dataset= pd.read_csv(year+'.csv')
    
    
    #print(dataset.shape)
    num_dataset=np.array(dataset)
    bool_positive = (num_dataset[:,13] == 1)
    bool_negative = (num_dataset[:,13] == 0)
    positive_dataset=dataset[bool_positive]
    negative_dataset=dataset[bool_negative]
    #print(positive_dataset.shape)
    #print(negative_dataset.shape)
    positive_dataset_input=positive_dataset.iloc[:,0:13]
    positive_dataset_output=positive_dataset.iloc[:,13:]
    #print(positive_dataset_input.shape)
    #print(positive_dataset_output.shape)
    pos_train_in, pos_test_in, pos_train_out, pos_test_out = train_test_split(positive_dataset_input,positive_dataset_output, test_size=4/5)
    pos_train_in, pos_test_in, pos_train_out, pos_test_out = train_test_split(pos_train_in,pos_train_out, test_size=1/noofsplitinratio)
    #print(year)
    #print(pos_train_in.shape)
    #print(pos_test_in.shape)
    negative_dataset_input=negative_dataset.iloc[:,0:13]
    negative_dataset_output=negative_dataset.iloc[:,13:]
    #print(negative_dataset_input.shape)
    #print(negative_dataset_output.shape)
    neg_train_in, neg_test_in, neg_train_out, neg_test_out = train_test_split(negative_dataset_input,negative_dataset_output, test_size=4/5)
    neg_train_in, neg_test_in, neg_train_out, neg_test_out = train_test_split(neg_train_in,neg_train_out, test_size=1/noofsplitinratio)
    #print(neg_train_in.shape)
    #print(neg_test_in.shape)
       
    one_train_in=np.concatenate([pos_train_in, neg_train_in])
    one_test_in=np.concatenate([pos_test_in, neg_test_in])
    one_train_out=np.concatenate([pos_train_out, neg_train_out])
    one_test_out=np.concatenate([pos_test_out, neg_test_out])
    
    
    return one_train_in,one_test_in,one_train_out,one_test_out


def get_dataset(putfold_for_csv,stockname,onecsvfile,noofnodes,noofepoch,noofbatchsize,noofsplitinratio,putyear):
    #sharetype='EQN'
    years=[]
    initial=putyear
    for i in range(10):
        putstr=putfold_for_csv+'computed_feature_01-01-'+str(initial)+'-TO-31-12-'+str(initial)+onecsvfile
        
        #print(putstr)
        years.append(putstr)
        initial=initial+1
        
    all_train_in,all_test_in,all_train_out,all_test_out=get_one_year_filter_data(years[0],noofnodes,noofepoch,noofbatchsize,noofsplitinratio)
    #print(all_train_out.shape)
    for year in range(1,len(years)):
        #print(years[year])
        #print(neg_test_out)
        #print(neg_test_in)
        one_train_in,one_test_in,one_train_out,one_test_out=get_one_year_filter_data(years[year],noofnodes,noofepoch,noofbatchsize,noofsplitinratio)
        #print(one_train_out.shape)
        #print(all_train_out.shape)
        
        #np.concatenate([x, y,z])
        all_train_in=np.concatenate([all_train_in, one_train_in])
        all_test_in=np.concatenate([all_test_in, one_test_in])
        all_train_out=np.concatenate([all_train_out, one_train_out])
        all_test_out=np.concatenate([all_test_out, one_test_out])
        
    '''print(all_train_in.shape)
    print(all_test_in.shape)
    print(all_train_out.shape)
    print(all_test_out.shape)
    '''
    
    '''all_train_in=all_train_in.dropna()
    all_test_in=all_test_in.dropna()
    all_train_out=all_train_out.dropna()
    all_test_out=all_test_out.dropna()
    '''
    return all_train_in,all_test_in,all_train_out,all_test_out
    
def save_data_mapping_with_dates(train_in,test_in,train_out,test_out):
    #Completing Save
    #all_train_out=np.concatenate([train_in, train_out])
    tem_train_in=pd.DataFrame(train_in)
    tem_test_in=pd.DataFrame(test_in)
    tem_train_out=pd.DataFrame(train_out)
    tem_test_out=pd.DataFrame(test_out)
    
    all_train=pd.concat([tem_train_in, tem_train_out], axis=1)
    all_test=pd.concat([tem_test_in, tem_test_out], axis=1)
    putheaders=['date','close_10_sma','close_10_ema','kdjk_10','kdjd_10','macd','rsi_10','wr_10','cci_10','Momentum','ADOsc','New_Feature','OpenPrice','UpDown']
    all_train.columns =putheaders
    all_test.columns =putheaders
    
    all_train['date'] =pd.to_datetime(all_train['date'])
    all_test['date'] =pd.to_datetime(all_test['date'])
    all_train=all_train.sort_values(by='date',ascending=True)
    all_test=all_test.sort_values(by='date',ascending=True)
        
    all_train.to_csv(putfoldername+'Mapped_Train_data_with_dates.csv',index=False)
    all_test.to_csv(putfoldername+'Mapped_Test_data_with_dates.csv',index=False)
    
    all_train=np.array(all_train)
    all_test=np.array(all_test)
    
    without_date_train_in=all_train[:,1:13]
    without_date_test_in=all_test[:,1:13]
    train_out=all_train[:,13]
    test_out=all_test[:,13]
    
    c_2d=[]
    for d in all_train[:,13]:
        one=[]
        one.append(d)
        c_2d.append(one)
    train_out=np.array(c_2d)
    c_2d=[]
    for d in all_test[:,13]:
        one=[]
        one.append(d)
        c_2d.append(one)
    test_out=np.array(c_2d)
    
    
    return without_date_train_in,without_date_test_in,train_out,test_out
    
   


def trim_dataset(mat,batch_size):
    """
    trims dataset to a size that's divisible by BATCH_SIZE
    """
    no_of_rows_drop = mat.shape[0]%batch_size
    if no_of_rows_drop > 0:
        return mat[:-no_of_rows_drop]
    else:
        return mat


def build_timeseries(mat_in, mat_out,TIME_STEPS):
    """
    Converts ndarray into timeseries format and supervised data format. Takes first TIME_STEPS
    number of rows as input and sets the TIME_STEPS+1th data as corresponding output and so on.
    :param mat: ndarray which holds the dataset
    :param y_col_index: index of column which acts as output
    :return: returns two ndarrays-- input and output in format suitable to feed
    to LSTM.
    """
    # total number of time-series samples would be len(mat) - TIME_STEPS
    dim_0 = mat_in.shape[0] - TIME_STEPS
    dim_1 = mat_in.shape[1]
    x = np.zeros((dim_0, TIME_STEPS, dim_1))
    y = np.zeros((dim_0,))
    #print("dim_0",dim_0)
    for i in tqdm_notebook(range(dim_0)):
        x[i] = mat_in[i:TIME_STEPS+i]
        y[i] = mat_out[TIME_STEPS+i]
#         if i < 10:
#           print(i,"-->", x[i,-1,:], y[i])
    #print("length of time-series i/o",x.shape,y.shape)
    return x, y
         

def compute_effi(putmodelindex,putfoldername,putcustom,putoptimizer,putactivation,putlr,putmc,csvfile,allnu,nu,train_in,test_in,train_out,test_out,noofnodes,noofepoch,noofbatchsize,noofsplitinratio):
    
    from sklearn.preprocessing import MinMaxScaler
    scaler=MinMaxScaler(feature_range=(-1, 1))
    train_in_sliced=scaler.fit_transform(train_in[:,0:11])
    test_in_sliced=scaler.transform(test_in[:,0:11])
    
    final_train_in=[]
    final_test_in=[]
    
    for i in range(train_in_sliced.shape[0]):
        onerow=[]
        for j in range(11):
            onerow.append(train_in_sliced[i][j])
        onerow.append(train_in[i][11])
        final_train_in.append(onerow)
        
    for i in range(test_in_sliced.shape[0]):
        onerow=[]
        for j in range(11):
            onerow.append(test_in_sliced[i][j])
        onerow.append(test_in[i][11])
        final_test_in.append(onerow)
    
    final_train_in=np.array(final_train_in)
    final_test_in=np.array(final_test_in)  
      
    putheaders='close_10_sma,close_10_ema,kdjk_10,kdjd_10,macd,rsi_10,wr_10,cci_10,Momentum,ADOsc,New_Feature,OpenPrice'

    np.savetxt(putfoldername+'Data_TrainingInput.csv',final_train_in, fmt='%.10f',delimiter=',', header=putheaders)
    np.savetxt(putfoldername+'Data_TrainingOutput.csv',train_out, fmt='%.10f',delimiter=',', header='UpDown')
    np.savetxt(putfoldername+'Data_TestingInput.csv',final_test_in, fmt='%.10f',delimiter=',', header=putheaders)
    np.savetxt(putfoldername+'Data_TestingOutput.csv',test_out, fmt='%.10f',delimiter=',', header='UpDown')
    
    train_dataset= pd.read_csv(putfoldername+'Data_TrainingInput.csv')
    corel_full_matrix=train_dataset.corr(method='pearson')
    OpenPriceRelation=corel_full_matrix['OpenPrice']
    OpenPriceRelation=np.array(OpenPriceRelation)
    if(putmodelindex==3):   #  PEARSON Absolute
        OpenPriceRelation=np.absolute(OpenPriceRelation)
    OpenPriceRelationFilter = (OpenPriceRelation!=1)
    
    
    #pl("gone")
    #print(corel_full_matrix)
    #pl("done corel")
    #print(OpenPriceRelation)
    newRel=[]
    for il in OpenPriceRelation:
        if(il!=1):
            newRel.append(float(il))
        
    #print(newRel)
    #newRel=newRel.remove(newRel[len(newRel-1)])
    #print(newRel)
    
    insort=np.argsort(newRel)
    #print(insort)
    """
    #LOGIC of np.argsort()
    insort=np.argsort([1,2,3,4,5,6])
    print(insort)
    #Output: array([0, 1, 2, 3, 4, 5], dtype=int64)
    insort=np.argsort([1,2,3,4,6,5])
    print(insort)
    #Output: array([0, 1, 2, 3, 5, 4], dtype=int64)
    """
    
    
    removesecond=0
    
    if(insort[0]==10):   #  new is not relevant
        removesecond=1
    newRel=np.array(newRel)
    #pl("here")
    #print(newRel[insort[0]])
    #pl("here")
    #print(newRel[insort[1]])
    #pl("here")
    
    if(removesecond==0):
        OpenPriceRelationFilter = (OpenPriceRelation!=newRel[insort[0]])
    else:
        OpenPriceRelationFilter = (OpenPriceRelation!=newRel[insort[1]])
    
    #print(OpenPriceRelationFilter)
    #pl("here")
        
    OpenPriceRelationFilter[len(OpenPriceRelationFilter)-1]=False
    #pl("here")
    
    
    #print(OpenPriceRelationFilter)
    
    train_in=final_train_in[:,OpenPriceRelationFilter]
    test_in=final_test_in[:,OpenPriceRelationFilter]
    #print(OpenPriceRelation)
    
    OpenPriceRelation=OpenPriceRelation[OpenPriceRelationFilter]
    
    #print(OpenPriceRelation)
    
    #print(train_in.shape)
    #print(test_in.shape)
    
    # Initialising the ANN
    #return cm,effi,precision,recall,f_measure,OpenArray,final,stime,etime,train_in,test_in,final_train_in,corel_full_matrix
    
    TIME_STEPS=10
    #print("Are any NaNs present in train/test matrices?",np.isnan(train_in).any(), np.isnan(train_in).any())
    train_in, train_out = build_timeseries(train_in,train_out, TIME_STEPS)
    train_in = trim_dataset(train_in, noofbatchsize)
    train_out = trim_dataset(train_out, noofbatchsize)
    #print("Batch trimmed size",train_in.shape, train_out.shape)
    classifier = Sequential()    
    # Adding the input layer and the first hidden layer
    #Old -- classifier.add(Dense(activation = putactivation,kernel_initializer = 'uniform',input_dim = 10,units = noofnodes))
    classifier.add(LSTM(noofnodes, batch_input_shape=(noofbatchsize, TIME_STEPS, train_in.shape[2]),
                        dropout=0.0, recurrent_dropout=0.0, stateful=True, return_sequences=True,
                        kernel_initializer='random_uniform'))
    classifier.add(Dropout(0.2))
    classifier.add(LSTM(50, dropout=0.0))
    classifier.add(Dropout(0.4))
    classifier.add(Dense(10,activation='relu'))
    classifier.add(Dense(kernel_initializer = 'uniform',activation = 'sigmoid',units= 1))     
    # Adding the output layer
    # Compiling the ANN
    #pl("here done making Model")
    #print('--------')
    
      
    if(putcustom):
        if(putoptimizer=='sgd'):
                sgd = optimizers.SGD(lr=putlr, momentum=putmc)
                classifier.compile(optimizer=sgd, loss = 'binary_crossentropy', metrics = ['accuracy'])   
        elif(putoptimizer=='adam'):
            adm=optimizers.Adam(lr=putlr, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
            classifier.compile(optimizer=adm, loss = 'binary_crossentropy', metrics = ['accuracy'])
    else:
       classifier.compile(optimizer=putoptimizer, loss = 'binary_crossentropy', metrics = ['accuracy'])
      
    ##################################################
    ##################################################
    ##################################################
    #pl("here done going for Model Weights "+str(putmodelindex))
    if(putmodelindex==1):     #Randommodel
        # Do nothing
        # In Random Model, So no need to use set_weights method
        timepass=0   # just for fun  :) 
        timepass=timepass+1 # just for fun  :)
        #print("In Random Model, So no need to use set_weights method "+str(timepass))
    elif(putmodelindex==2):    # Pearson
        final = []  
        inp_hidden = []
        hidden_bias = []
        hidden_op = []
        op_bias = []  
        for i in range(10):   # put pearson coeffi as weights on edges
            temp = []
            for j in range(noofnodes):
                temp.append(OpenPriceRelation[i])
            inp_hidden.append(temp)
        hidden_bias=np.random.uniform(-1,1,size=(noofnodes,))       # random bais from range -1 to 1 
        hidden_op = np.random.uniform(-1, 1, size=(noofnodes,1))   
        op_bias = np.random.uniform(-1, 1, size=(1,))
        final.append(np.array(inp_hidden))
        final.append(np.array(hidden_bias))
        final.append(np.array(hidden_op))
        final.append(np.array(op_bias))
        classifier.set_weights(final)
    elif(putmodelindex==3):    # Pearson ABSOLUTE
        final = []  
        inp_hidden = []
        hidden_bias = []
        hidden_op = []
        op_bias = []
        for i in range(10):   # put pearson coeffi as weights on edges
            temp = []
            for j in range(noofnodes):
                temp.append(abs(OpenPriceRelation[i]))
            inp_hidden.append(temp)
        hidden_bias=np.random.uniform(0,1,size=(noofnodes,))       # random bais from range -1 to 1 
        hidden_op = np.random.uniform(0, 1, size=(noofnodes,1))   
        op_bias = np.random.uniform(0, 1, size=(1,)) 
        final.append(np.array(inp_hidden))
        final.append(np.array(hidden_bias))
        final.append(np.array(hidden_op))
        final.append(np.array(op_bias)) 
        classifier.set_weights(final)
            
    ##################################################
    ##################################################
    ##################################################
    #pl("here done starting time")
    
    import time
    stime = int(round(time.time() * 1000))
    #pl("here get Weights time")
    
    final=classifier.get_weights()
    #pl("here Done geting initial weights and saving in file")
    classifier.save_weights(nu+"Initial_Training_Assigned_ANNweight.h5")
    #pl("here Done geting initial weights and saving in file")
    # Fitting the ANN to the Training set
    test_in, test_out = build_timeseries(test_in,test_out, TIME_STEPS)
    x_val, x_test_t = np.split(trim_dataset(test_in, noofbatchsize),2)
    y_val, y_test_t = np.split(trim_dataset(test_out, noofbatchsize),2)
    #print("Test size", x_test_t.shape, y_test_t.shape, x_val.shape, y_val.shape)

    classifier.fit(train_in, train_out, epochs=noofepoch, batch_size=noofbatchsize, verbose=0,
                        shuffle=False, validation_data=(trim_dataset(x_val, noofbatchsize),
                        trim_dataset(y_val, noofbatchsize)))
    #classifier.fit(train_in, train_out,batch_size = noofbatchsize, epochs =noofepoch,verbose=1)      
    #pl("here Done fiting")
    import time
    etime = int(round(time.time() * 1000))
    # Predicting the Test set results
    
    y_pred = classifier.predict(trim_dataset(x_test_t, noofbatchsize), batch_size=noofbatchsize)
    y_pred = y_pred.flatten()
    y_test_t = trim_dataset(y_test_t, noofbatchsize)
    #print(y_pred)
    y_pred = (y_pred > 0.5)
    #print(y_pred)    
    #print("\n\n\n###########  here")
    cm=confusion_matrix(y_test_t, y_pred)
    #print(cm)
    #print("\n\n\n###########  here")    
    effi=((cm[0][0]+cm[1][1])*100)/float(cm[0][0]+cm[1][1]+cm[1][0]+cm[0][1])
    precision=(cm[0][0]/float(cm[0][1]+cm[0][0]))
    recall=(cm[0][0]/float(cm[1][0]+cm[0][0]))
    f_measure=(2*precision*recall)/float(precision+recall)
    #print(effi)
    
    # serialize model to JSON
    #hiddennode_epoch_decay_learningrate
    OpenArray=classifier.get_weights()
    #print(OpenArray)
    
    classifier.save(nu+"full_model.h5")  # creates a HDF5 file 'my_model.h5'
    classifier.save_weights(nu+"After_Training_Final_ANNweight.h5")
    
    del classifier  # deletes the existing model
    
    # returns a compiled model
    # identical to the previous one
    #from keras.models import load_model
    #model = load_model('my_model.h5')
    
    '''
    model_json = classifier.to_json()
    with open(nu+"classifer.json", "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    classifier.save_weights(nu+"model.h5")
    #print("Saved model to disk")
    '''
    
    
    return cm,effi,precision,recall,f_measure,OpenArray,final,stime,etime,train_in,test_in,final_train_in,corel_full_matrix
    

#----------------------------------------------------
#-----------------------MAIN-------------------------
#----------------------------------------------------
#----------------------------------------------------
#csvfiles=[]
#noofepoch=[]
#noofnodes=[]
#putmc=[]
#



# parameter  1 for Company Selection      #  1 for Reliance,  2 for Infosys  3 for SBI   4 for SunPharma
# parameter  2 for Model Selection        #  1 for Random weights, 2 for Pearson, 3 for Pearson absolute 
# parameter  3 for Starting Epoch
# parameter  4 for Ending Epoch
# parameter  5 for Starting Node
# parameter  6 for Ending Node
# parameter  7 for add_epoch_gap
# parameter  8 for putyear                #    2003 or 2008

import sys
gotParameters=sys.argv

cmpindex=int(gotParameters[1])   # 1 for Reliance 2 for Infosys
modelindex=int(gotParameters[2])    # 1 for random weights 2 for pearson 3 for pearson absolute 

#modelindex=1    # 1 for random weights 2 for pearson 3 for pearson absolute 
#cmpindex=1   # 1 for Reliance 2 for Infosys

#putcmp=['','Reliance','Infosys','SBI','SunPharma','HDFC','DrReddy']   # Reliance, Infosy
putcmp=['','Reliance','Infosys','HDFC','DrReddy']   # Reliance, Infosy
#putcmp_stockname=['','RELIANCEEQN','INFYEQN','SBINEQN','SUNPHARMAEQN','HDFCEQN','DRREDDYEQN']
putcmp_stockname=['','RELIANCEEQN','INFYEQN','HDFCEQN','DRREDDYEQN']
putmodel=['','Random Weights','Pearson Weights','Pearson Weights ABSOLUTE']


Start_Epoch=int(gotParameters[3])
End_Epoch=int(gotParameters[4])
Start_Node=int(gotParameters[5])
End_Node=int(gotParameters[6])
add_epoch_gap=int(gotParameters[7])
putyear=int(gotParameters[8])

#End_Epoch=10
#Start_Node=10
#Start_Epoch=10
#End_Node=10
#add_epoch_gap=10
#putyear=2008

#----------------------------------------------------
#-----------------------MAIN CLOSE-------------------
#----------------------------------------------------
#----------------------------------------------------


gotcmp=putcmp[cmpindex]
gotmodel=putmodel[modelindex]
stockname=putcmp_stockname[cmpindex]

#for one_epoch in range(Start_Epoch,End_Epoch+1000,1000): 
#    for one_node in range(Start_Node,End_Node+10,10):
#        for one_mc in range(1,10,1):
#            one_mc=one_mc/10
#            csvfiles.append(stockname)
#            noofepoch.append(one_epoch)
#            noofnodes.append(one_node)
#            putmc.append(one_mc)
    

noofbatchsize=30 #BSZ BatchSize
noofsplitinratio=2 #SR SplitInRatio
putlr=0.1
putactivation='relu'   # tanh OR relu
putoptimizer='sgd'   # rmsprop OR adam OR custom (sgd Stochastic gradient descent )
putcustomoptimizer=True
putcustom=putcustomoptimizer

#----change the above parameters---------------------
#----------------------------------------------------
#----------------------------------------------------
#----------------------------------------------------

print("Models Started")
for one_epoch in range(Start_Epoch,End_Epoch+add_epoch_gap,add_epoch_gap): 
    for one_node in range(Start_Node,End_Node+10,10):  
        AllComputedEfficiency=[]
        AllComputedPrecision=[]
        AllComputedRecall=[]
        AllComputedFMeasure=[]
        AllTimeHH=[]
        AllTimeMM=[]
        AllTimeSS=[]
        AllTimeMS=[]
        AllTimeAllMS=[]
        for one_mc in range(1,10,1):
            one_mc=one_mc/10
            putfold_for_csv,putfoldername,putinnu=GiveFoldersAccordingToCustomChoice(putyear,gotcmp,gotmodel,stockname,putcustom,putactivation,putoptimizer,putlr,one_mc,noofsplitinratio,noofbatchsize,one_node,one_epoch)
            
            #print(putfoldername)
            path = putfoldername   # if folder doesn't exists then create new folder
            if not os.path.exists(path):
                os.makedirs(path)    
            allnu=putfoldername+'Runs'+putinnu
            nu=putfoldername+putinnu 
            
            
            #print(csvfiles[puti])
            train_in,test_in,train_out,test_out=get_dataset(putfold_for_csv,stockname,stockname,one_node,one_epoch,noofbatchsize,noofsplitinratio,putyear)
            train_in,test_in,train_out,test_out=save_data_mapping_with_dates(train_in,test_in,train_out,test_out)
            
            
            onecm,oneeffi,oneprecision,onerecall,onef_measure,final_ANNweight,Assigned_ANNweight,stime,etime,normalized_train_in,normalized_test_in,final_train_in,corel_full_matrix=compute_effi(modelindex,putfoldername,putcustom,putoptimizer,putactivation,putlr,one_mc,stockname,allnu,nu,train_in,test_in,train_out,test_out,one_node,one_epoch,noofbatchsize,noofsplitinratio)
            #print(onecm)
            #print("Efficiency : "+str(oneeffi))
            savemodel(stime,etime,allnu,nu,stockname,onecm,oneeffi,one_node,one_epoch,noofbatchsize,noofsplitinratio)
            final_ma=corel_full_matrix    
            final_ma.to_csv(putfoldername+'relation.csv', float_format='%.05f',sep=',',index=False) 
            putstr,puth,putm,puts,putmilli,putallmilli=get_run_time(stime,etime)
            #print("\n "+putstr)
            
            
            if int(one_mc*100) in [10,30,60,90]:
                print("--> Completed -- Epoch "+str(one_epoch)+" Node "+str(one_node)+" MC "+str(one_mc*100))   
                
            
            AllComputedEfficiency.append(oneeffi)
            AllComputedPrecision.append(oneprecision)
            AllComputedRecall.append(onerecall)
            AllComputedFMeasure.append(onef_measure)
            AllTimeHH.append(puth)
            AllTimeMM.append(putm)
            AllTimeSS.append(puts)
            AllTimeMS.append(putmilli)
            AllTimeAllMS.append(putallmilli)
            
        #print("call save all")
        saveAllInCSV(putyear,gotcmp,gotmodel,one_node,one_epoch,stockname,AllComputedEfficiency,AllComputedPrecision,AllComputedRecall,AllComputedFMeasure,AllTimeHH,AllTimeMM,AllTimeSS,AllTimeMS,AllTimeAllMS)
        
        
print("Done-----------Done-------------Done")
print("--------------------------------------------------------------------------------------")
print("--------------------------------------------------------------------------------------")
print("----------------------------------"+gotcmp+"------------------------------------------")
print("----------------------------------"+gotmodel+"----------------------------------------")
print("-----------------Epoch--"+str(Start_Epoch)+" to "+str(End_Epoch)+"--------------------")
print("-----------------Node--"+str(Start_Node)+" to "+str(End_Node)+"-----------------------")
print("-----------------Year--------------"+str(putyear)+"-----------------------------------")
print("--------------------------------------------------------------------------------------")
print("--------------------------------------------------------------------------------------")
