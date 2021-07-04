# -*- coding: utf-8 -*-
"""
Created on Sun Jul  4 18:26:22 2021

@author: admin
"""

import numpy as np
import pandas as pd
from flask import Flask, render_template, request

#Read and merge the dataframes
def read_df():
    df1 = pd.read_csv("manga_details.csv")
    manga_titles = pd.read_csv("manga.csv")
    # Merge the 2 dataframes
    df = pd.merge(df1, manga_titles, on = 'MangaID')
    return df


# Let's create a function to return the 5 most similar manga
def recmd(manga):
    df = read_df()
    result = pd.DataFrame()
    mangamat = df.pivot_table(index='User',columns='Title',values='Score')
    ratings = pd.DataFrame(df.groupby('Title')['Score'].mean())
    ratings["num of ratings"] = pd.DataFrame(df.groupby('Title')['Score'].count())
    if manga not in df['Title'].unique():
        return('This manga is not in our database.\nPlease check if you spelled it correct.')
    else:
        manga_user_ratings = mangamat[manga]
        similar = mangamat.corrwith(manga_user_ratings)
        corr = pd.DataFrame(similar,columns=['Correlation'])
        corr.dropna(inplace=True)
        corr = corr.join(ratings['num of ratings'])
        result = corr[corr['num of ratings']>100].sort_values('Correlation',ascending=False).head(6)
        return result.index[1:]
    
mangaList = (recmd("Bleach"))  
print(mangaList)  

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/recommend")
def recommend():
    manga = request.args.get('manga')
    r = recmd(manga)
    if type(r)==type('string'):
        return render_template('recommend.html',manga=manga,r=r,t='s')
    else:
        return render_template('recommend.html',manga=manga,r=r,t='l')
    
    
if __name__ == '__main__':
    app.run()