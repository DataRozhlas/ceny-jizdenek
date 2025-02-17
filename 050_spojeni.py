#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd
import datetime
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 500)


# In[2]:


df = pd.DataFrame()
for f in [x for x in os.listdir("data") if x[2] == "_"]:
    df = pd.concat([df, pd.read_parquet(os.path.join("data",f))])


# In[3]:


df['oscrapovano_minuty'] = df['oscrapovano'].apply(lambda x: str(x)[0:14])


# In[4]:


df['oscrapovano_minuty']


# In[5]:


df = df.drop_duplicates(subset=['odkud','kam','odjezd','oscrapovano_minuty'], keep="last")


# In[6]:


len(df)


# In[7]:


df[['odjezd','odkud','kam']].drop_duplicates().shape[0]


# In[8]:


df.groupby(['prodejce',pd.Grouper(key='oscrapovano',freq='D')]).size()


# Výpadek ČD 2024-11-26 opraven, vyřešen.

# In[10]:


df = df.sort_values(by="oscrapovano").reset_index(drop=True)


# In[11]:


df = df.dropna(subset=['odkud','kam','odjezd','oscrapovano'],how='any')


# In[12]:


df = df[df['prostredek'] != 'autobus']


# In[13]:


df = df[~df['kam'].str.contains('(tief)',na=False)]
df = df[~df['odkud'].str.contains('(tief)',na=False)]


# Před 7. listopadem scrapování testovací a nesystematické = nevypovídající = filtrujeme.

# In[15]:


df = df[df['oscrapovano'] >= '2024-11-08']


# In[16]:


df.groupby(['prodejce',pd.Grouper(key='oscrapovano',freq='D')]).size()


# In[17]:


days = {0: 'po', 1: 'út', 2: 'st', 3: 'čt', 
        4: 'pá', 5: 'so', 6: 'ne'}
df['den'] = df['odjezd'].dt.dayofweek.map(days)


# In[18]:


df['predstih_d'] = df['predstih'].dt.days
df['predstih_h'] = df['predstih'].dt.total_seconds() / 3600


# In[19]:


df = df[df['predstih_h'] > -3]


# In[20]:


kategoricka_data = ['odkud','kam','prodejce','den']


# In[21]:


for k in kategoricka_data:
    print("Before:", df[k].memory_usage(deep=True))
    df[k] = df[k].astype('category')
    print("After: ", df[k].memory_usage(deep=True))


# In[22]:


df['cena'] = pd.to_numeric(df['cena'])


# In[23]:


df.shape[0]


# In[24]:


df[['odjezd','odkud','kam']].drop_duplicates().shape[0]


# In[25]:


poradi = ['oscrapovano','prodejce','odkud','kam',
 'odjezd',
 'predstih',
 'predstih_d',
 'predstih_h',
          'cena',
 'prostredek',
          'volnych_mist',
 'obsazenost',
 'jizdni_doba',
 'vzdalenost',
 'zpozdeni',
 'cena_poznamka',
 'den',
 'prestupy',
'vlaky',
 'mistenka_zdarma',
 'nahradni_bus',
 'volna_mista_economy',
 'volna_mista_economy_plus',
 'volna_mista_economy_business',
 'volna_mista_premium']


# In[26]:


df[poradi].to_parquet(os.path.join("data","jizdenky.parquet"))


# In[27]:


nejnovejsi = df['oscrapovano'].max()
nejnovejsi
df_tyden = df[df['oscrapovano'] > (nejnovejsi - datetime.timedelta(hours=168))]


# In[28]:


df_tyden[poradi].to_csv(os.path.join("data","jizdenky_tyden.csv"))


# In[ ]:




