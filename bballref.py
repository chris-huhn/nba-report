# import libraries
from bs4 import BeautifulSoup
import datetime as dt
import pandas as pd
import requests
import numpy as np

# scrape basketball reference scores page
url = 'https://www.basketball-reference.com/boxscores/'
html = requests.get(url).content
df_list = pd.read_html(html)

# list ofd box score dataframes for every game night, indexing to isolate box scores
scores = df_list[:-2:3]

# change column names
for i in scores:
    i.columns = ['Teams', 'Score', 'Progress']
    
# change NaN values to ''
for i in range(len(scores)):
    scores[i] = scores[i].replace(np.nan, '', regex=True)
    
# create scores dataframe
scores_df = pd.concat(scores, ignore_index=True)

# insert a blank line between each score in the dataframe
myarr = range(len(scores_df)+3)[2::3]
for i in myarr:
    line = pd.DataFrame({'Teams':'', 'Score':'', 'Progress':''}, index=[i])
    scores_df = pd.concat([scores_df.iloc[:i], line, scores_df.iloc[i:]]).reset_index(drop=True)
    
# create index column list to show home and away teams
mylist = [['Away', 'Home', ''] for i in scores]
mylist = [item for sublist in mylist for item in sublist]
del mylist[-1]

# reset indes to my_list
scores_df.index = mylist

# export to excel
scores_df.to_excel(f'NBA-report_{dt.date.today()}.xlsx')