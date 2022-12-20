import pandas as pd
import string
from datetime import date
from bs4 import BeautifulSoup
from requests import get
import requests
import re
try:
    from br_api.util import get_player_suffix
    from br_api.lookup import lookup
except:
    from br_api.util import get_player_suffix
    from br_api.lookup import lookup

def scrapeSalary():
    """
    I scrape the data for seasons 2009-2010 to 2019-2020. 
    """
    df = pd.DataFrame(columns=['playerName', 'seasonStartYear', 'salary', 'inflationAdjSalary'])
    current_yr = int(date.today().strftime('%Y'))
    for year in range(2010, 2020):
        url = 'https://hoopshype.com/salaries/players/{}-{}/'.format(year-1, year)
        table = pd.io.html.read_html(url)[0]
        table.drop(columns=['Unnamed: 0'], inplace=True)
        table.set_axis(['playerName', 'salary', 'inflationAdjSalary'], axis=1, inplace=True)
        table['seasonStartYear'] = year - 1
        df = pd.concat([df, table])

    # Get the current season salary
    table = pd.io.html.read_html('https://hoopshype.com/salaries/players/')[0]
    table = table.iloc[:, [1,2]]
    table.set_axis(['playerName', 'salary'], axis=1, inplace=True)
    table['seasonStartYear'] = current_yr - 1
    df = pd.concat([df, table])
    #df.to_csv(dest_file, index=False)
    return df


def getSeasonStatSoup(year, stat_type='per game'):
	stat_type = stat_type.lower()
	stat_type_dict = {'per game': 'per_game', 'total': 'totals', 'per 36': 'per_minute', 'advanced': 'advanced'}
	if stat_type not in stat_type_dict.keys():
		print ("Stat type not supported. Valid options: " + str(stat_type_dict.keys()))
	else:

		# basketball-reference season stat page
		base_url = 'http://www.basketball-reference.com/leagues/NBA_'+str(year)+'_per_game.html'
		#url = base_url % {'year': year, 'stat_type_str': stat_type_dict[stat_type]}

		# BeautifulSoup parsing only works with "xml" parsing option -- not exactly sure why
		r = requests.get(base_url)
		soup = BeautifulSoup(r.text, "xml")

		return soup

def getPlayerYear(name, year, stat_type='per game'):

	soup = getSeasonStatSoup(year, stat_type)

	if soup is not None:

		# get category strings -- this assumes same order as stats
		cats = []
		cat_parent = soup.find('tr', class_='no_ranker thead')
		if cat_parent != None:
			cats_html = cat_parent.find_all('th')
			for cat in cats_html:
				cats.append(cat.get('data-stat'))

		# transform player name to "Last, First" format
		name_list = name.split(' ')
		#name_list.reverse()
		csk_str = ','.join(name_list)

		# find player via csk_str, then iterate over stat entries
		stats = []
		tag = soup.find('td', csk=csk_str)
		if tag != None:
			stats_html = tag.parent.find_all('td')
			for stat in stats_html:
				# remove asterisk from some players
				stats.append(re.sub('\*','',stat.get_text())) 

		player_stats = dict(zip(cats, stats))
		return player_stats

def listPlayers(year):

	soup = getSeasonStatSoup(year)
	player_list = []
	tds = soup.find_all('td')
	for td in tds:
		txt = td.get_text()
		if td.has_attr('csk') and (re.search('\d', txt) == None) and (txt not in player_list):
			player_list.append(txt)
	return player_list

def getPlayerStats(salaryDF):
	statsDF = pd.DataFrame()
	for index, row in salaryDF.iterrows():
		print(row['c1'], row['c2'])
	return statsDF


def get_stats(_name, stat_type='PER_GAME', playoffs=False, career=False, ask_matches = True):
    name = lookup(_name, ask_matches)
    suffix = get_player_suffix(name)
    if suffix:
        suffix = suffix.replace('/', '%2F')
    else:
        return pd.DataFrame()
    selector = stat_type.lower()
    if playoffs:
        selector = 'playoffs_'+selector
    r = get(f'https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url={suffix}&div=div_{selector}')
    if r.status_code==200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        if table is None:
            return pd.DataFrame()
        df = pd.read_html(str(table))[0]
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