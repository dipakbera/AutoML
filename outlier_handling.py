#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def outlier_handling(data):
    primary_shape=data.shape[0]
    flag=0
    data_n=data
    while flag==0 and data.shape[0]>0.9*primary_shape:
          for col in data.columns:
            if data[col].dtype!='O' and data.shape[0]>0.9*primary_shape:
                if abs(data[col].skew())>1.5:
                            q=data[col].quantile(.01)  #top 1% we are removing
                            data_n = data[data[col]>q]
                            if data_n.shape[0]>0.9*primary_shape:
                               data = data_n
                            
          if data.shape[0]!=data_n.shape[0]:
             break
        
          flag=1                 
          skew_list = [abs(data[col].skew()) for col in data.columns if data[col].dtype!='O']
          for skw in skew_list:
              if skw > 1.5:
                 flag=0
                 break
    return data 

