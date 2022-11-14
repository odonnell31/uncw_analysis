# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 22:25:22 2022

@author: ODsLaptop
"""

import UNCW_basketball_scraper_V1 as uncw
import time
import pandas as pd

all_time_games = pd.DataFrame()

for y in range(2009, 2022):
    time.sleep(20)
    season = uncw.scrape_UNCW_basketball_season(year = y)
    all_time_games = all_time_games.append(season)
    
all_time_games.to_csv("uncw_.csv", index = False)