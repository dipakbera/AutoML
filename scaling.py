#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def standard_scaling(x):
    scaler =StandardScaler()
    x_scaled = scaler.fit_transform(x)
    return x_scaled

def normal_scaling(x):
    scaler =MinMaxScaler()
    x_scaled = scaler.fit_transform(x)
    return x_scaled

def scaling(x):
    l=[abs(x[col].skew()) for col in x.columns]
    flag=0
    for elm in l:
        if elm>2:
            flag=1
            break
    if flag==0:
        return standard_scaling(x)
    else:
        return normal_scaling(x)

