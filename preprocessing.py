import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.preprocessing import StandardScaler,MinMaxScaler
from sklearn.decomposition import PCA

def data_cleaning(df, target='last'):
    df.reset_index(inplace = True, drop = True)
    df.drop_duplicates(subset=None,keep='first',inplace=True)
    if target=='last':
        df.dropna(subset=[df.columns[-1]],inplace=True)
    else:
        df.dropna(subset=[target],inplace=True)
    df=df.replace('[~!@#$%^&*()_+/]','',regex = True)
    return df

def Null_checking(df):
    null_df=pd.DataFrame({col:[df[col].isnull().sum(),df[col].isnull().sum()*100/len(df)] for col in df.columns},\
    index=['null_count','null_percentage'])
    return null_df

def Excessive_Null(df,percent_limit=70):
    for col in df.columns:
        if df[col].isnull().sum() > percent_limit*len(df)/100 :
            df.drop(col,axis=1,inplace=True)
    return df

def uniqueness_checking(df):
    unique_df=pd.DataFrame({col:[df[col].unique().shape[0],df[col].unique().shape[0]*100/len(df), df[col].dtypes]\
    for col in df.columns},index=['unique_count','uniqueness_percentage', 'dtype'])
    return unique_df

def severe_unique_int_obj_drop(df,percent_limit=99):
    for col in df.columns:
        if df[col].dtype != 'float64' and df[col].unique().shape[0] > percent_limit*len(df)/100 :
             df.drop(col,axis=1,inplace=True)
    return df

def drop_cols(df, cols=[]):
    for col in cols:
        df.drop(col, axis=1, inplace=True)
    return df

def Null_filling_num(df,fill_by='mean'):
    for col in df.columns:
        if df[col].dtypes!= 'O' and df[col].isnull().sum()>0:
           if fill_by == 'mean':
              df[col].fillna(df[col].mean(),inplace=True)
           elif fill_by == 'median':
              df[col].fillna(df[col].median(),inplace=True)
           elif fill_by == 'mode':
              df[col].fillna(df[col].mode()[0],inplace=True)
           elif fill_by == 'interpolate':
              df[col].fillna(df[col].interpolate(),inplace=True)
    return df

def Null_filling_cat(df,fill_by='mode'):
    for col in df.columns:
        if df[col].dtypes == 'O' and df[col].isnull().sum()>0:
           if fill_by == 'mode':
              df[col].fillna(df[col].mode()[0],inplace=True)
           elif fill_by == 'ffill':
              df[col].fillna(method = "ffill", inplace = True)
           elif fill_by == 'bfill':
              df[col].fillna(method = "bfill", inplace = True)
    return df

def skew_handling(df, trans= 'yeojohnson'):
    for col in df.columns:
        if df[col].dtype!='O' and abs(df[col].skew())>1:
           flag = 0
           if trans == 'sqrt':
                for elm in df[col].unique():
                    if elm < 0:
                        flag=1
                        break
                if flag==0:
                   df[col]=np.sqrt(df[col]) 
                
           elif trans == 'log':
                for elm in df[col].unique():
                        if elm <= 0:
                            flag=1
                            break
                if flag==0:
                   df[col]=np.log(df[col])
                    
           elif trans == 'boxcox':
                for elm in df[col].unique():
                        if elm <= 0:
                            flag=1
                            break
                if flag==0:
                    df[col], param = stats.boxcox(df[col]) 
                    
           if trans == 'yeojohnson' or flag == 1:
              df[col], param = stats.yeojohnson(df[col].astype(float))
    return df

def remove_outliers_interquartile(qu_dataset, qu_field, qu_fence='inner'):
    a = qu_dataset[qu_field].describe()
    iqr = a["75%"] - a["25%"]
    
    if qu_fence == "inner":
        upper_inner_fence = a["75%"] + 1.5 * iqr
        lower_inner_fence = a["25%"] - 1.5 * iqr
        output_dataset = qu_dataset[qu_dataset[qu_field]<=upper_inner_fence]
        output_dataset = output_dataset[output_dataset[qu_field]>=lower_inner_fence]
     
    elif qu_fence == "outer":
        upper_outer_fence = a["75%"] + 3 * iqr
        lower_outer_fence = a["25%"] - 3 * iqr
        output_dataset = qu_dataset[qu_dataset[qu_field]<=upper_outer_fence]
        output_dataset = output_dataset[output_dataset[qu_field]>=lower_outer_fence]
    
    percent_removed=100*(len(qu_dataset)-len(output_dataset))/len(qu_dataset)
    outlier_dict = {'initial_length':len(qu_dataset),'updated_length':len(output_dataset),'percent_removed(%)':percent_removed}
    
    return outlier_dict,output_dataset

def create_dummies(data):
    for col in data.columns:
        if data[col].dtype=='O': 
            catgs=data[col].unique()
            occurs=np.array(data[col].value_counts())
            cumsum_occurs=np.cumsum(occurs)
        
            for i in range(len(cumsum_occurs)):
                if cumsum_occurs[i]>=.9*data.shape[0]:
                    p=i+1
                    break
                    
            top_catgs=catgs[:p]       
            data[col].replace(to_replace =catgs[p:], 
                            value = catgs[0], inplace=True)
            
            mydummy = pd.get_dummies(data[col], prefix=col,drop_first=True)
            data=pd.concat([data,mydummy],axis=1)
            data.drop(columns = col,inplace=True)
    return data

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
        M=max(vif_dict.values())    
        for key in vif_dict.keys():
            if vif_dict[key]==M:
                 dfx.drop(columns=[key],inplace=True)
                 flag = 0
                 break
        
        if max(vif_checking(dfx).values()) >5:
           flag=1
    return dfx

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

