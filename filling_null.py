#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def filling_null(data):
    rows,cols=data.shape
    col_info={}
    for column in data.columns:
        col_info[column]=[data[column].dtype,data[column].isnull().sum()]
        
    for key in col_info.keys():
        if col_info[key][1]>=0.4*rows: #if null values are greater than 40% in a single column
                data.drop(columns = key,inplace=True)
          
        elif col_info[key][0]=='O':
                if data[key].unique().shape[0]>=0.7*rows:
                    data.drop(columns = key,inplace=True)
                elif col_info[key][1]!=0:
                       for elm in list(zip(data[key].unique(),data[key].value_counts())):
                          #we can consider [*l.index 
                          if elm[1]==max(data[key].value_counts()):#by max value
                             data[key].fillna(elm[0],inplace=True)  
                            

        elif col_info[key][0]!='O' and col_info[key][1]!=0:
                 #filling with mean value of that column
                 data[key].fillna(np.mean(data[key]),inplace=True)

        elif col_info[key][0]=='int32' or 'int64':    #considering the case where some ID column is given
             if data[key].unique().shape[0]>=0.99*rows:
                data.drop(columns = key,inplace=True) 

    return data

