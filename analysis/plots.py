"""
Plottings
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
from data_preprocessing import *

def make_histogram(dataset, attribute, bins=25, bar_color='#3498db', edge_color='#2980b9', title='Title', xlab='X', ylab='Y', sort_index=False):
    """histogram

    Args:
        dataset (rec_data): RecSystem dataformat
        attribute (string): column
        bins (int, optional): bins. Defaults to 25.
        bar_color (str, optional): bar_color. Defaults to '#3498db'.
        edge_color (str, optional): edge_color. Defaults to '#2980b9'.
        title (str, optional): title. Defaults to 'Title'.
        xlab (str, optional): xlab. Defaults to 'X'.
        ylab (str, optional): ylab. Defaults to 'Y'.
        sort_index (bool, optional): sort_index. Defaults to False.
    """
    if attribute == 'moviePubYear':
        dataset = dataset[dataset['moviePubYear'] != 9999]
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_title(title, fontsize=24, pad=20)
    ax.set_xlabel(xlab, fontsize=16, labelpad=20)
    ax.set_ylabel(ylab, fontsize=16, labelpad=20)
    
    plt.hist(dataset[attribute], bins=bins, color=bar_color, ec=edge_color, linewidth=2)
    
    plt.xticks(rotation=45)
    plt.show()
def make_bar_chart(dataset, attribute, bar_color='#3498db', edge_color='#2980b9', title='Title', xlab='X', ylab='Y', sort_index=False):
    """_summary_

    Args:
        dataset (rec_data): RecSystem dataformat
        attribute (string): column
        bar_color (str, optional): bar_color. Defaults to '#3498db'.
        edge_color (str, optional): edge_color. Defaults to '#2980b9'.
        title (str, optional): title. Defaults to 'Title'.
        xlab (str, optional): xlab. Defaults to 'X'.
        ylab (str, optional): ylab. Defaults to 'Y'.
        sort_index (bool, optional): sort_index. Defaults to False.
    """
    if sort_index == False:
        xs = dataset[attribute].value_counts().index
        ys = dataset[attribute].value_counts().values
    else:
        xs = dataset[attribute].value_counts().sort_index().index
        ys = dataset[attribute].value_counts().sort_index().values
        
    
    fig, ax = plt.subplots(figsize=(14, 7))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_title(title, fontsize=24, pad=20)
    ax.set_xlabel(xlab, fontsize=16, labelpad=20)
    ax.set_ylabel(ylab, fontsize=16, labelpad=20)
    
    plt.bar(x=xs, height=ys, color=bar_color, edgecolor=edge_color, linewidth=2)
    plt.xticks(rotation=45)
    plt.show()
def plot_hist(data : rec_data):
    """plots the histogram of movies published per year

    Args:
        data (rec_data): RecSystem dataformat
    """
    make_histogram(data, 'moviePubYear', title='Movies Published per Year', xlab='Year', ylab='Counts')
def plot_rating_by_genre(data: rec_data):
    """
    plots ratings by genre

    Args:
        data (rec_data): _description_
    """
    values = defaultdict(list)
    for ind, row in data.iterrows():
        for genre in row['genres'].split('|'):
            values[genre].append(row['rating'])
            
            
    genre_lst, rating_lst = [], []
    for key, item in values.items():
        if key not in [0, 1]:
            genre_lst.append(key)
            rating_lst.append(np.mean(item))
            
            
    genres_with_ratings = pd.DataFrame([genre_lst, rating_lst]).T
    genres_with_ratings.columns = ['Genre', 'Mean_Rating']
    make_histogram(genres_with_ratings,
                   'Mean_Rating',
                   title = "Distribution of Movie Ratings",
                   xlab = 'Rating',
                   ylab = "Count")
def plot_bar_popgenre(data : rec_data):
    """
    Plots the bar for popularity of Genres
    """
    
    genre_df = pd.DataFrame(data['genres'].str.split('|').tolist(), index=data['movieId']).stack()
    genre_df = genre_df.reset_index([0, 'movieId'])
    genre_df.columns = ['movieId', 'Genre']
    make_bar_chart(genre_df, 'Genre', title='Most Popular Movie Genres', xlab='Genre', ylab='Counts')

def num_of_ratings(data : rec_data):
    """
    plots number of ratings distribution
    """
    
    num_ratings = pd.DataFrame(data.groupby('movieId').count()['rating']).reset_index()
    data = pd.merge(left=data, right=num_ratings, on='movieId')
    data.rename(columns={'rating_x': 'rating', 'rating_y': 'numRatings'}, inplace=True)
    make_histogram(data,'numRatings', title = 'Number of Ratings Distribution', xlab = 
                   'Number of Ratings', ylab = 'Counts')
def ratings_vs_num_ratings(data : rec_data):
    """plots the Rating vs Number of Ratings

    Args:
        data (rec_data): RecSystem format
    """
    ratings_df = pd.DataFrame()
    ratings_df['Mean_Rating'] = data.groupby('title')['rating'].mean().values
    ratings_df['Num_Ratings'] = data.groupby('title')['rating'].count().values


    fig, ax = plt.subplots(figsize=(14, 7))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_title('Rating vs. Number of Ratings', fontsize=24, pad=20)
    ax.set_xlabel('Rating', fontsize=16, labelpad=20)
    ax.set_ylabel('Number of Ratings', fontsize=16, labelpad=20)

    plt.scatter(ratings_df['Mean_Rating'], ratings_df['Num_Ratings'], alpha=0.5)
    plt.show()