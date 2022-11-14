# -*- coding: utf-8 -*-
"""
Created on Thursday, November 10th 2022

@author: Michael ODonnell

@purpose: scrape UNCW mens basketball games
"""

# import needed libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time

def scrape_UNCW_basketball_season(year: int):
    
    # start a timer
    start = time.time()

    # URL to scrape
    url = f'https://www.sports-reference.com/cbb/schools/north-carolina-wilmington/{year}-gamelogs.html'
    
    # collect HTML data
    response = requests.get(url)
    
    # check response status code
    # if response code != 200, print
    if response.status_code != 200:  
        print(f"invalid url response code for year {year}: {response.status_code}")
    
    try:    
        # create beautiful soup object from HTML
        soup = BeautifulSoup(response.content, features="lxml")
        
        # use getText()to extract the column headers into a list
        columns = [th.getText() for th in soup.findAll('tr', limit=2)[1].findAll('th')]
        columns = columns[1:]
        
        # get the data from each row
        row_data = soup.findAll('tr')[1:]
        
        # turn the row data into a list
        rows_data_list = [[td.getText() for td in row_data[i].findAll('td')]
                            for i in range(len(row_data))]
        # exclude the conferences from the row data
        rows_data_list = [l for l in rows_data_list if len(l) > 2]
            
        # create a dataframe with all aquired info
        uncw_season = pd.DataFrame(data = rows_data_list,
                                    columns = columns)
        
        # add the year to the standings
        uncw_season["year"] = year
        
        # change column names
        uncw_season.columns = ['date', 'game_location', 'opponent', 'W/L', 'points',
                               'opponent_points', 'team_FG', 'team_FGA', 'team_FG%',
                               'team_3P', 'team_3PA', 'team_3P%', 'team_FT', 'team_FTA',
                               'team_FT%', 'team_ORB', 'team_TRB', 'team_AST', 'team_STL',
                               'team_BLK', 'team_TOV', 'team_PF', 'remove',
                               'opponent_FG', 'opponent_FGA', 'opponent_FG%',
                               'opponent_3P', 'opponent_3PA', 'opponent_3P%', 'opponent_FT',
                               'opponent_FTA', 'opponent_FT%', 'opponent_ORB',
                               'opponent_TRB', 'opponent_AST', 'opponent_STL',
                               'opponent_BLK', 'opponent_TOV', 'opponent_PF', 'year']
        uncw_season = uncw_season.drop(['remove'], axis = 1)
        
        # change column data types
        for col in ['points',
                   'opponent_points', 'team_FG', 'team_FGA', 'team_FG%',
                   'team_3P', 'team_3PA', 'team_3P%', 'team_FT', 'team_FTA',
                   'team_FT%', 'team_ORB', 'team_TRB', 'team_AST', 'team_STL',
                   'team_BLK', 'team_TOV', 'team_PF',
                   'opponent_FG', 'opponent_FGA', 'opponent_FG%',
                   'opponent_3P', 'opponent_3PA', 'opponent_3P%', 'opponent_FT',
                   'opponent_FTA', 'opponent_FT%', 'opponent_ORB',
                   'opponent_TRB', 'opponent_AST', 'opponent_STL',
                   'opponent_BLK', 'opponent_TOV', 'opponent_PF']:
            try:
                uncw_season[col] = uncw_season[col].astype(float)
            except:
                print(f"could not update column {col} year {year} data type")

        # remove special and extra characters from W/L column
        uncw_season['W/L'] = uncw_season['W/L'].str.replace('[^\w\s]','')
        uncw_season['W/L'] = uncw_season['W/L'].astype(str).str[0]
        
        # update values in game_location column
        uncw_season["game_location"] = np.where(uncw_season["game_location"] == "@", "away", uncw_season["game_location"])
        uncw_season["game_location"] = np.where(uncw_season["game_location"] == "", "home", uncw_season["game_location"])
        uncw_season["game_location"] = np.where(uncw_season["game_location"] == "N", "nuetral_site", uncw_season["game_location"])
        
        # end the timer
        end = time.time()
        print(f"SCRAPED: UNCW mens basketball season {year} in {round(end-start, 2)} seconds")
        return uncw_season
    
    except:
        print(f"FAILED: could not scrape UNCW mens basketball season {year}")