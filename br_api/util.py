from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import unicodedata, unidecode


#Helper function to determine what the last name part of the suffix should be
#Usefull for players with multiple part or abbreviated names

def create_last_name_part_of_suffix(potential_last_names):
    last_names = ''.join(potential_last_names)
    #If the last name is 5 letters or less just return that given that the last name section is 5 characters
    if len(last_names) <= 5:
        return last_names[:].lower()
    #If its longer select the first 5
    else:
        return last_names[:5].lower()

  
#Basketball reference standardizes URL codes, it is much more efficient to create them and then check that the URLs direct you to the correct page
#This implementation dropped player lookup fail count from 306 to 35.

def get_player_suffix(name):
    normalized_name = unidecode.unidecode(unicodedata.normalize('NFD', name).encode('ascii', 'ignore').decode("utf-8"))
    #These if statements were an attempt to try and rectify the bad inputs that were showing up in our combinator.py
    if normalized_name == 'Metta World Peace' :
        suffix = '/players/a/artesro01.html'
    #Some still would not scrape correctly    
    #if normalized_name == "Clint Capela" :
        #suffix = '/players/c/capelca01.html'
    else:
        #Creating the suffix of the URL
        split_normalized_name = normalized_name.split(' ')
        #Case for only a first or a last name
        if len(split_normalized_name) < 2:
            return None
        #First letter of last name
        initial = normalized_name.split(' ')[1][0].lower()
        all_names = name.split(' ')
        #First two letters of last name
        first_name_part = unidecode.unidecode(all_names[0][:2].lower())
        first_name = all_names[0]
        other_names = all_names[1:]
        other_names_search = other_names
        last_name_part = create_last_name_part_of_suffix(other_names)
        suffix = '/players/'+initial+'/'+last_name_part+first_name_part+'01.html'
    player_r = get(f'https://www.basketball-reference.com{suffix}')
    #If the URL doesnt lead to a valid page continue on to reiterate the suffix and try again
    while player_r.status_code == 404:
        continue
    #This is when the URL does lead to a valid page
    while player_r.status_code==200:
        player_soup = BeautifulSoup(player_r.content, 'html.parser')
        h1 = player_soup.find('h1')
        if h1:
            page_name = h1.find('span').text
            #Checking to see if the URL leads you to the correct page. If not incriment the suffix formula and check again
            if ((unidecode.unidecode(page_name)).lower() == normalized_name.lower()):
                return suffix
            else:
                page_names = unidecode.unidecode(page_name).lower().split(' ')
                page_first_name = page_names[0]
                if first_name.lower() == page_first_name.lower():
                    return suffix
                # if players have same first two letters of last name then just
                # increment suffix
                elif first_name.lower()[:2] == page_first_name.lower()[:2]:
                    player_number = int(''.join(c for c in suffix if c.isdigit())) + 1
                    if player_number < 10:
                        player_number = f"0{str(player_number)}"
                    suffix = f"/players/{initial}/{last_name_part}{first_name_part}{player_number}.html"
                else:
                    if not other_names_search:
                        return None
                    other_names_search.pop(0)
                    last_name_part = create_last_name_part_of_suffix(other_names_search)
                    initial = last_name_part[0].lower()
                    suffix = '/players/'+initial+'/'+last_name_part+first_name_part+'01.html'

                player_r = get(f'https://www.basketball-reference.com{suffix}')

    return None
