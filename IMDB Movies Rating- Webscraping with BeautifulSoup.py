#!/usr/bin/env python
# coding: utf-8

# ### IMPORT LIBRARIES

# In[15]:


# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl


# ### CREATE EMPTY EXCEL SHEET TO TAKE SCRAPED FILE

# In[16]:


# create an excel file
IMDB_Movies_Excel = openpyxl.Workbook()

# Assign the excel sheet and name it
sheet = IMDB_Movies_Excel.active
sheet.title = "IMDB Movies Rating"
print(IMDB_Movies_Excel.sheetnames)

sheet.append(['Rank', 'Name', 'Year', 'IMDB_Rating'])


# ### WEBSCRAPING, CONVERTING SCRAPED DATA TO A LIST

# In[22]:


# Initialize an empty list to store movie ratings
Movie_Rating_List = []

# Try to scrape the IMDb top 250 movies webpage
try:
    # Send a GET request to the IMDb webpage and set a timeout
    source = requests.get("https://www.imdb.com/chart/top/", headers={'User-Agent': 'Mozilla/5.0'}, timeout=1000)
    source.raise_for_status()  # Raise an error if the response is not successful
    
    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(source.text, "html.parser")
    
    # Find the list containing movie details
    movies_250 = soup.find("ul", class_="ipc-metadata-list ipc-metadata-list--dividers-between sc-71ed9118-0 kxsUNk compact-list-view ipc-metadata-list--base", role="presentation")
    
    # Find all list items containing individual movie details
    movies_250_all = movies_250.find_all("li", class_="ipc-metadata-list-summary-item sc-1364e729-0 caNpAE cli-parent")
    
    # Iterate through each movie in the list
    for movie in movies_250_all:
        # Extract movie name, removing the period at the beginning
        Name = movie.find("h3", class_="ipc-title__text").text.split(".")[1]
        
        # Extract movie rank
        Rank = movie.find("h3", class_="ipc-title__text").text.split(".")[0]
        
        # Extract movie release year
        Year = movie.find("span", class_="sc-be6f1408-8 fcCUPU cli-title-metadata-item").text
        
        # Extract IMDb rating of the movie
        IMDB_rating = movie.find("span", class_="ipc-rating-star--imdb")
        IMDB_rating = IMDB_rating.text.strip()[:3]  # Extracting only the rating value
        
        # Store movie details in a list
        data = [Rank, Name, Year, IMDB_rating]
        
        # Append the movie details to the main list
        Movie_Rating_List.append(data)
        
        # Append movie details to excel sheet
        sheet.append(data)
        
# Handle exceptions that may occur during the scraping process
except Exception as e:
    print(e)  # Print the error message if an exception occurs


# ### SCRAPED DATA TO DATAFRAME

# In[23]:


# Define the column names for the DataFrame
columns = ['Rank', 'Name', 'Year', 'IMDB_Rating']

# Create a DataFrame using the collected movie rating data and column names
IMDB_Movie_Rating = pd.DataFrame(data=Movie_Rating_List, columns=columns)

# Print the DataFrame containing IMDb movie ratings
print(IMDB_Movie_Rating)


# ### SAVE EXCEL SHEET AND DATAFRAME CREATED LOCALLY

# In[26]:


IMDB_Movies_Excel.save("IMDB Movies Rating_250.xlsx")
IMDB_Movie_Rating.to_csv("IMDB Movies DataFrame.csv")

