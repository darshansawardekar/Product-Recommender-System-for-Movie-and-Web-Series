#!/usr/bin/env python
# coding: utf-8

# In[6]:


import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
import seaborn as sns
movies = pd.read_csv("E:\Project\Dev Data set\ml-latest-small\Data set/movies.csv")
ratings = pd.read_csv("E:\Project\Dev Data set\ml-latest-small\Data set2/ratings.csv")


# In[8]:


movies.head()


# In[9]:


ratings.head()


# In[10]:


final_dataset = ratings.pivot(index='movieId',columns='userId',values='rating')
final_dataset.head()


# In[11]:


final_dataset.fillna(0,inplace=True)
final_dataset.head()


# In[12]:


no_user_voted = ratings.groupby('movieId')['rating'].agg('count')
no_movies_voted = ratings.groupby('userId')['rating'].agg('count')


# In[13]:


f,ax = plt.subplots(1,1,figsize=(16,4))
# ratings['rating'].plot(kind='hist')
plt.scatter(no_user_voted.index,no_user_voted,color='mediumseagreen')
plt.axhline(y=10,color='r')
plt.xlabel('MovieId')
plt.ylabel('No. of users voted')
plt.show()


# In[14]:


final_dataset = final_dataset.loc[no_user_voted[no_user_voted > 10].index,:]


# In[15]:


f,ax = plt.subplots(1,1,figsize=(16,4))
plt.scatter(no_movies_voted.index,no_movies_voted,color='mediumseagreen')
plt.axhline(y=50,color='r')
plt.xlabel('UserId')
plt.ylabel('No. of votes by user')
plt.show()


# In[16]:


final_dataset=final_dataset.loc[:,no_movies_voted[no_movies_voted > 50].index]
final_dataset


# In[17]:


sample = np.array([[0,0,3,0,0],[4,0,0,0,2],[0,0,0,0,1]])
sparsity = 1.0 - ( np.count_nonzero(sample) / float(sample.size) )
print(sparsity)


# In[18]:


csr_sample = csr_matrix(sample)
print(csr_sample)


# In[19]:


csr_data = csr_matrix(final_dataset.values)
final_dataset.reset_index(inplace=True)


# In[20]:


knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
knn.fit(csr_data)


# In[21]:


def get_movie_recommendation(movie_name):
    n_movies_to_reccomend = 10
    movie_list = movies[movies['title'].str.contains(movie_name)]  
    if len(movie_list):        
        movie_idx= movie_list.iloc[0]['movieId']
        movie_idx = final_dataset[final_dataset['movieId'] == movie_idx].index[0]
        distances , indices = knn.kneighbors(csr_data[movie_idx],n_neighbors=n_movies_to_reccomend+1)    
        rec_movie_indices = sorted(list(zip(indices.squeeze().tolist(),distances.squeeze().tolist())),key=lambda x: x[1])[:0:-1]
        recommend_frame = []
        for val in rec_movie_indices:
            movie_idx = final_dataset.iloc[val[0]]['movieId']
            idx = movies[movies['movieId'] == movie_idx].index
            recommend_frame.append({'Title':movies.iloc[idx]['title'].values[0],'Distance':val[1]})
        df = pd.DataFrame(recommend_frame,index=range(1,n_movies_to_reccomend+1))
        return df
    else:
        return "No movies found. Please check your input"


# In[38]:


get_movie_recommendation('Inception')


# In[23]:


get_movie_recommendation('Memento')


# In[28]:


get_movie_recommendation('Kill Bill: Vol. 2')


# In[ ]:




