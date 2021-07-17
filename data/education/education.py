# -*- coding: utf-8 -*-
"""
Created on Sun Jul 18 01:01:38 2021

@author: flama
"""


import pandas as pd
import statsmodels.api as sm
from tqdm import tqdm

asheville = pd.read_csv('asheville.csv')
austin = pd.read_csv('austin.csv')
la = pd.read_csv('los_angeles.csv')
nashville = pd.read_csv('nashville.csv')
new_orleans = pd.read_csv('new_orleans.csv')

asheville.rename(columns={asheville.columns[0]:'date',asheville.columns[1]:'education'},inplace=True)
austin.rename(columns={austin.columns[0]:'date',austin.columns[1]:'education'},inplace=True)
la.rename(columns={la.columns[0]:'date',la.columns[1]:'education'},inplace=True)
nashville.rename(columns={nashville.columns[0]:'date',nashville.columns[1]:'education'},inplace=True)
new_orleans.rename(columns={new_orleans.columns[0]:'date',new_orleans.columns[1]:'education'},inplace=True)

asheville.iloc[-1,0] = '2019-12-26'
austin.iloc[-1,0] = '2019-12-26'
la.iloc[-1,0] = '2019-12-26'
nashville.iloc[-1,0] = '2019-12-26'
new_orleans.iloc[-1,0] = '2019-12-26'

city_list = [asheville, new_orleans, nashville, austin, la]
cl = ['asheville', 'new_orleans', 'nashville', 'austin', 'la']

for i in range(len(city_list)):
    city_list[i] = city_list[i].set_index(pd.to_datetime(city_list[i]['date']))
    city_list[i] = city_list[i].resample('M',label='left').first()
    city_list[i]['tmp'] = [i for i in range(len(city_list[i]))]

    tmp = city_list[i]
    tmp['date'] = list(tmp.index)
    tmp['date'] = tmp['date'].apply(lambda x: str(x).split()[0])
    tmp.reset_index(drop=True,inplace=True)
    
    tmp.ffill(inplace=True,limit=6)
    tmp.bfill(inplace=True)
    city_list[i] = tmp
    
date_range = city_list[0].date.unique()

combined = [[i,j,0] for i in date_range for j in cl]
df = pd.DataFrame(combined,columns=['date','city','education'])

for i in range(len(city_list)):
    for row, s in city_list[i].iterrows():
        mask = (df['date'] == s['date']) & \
                (df['city'] == cl[i])
        df.loc[mask, 'education'] = s['education']
        
df.to_csv('education.csv')