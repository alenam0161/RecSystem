"""
Data reading,preprocessing and info return

Returns:
    rec_data: the format for recommendation system for movie system
    
"""
import os
import numpy as np
import pandas as pd

class rec_data:
    """
    Data for recommendation system
    """
    def __init__(self,movies = None,ratings = None,data = None):
        self.movies = movies
        self.ratings = ratings
        self.data = data
    def read_data(self,fl_name):
        """reads the data

        Args:
            fl_name (string): location of movies and ratings csv
            which should contain movies.csv and ratings.csv
        """
        self.movies = pd.read_csv(fl_name + 'movies.csv')
        self.ratings = pd.read_csv(fl_name + 'ratings.csv')
        # merge the data on given column
        self.data = pd.merge(left = self.movies, right = self.ratings, on = 'movieId')
    def shape(self):
        """

        Returns:
            shape: shape
        """
        return self.data.shape
    def num_of_null(self):
        """null sum of columns

        Returns:
            list: list of integers
        """
        return self.data.isnull().sum()
    def num_of_movies(self,column = 'movieId'):
        """
        returns num of unique values

        Args:
            column (str):  Defaults to 'movieId'.

        Returns:
            list: list of nulls
        """
        return self.data[column].nunique()
    def head(self):
        """
        Returns:
            DataFrame: head of DataFrame
        """
        return self.data.head()

def obtain_year(df : rec_data):
    """return years of publishment

    Args:
        df (rec_data): RecSystem DataFrame
    """
    years = []

    for title in df.data['title']:
        year_subset = title[-5:-1]
        try: years.append(int(year_subset))
        except: years.append(9999)
            
    df.data['moviePubYear'] = years
    #prints values
    print(len(df.data[df.data['moviePubYear'] == 9999]))
    print(df.data[df.data['moviePubYear'] == 9999])