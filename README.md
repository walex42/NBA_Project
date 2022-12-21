# NBA Project

This is a project designed to take salary data and player data and combine them into a large database.
This database can be used for several things including trying to predict the future salaries, as well as looking back throughout history to see what contracts were overvalued,
or which contracts should have been higher.
This dataset is set up to gather financial and statistical data about the top-200 paid athletes in the NBA. I chose the top two hundred to focus on because chances are they had enough statistical history to analyze a trend (if there is one), and the fact that these are the biggest sources of cost for teams. If they are overpaying their star players they should be able to find out so that they can spend their money elsewhere.

# Data Sources
I had two main sources in which I used web scraping techniques to get the data. My first was https://hoopshype.com/ this website contained all of the salary data that was needed to assemble the data set. The second was https://www.basketball-reference.com/ this website is the best site to gather any NBA staistic you can think of. 

# Getting Started
There is very little prep needed when using this repository. The big thing is to make sure you have all of the dependecies needed. Once you have confirmed that everything is in order there is really one more step. All you would have to do is run [combinator.py](https://github.com/walex42/NBA_Project/blob/main/combinator.py) to generate a salary and stats linked spreadsheet! Below you can find the breakdown of the files so that if any parameters need to be changed (start and end year, what players to look at, and what stats to gather)

# File Breakdown
### Scraper
The scraper is where you will find the main web scaping fuctions that we used to gather our data. 
The first function scrapeSalary() gathers all players salaries for any given season over a time frame. In order to change the time frame all you would need to do is edit the year range in the loop.
The second function is get_stats(_name, stat_type='PER_GAME', playoffs=False, career=False, ask_matches = True), of which the parameters are fairly straight fowards.  
- Name: player name  
- Stat type: what type of stats you want to gather (per game, per 36, advanced, ect)  
- Playoffs: do you want to include playoff stats  
- Career: do you want to include career stats  
- Ask matches: leave as true as it allows spelling check and matching  
The first hald of get_stats() uses the util.py and lookup.py in order to help generate the URL. The second half takes that URL and goes through the table grabbing all statistics
### Util
The util is the file that houses the functions to generate the suffix of the URL. In this case the suffix is everything in the URL that comes after "www.basketball-reference.com". The suffix is normally made of /player/player last initial/first 5 of last name + first 2 of first name/01/.  
The first function is create_last_name_part_of_suffix which simply is a helper function that gathers the first 5 characters of a players last name.  
The second function combines all of the parts of the suffix and tests to ensure that the URL is valid
### Lookup
The lookup function is also a helper function with the purpose of catching speling mistake or strange characters. THe NBA is an international sport and with that comes many interesting names. Because of this it was only right to incluse a way for the program to understand the name it is looking at. Using a levenshtein algorithm we are able to identify any possible matches if a name is passed that is not recognized. The person who made the levenshtein algothim is cited at the top of the file. The lookup function applies the algorith defined before it and returns the best possible match. That matched name is then used in the get_stats() call. The list of matchable names can be found in [br_names.txt](https://github.com/walex42/NBA_Project/blob/main/br_api/br_names.txt)
### Data Cleaning
The data cleaning file is a simple one aswell. There are two fucntions one for cleaning the salary dataframe and one for cleaning the player stats dataframe.  
The salaryClean() does 4 main things:  
- Renames the season column to "SEASON" to establish a link between the two dataframes  
- Removes the "inflationAdjSalary" since it is almost constantly changing and is hard to apply further back  
- Removes the special characters from the salary column  
- Filters the salary values to be over a million to avoid adding minimum contracts  
The playerSeasonClean() does 3 main things:  
- Changes the "SEASON" column to be a single number  
- Removes unnneccesary columns  
- Makes sure that we only have season data from the same time frame as salary data
### Combinator
The combinator file is the main one that you will use to generate the final dataframe. This file has 4 main actions:  
- The first is to generate and clean the salary dataframe
- The second is to generate a list of players that you want to include in the analysis. As stated in the intro I was focusing on the top-200 paid players of the 2021 NBA season. To do that we used the 2021 salary data and took the top 200 results and converted their player names into a list. We then eliminated the bad inputs. These bad inputs were caused by the player being a rookie, coming from an international team, or sometimes there was an issue with the standard URL naming convention.  
- Third we iterate through every player to start to combine the data into the final data frame. We start by gathering all of the players season stats, then we merge that with the salray data provided for that player. We used the season column to merge on so that the players salary for that year is tied to their stats of that year.  
- Finally once we iterate through every player we take that final dataframe and convert it to a csv to use how ever you desire.

# What can be changed
If you would like to develop a different set that what is pre established you can edit the year time frame in [scraper.py](https://github.com/walex42/NBA_Project/blob/main/scraper.py). You can also edit the type of get_stats() call you make an what players you choose to use in [combinator.py](https://github.com/walex42/NBA_Project/blob/main/combinator.py)

# Exapmles
If you would like to see how this data set could be used in a real world senario please look at [vizualization.ipynb](https://github.com/walex42/NBA_Project/blob/main/vizualization.ipynb). In this notebook I work through a very breif step by step analysis of some of the things found in the data. I show how the data can be visualized and also turned into a model. I used a random forest regression model as the preliminary model. As seen in my analysis this is definitley not the best model to use, and maybe I shall find a better one in the future.