#!/usr/bin/env python
# coding: utf-8

# In[21]:


import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pickle
from sklearn.metrics import accuracy_score
import nltk


# In[67]:


data = pd.read_csv('./Training.csv')

x = data.values
X = x[:,:-1]
X = X[:,20:40]
Y = x[:,-1]
le = preprocessing.LabelEncoder()
le.fit(Y)
Y = le.transform(Y)
Y.shape

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
lr = LogisticRegression(solver='lbfgs', multi_class='multinomial')
lr.fit(X_train,Y_train)
y_pred = lr.predict(nparray.reshape(-1,1))
Y_pred = le.inverse_transform(y_pred)


# In[68]:


np.sum(Y_pred==Y_test)/Y_test.shape


# In[69]:


accuracy_score(Y_test,Y_pred)


# In[61]:





# In[18]:


select_k_best_classifier.get_support? #list of booleans
# new_features = [] # The list of your K best features

# for bool, feature in zip(mask, feature_names):
#     if bool:
#         new_features.append(feature)


# In[19]:




#filename = 'finalized_model.sav'
#pickle.dump(lr, open(filename, 'wb'))


# In[68]:





# In[244]:



#accuracy_score(Y_test,y_pred)


# In[246]:


# loaded_model = pickle.load(open(filename, 'rb'))
# result = loaded_model.score(X_test, Y_test)
# # print(result)


# In[ ]:




