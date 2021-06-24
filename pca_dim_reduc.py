#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def pca_dim_reduc(dfx):
    dfx_scaled=standard_scaling(dfx)
    df=pd.DataFrame(data=dfx_scaled, columns= dfx.columns)
    pca = PCA()
    pca.fit_transform(df)
    pca.explained_variance_ratio_
    arr=np.cumsum(pca.explained_variance_ratio_)
    for i in range(len(arr)):
        if arr[i]>=.87:
            p=i+1
            break
        
    pca = PCA(n_components=p)
    new_data = pca.fit_transform(df)
    cols=['pc'+str(i+1) for i in range(p)]
    principal_Df = pd.DataFrame(data = new_data, columns=cols)
    
    return principal_Df

