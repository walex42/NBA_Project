import smtpd
from scraper import scrapeSalary
import pandas as pd

def salaryClean(df):
    df.rename(columns={'seasonStartYear': 'SEASON'}, inplace=True)
    df['SEASON'] = df['SEASON'].astype(str).astype(int)
    df['playerName'] = df['playerName'].str.lower()

    #We removed the inflatoin adjested salary because the values might constantly change
    #This might give us a better model in the future
    df = df.drop(columns=['inflationAdjSalary'])
    #This would remove most of the rookie contracts or players who just fill space on a team
    df['salary'] = df['salary'].str.slice(start=1)
    df['salary'] = df['salary'].str.replace(",", "")
    df['salary'] = df['salary'].astype(str).astype(int)
    newDF = df[df["salary"]>1000000]
    newDF = newDF.reset_index()
    return newDF

def playerSeasonClean(playerDF):
    playerDF['SEASON']= playerDF['SEASON'].str.slice(stop=4)
    playerDF = playerDF.drop(columns=['TEAM', 'LEAGUE','POS','G', 'GS'], inplace=True)
    playerDF['SEASON'] = playerDF['SEASON'].astype(str).astype(int)
    alignedDF = playerDF[playerDF["SEASON"] > 2009]
    alignedDF = playerDF[playerDF["SEASON"] < 2020]
    return alignedDF

