#!/usr/bin/env python
# coding: utf-8

# ## Assignment IBM
# ### To scrape the given Wikipedia page and create a Dataframe.
# 
# Transform the data on Wiki page into pandas dataframe

# Import Libraries

# In[5]:


from bs4 import BeautifulSoup
import requests
import pandas as pd


# Scrap List of postal codes of Canada wiki page content by using BeautifulSoup

# In[6]:


# download url data from internet
url = "https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M"
source = requests.get(url).text
Canada_data = BeautifulSoup(source, 'lxml')


# Convert content of PostalCode HTML table as dataframe

# In[7]:


`# creat a new Dataframe
column_names = ['Postalcode','Borough','Neighborhood']
toronto = pd.DataFrame(columns = column_names)

# loop through to find postcode, borough, neighborhood 
content = Canada_data.find('div', class_='mw-parser-output')
table = content.table.tbody
postcode = 0
borough = 0
neighborhood = 0

for tr in table.find_all('tr'):
    i = 0
    for td in tr.find_all('td'):
        if i == 0:
            postcode = td.text
            i = i + 1
        elif i == 1:
            borough = td.text
            i = i + 1
        elif i == 2: 
            neighborhood = td.text.strip('\n').replace(']','')
    toronto = toronto.append({'Postalcode': postcode,'Borough': borough,'Neighborhood': neighborhood},ignore_index=True)

# clean dataframe 
toronto = toronto[toronto.Borough!='Not assigned']
toronto = toronto[toronto.Borough!= 0]
toronto.reset_index(drop = True, inplace = True)
i = 0
for i in range(0,toronto.shape[0]):
    if toronto.iloc[i][2] == 'Not assigned':
        toronto.iloc[i][2] = toronto.iloc[i][1]
        i = i+1
                                 
df = toronto.groupby(['Postalcode','Borough'])['Neighborhood'].apply(', '.join).reset_index()
df.head()


# ## Data Cleaning
# Drop "None" rows in DataFrame
# 
# Drop any row which contains 'Not assigned' value
# 
# All "Not assigned" will be replace to 'NaN' using numpy for convenience.

# In[12]:


df = df.dropna()
empty = 'Not assigned'
df = df[(df.Postalcode != empty ) & (df.Borough != empty) & (df.Neighborhood != empty)]


# In[13]:


df.head()


# In[15]:


def neighborhood_list(grouped):    
    return ', '.join(sorted(grouped['Neighborhood'].tolist()))
                    
grp = df.groupby(['Postalcode', 'Borough'])
df2 = grp.apply(neighborhood_list).reset_index(name='Neighborhood')


# In[18]:


print(df2.shape)
df2.head()


# In[ ]:




