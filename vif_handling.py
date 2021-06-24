#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from statsmodels.stats.outliers_influence import variance_inflation_factor
def vif_checking(dfx):
    X_scaled=standard_scaling(dfx) #standardization is required before checking vif
    vif_dict = {dfx.columns[i]:variance_inflation_factor(X_scaled,i) for i in range(dfx.shape[1])}
    return vif_dict

def vif_handling(dfx): 
    flag=0
    vif_dict = vif_checking(dfx)
    if max(vif_dict.values()) >5:
        flag=1
    while flag == 1:
        vif_dict = vif_checking(dfx)
        for key in vif_dict.keys():
            M=max(vif_dict.values())
            if vif_dict[key]==M:
                 dfx.drop(columns=[key],inplace=True)
                 flag = 0
                 break
        
        if max(vif_checking(dfx).values()) >5:
           flag=1
        
    
    return dfx

