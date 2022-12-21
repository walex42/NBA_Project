import pandas as pd
from datetime import date
from bs4 import BeautifulSoup
from requests import get
from br_api.util import get_player_suffix
from br_api.lookup import lookup

#This is the web scraping function to gather salary data
#I scrape the data for seasons 2009-2010 to 2017-2018.
#I left out the more recent seasons becasue the were major rule changes in salary and luxuary tax that caused salary inflation.
#After that came the pandemic which put a hold on sports and the salaries players made

def scrapeSalary():
    df = pd.DataFrame(columns=['playerName', 'seasonStartYear', 'salary', 'inflationAdjSalary'])
    current_yr = int(date.today().strftime('%Y'))
    for year in range(2010, 2019):
        try:
                url = 'https://hoopshype.com/salaries/players/{}-{}/'.format(year-1, year)
                #Table of all players salaries from a given year
                table = pd.io.html.read_html(url)[0]
                table.drop(columns=["Unnamed: 0"], inplace = True)
                table.set_axis(['playerName', 'salary', 'inflationAdjSalary'], axis=1, inplace=True)
                table['seasonStartYear'] = year - 1
                #adding the yearly salaries to the year over year dataframe
                df = pd.concat([df, table])
        except ValueError:
                continue

    # Get the current season salary
    table = pd.io.html.read_html('https://hoopshype.com/salaries/players/')[0]
    table = table.iloc[:, [1,2]]
    table.set_axis(['playerName', 'salary'], axis=1, inplace=True)
    #Add what season the data is from
    table['seasonStartYear'] = current_yr - 1
    df = pd.concat([df, table])
    return df

#This is the function to web scrap data from basketball reference
#They do have the abiility to download any table to a CSV but that would mean hundreds of csv files to manage
def get_stats(_name, stat_type='PER_GAME', playoffs=False, career=False, ask_matches = True):
    #Use the lookup functions to confirm the name
    name = lookup(_name, ask_matches)
    #Generate suffix of URL
    suffix = get_player_suffix(name)
    if suffix:
        suffix = suffix.replace('/', '%2F')
    else:
        return pd.DataFrame()
    selector = stat_type.lower()
    if playoffs:
        selector = 'playoffs_'+selector
    #Go to URL of the player suffix that you just generated as well as the specific table you want to scrape data from
    r = get(f'https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url={suffix}&div=div_{selector}')
    if r.status_code==200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        if table is None:
            return pd.DataFrame()
        df = pd.read_html(str(table))[0]
        #Selecting the columns we want and naming them
        df.rename(columns={'Season': 'SEASON', 'Age': 'AGE',
                  'Tm': 'TEAM', 'Lg': 'LEAGUE', 'Pos': 'POS'}, inplace=True)
        if 'FG.1' in df.columns:
            df.rename(columns={'FG.1': 'FG%'}, inplace=True)
        if 'eFG' in df.columns:
            df.rename(columns={'eFG': 'eFG%'}, inplace=True)
        if 'FT.1' in df.columns:
            df.rename(columns={'FT.1': 'FT%'}, inplace=True)

        career_index = df[df['SEASON']=='Career'].index[0]
        if career:
            df = df.iloc[career_index+2:, :]
        else:
            df = df.iloc[:career_index, :]

        df = df.reset_index().drop('index', axis=1)
        return df