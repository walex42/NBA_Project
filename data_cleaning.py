from scraper import scrapeSalary
import pandas as pd

def salaryClean(df):
    #We removed the inflatoin adjested salary because the values might constantly change
    #This might give us a better model in the future
    df.drop(columns=['inflationAdjSalary'])
    #This would remove most of the rookie contracts or players who just fill space on a team
    newDF = df[df["salary"]>1000000]
    newDF = newDF.reset_index()
    return newDF
