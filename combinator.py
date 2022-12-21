from scraper import scrapeSalary, get_stats
from data_cleaning import salaryClean, playerSeasonClean
import pandas as pd
import string as str

#Gather the Salary data
salaryDF = scrapeSalary();
cleanSalary = salaryClean(salaryDF);

#Gather the list of players
playerList =cleanSalary['playerName'].unique().tolist()
playerList = [x.lower() for x in playerList]

#Collecting player stats and merging with salary
finalDF = pd.DataFrame()
for player in playerList:
    if(player == "jermaine o'neal" or player == "shaquille o'neal"):
        continue
    playerStat = get_stats(player, stat_type='PER_GAME', playoffs=False, career=False)
    cleanPlayerStat = playerSeasonClean(playerStat)
    playerSalary = cleanSalary[cleanSalary['playerName'] == player]
    completePlayer = pd.merge(playerSalary, cleanPlayerStat, on=['SEASON'])
    completePlayer.reset_index()
    finalDF = pd.concat([finalDF, completePlayer], ignore_index=True)

#Send final dataframe to csv
finalDF.to_csv('final.csv', index=False)
