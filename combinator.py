from scraper import scrapeSalary, get_stats
from data_cleaning import salaryClean, playerSeasonClean
import pandas as pd
import string as str
import time

#This is the main file for recieving the end CSVs
#After running this you should have generated a CSV that you can use for further analysis

#Gather the Salary data
salaryDF = scrapeSalary();
cleanSalary = salaryClean(salaryDF);


#Gather the list of players
#We are generating a final dataframe with the 200 highest earners of 2021
season = cleanSalary[cleanSalary['SEASON'] == 2021]
season = season[0:201]
playerList = season['playerName'].unique().tolist()
playerList = [x.lower() for x in playerList]
playerList = [x.replace("'", "") for x in playerList]
#These players are excluded because they would not return the right values, this is caused by the way basketball reference reports statistics. 
#Also some players listed in the bad inputs are also rookies who would not have season stats to use yet
badInputs = ["dangelo russell" ,"clint capela", 'paolo banchero', 'jaden ivey', 'bennedict mathurin', "chet holmgren", 'royce oneale', "maxi kleber", "nicolas claxton",
 "tj mcconnell", "scottie barnes", 'cedi osman', 'jaesean tate']
 #Final list
finalPlayers = [i for i in playerList if i not in badInputs]


#Collecting player stats and merging with salary
finalDF = pd.DataFrame()
#Iterate through the list of players we selected
for player in finalPlayers:
    playerStat = get_stats(player, stat_type='PER_GAME', playoffs=False, career=False)
    cleanPlayerStat = playerSeasonClean(playerStat)
    #Get all the salaries for a given player
    playerSalary = cleanSalary[cleanSalary['playerName'] == player]
    #Merge the two data frames
    completePlayer = pd.merge(playerSalary, cleanPlayerStat, on=['SEASON'])
    completePlayer.reset_index()
    #Add it to the final database that we will return
    finalDF = pd.concat([finalDF, completePlayer], ignore_index=True)
    #Rate limiter due to updated website policies
    time.sleep(3.5)

#Send final dataframe to csv
finalDF.to_csv('final.csv', index=False)
