"""
    This test.py is designed to identify the data, its visualisation and analytical info.
    
"""
from data_preprocessing import *
from analysis import *

# define the data
data = rec_data()

# read the data from the folder specified
data.read_data('data/')

# some summery info to understand the data, uncomment to see the results

print(data.shape())
print(data.num_of_movies())
print(data.num_of_null())
print(data.head())



# finds the publishing year of the movie
obtain_year(data)

#plots the histogram for movie publisher per year
plot_hist(data.data)

# plots the rating by genre in histogram
plot_rating_by_genre(data.data)

# barchart of genre popularity
plot_bar_popgenre(data.data)

# histogram of ratings distribution
num_of_ratings(data.data)

# scatterplots the ratings vs num_ratings 
ratings_vs_num_ratings(data.data)