#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#turn all the columns numerical
#by creating dummies
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
            #drop the categorical
            data.drop(columns = col,inplace=True)
            
    return data

