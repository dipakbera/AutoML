#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def skew_handling(data):
    
    for col in data.columns:
        if data[col].dtype!='O': 
          if data[col].skew()>2:
            if 0 in data[col].unique():
                data[col]=np.sqrt(data[col])
            else:
                data[col]=np.log(data[col])     
    return data

