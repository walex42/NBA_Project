import unidecode, os, sys, unicodedata

"""
    Bounded levenshtein algorithm credited to user amirouche on stackoverflow.
    Implementation borrowed from https://stackoverflow.com/questions/59686989/levenshtein-distance-with-bound-limit
"""
def levenshtein(s1, s2, maximum):  
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        if all((x >= maximum for x in distances_)):
            return -1
        distances = distances_
    return distances[-1]

#This function is used to find all of the possible matches that could exist for a player.
#This is needed due to the fact that there are some players with similar names, some have changed their names, or ther are a jr or second.
def lookup(player, ask_matches = True):
    path = os.path.join(os.path.dirname(__file__), 'br_names.txt')
    normalized = unidecode.unidecode(player)
    matches = []
    
    with open(path) as file:
        Lines = file.readlines()
        for line in Lines:
            #We chose a bound of 5 to use as our match selection criteria to account for mispellings or foriegn characters
            dist = levenshtein(normalized.lower(), line[:-1].lower(), 5)
            if dist >= 0:
                matches += [(line[:-1], dist)]

    #If there is one result return that result
    if len(matches) == 1 or ask_matches == False:
        matches.sort(key=lambda tup: tup[1])
        if ask_matches:
            print("You searched for \"{}\"\n{} result found.\n{}".format(player, len(matches), matches[0][0]))
            print("Results for {}:\n".format(matches[0][0]))
        return matches[0][0]
    #This else statement is supposed to be for the case in which there is more than one match.
    #Have not figured out how to select which match to use. Temporairly using the first one no matter what.
    elif len(matches) > 1:
        print("You searched for \"{}\"\n{} results found.".format(player, len(matches)))
        matches.sort(key=lambda tup: tup[1])
        i = 0
        return matches[0][0]
    #If player is not found return zero results
    elif len(matches) < 1:
        print("You searched for \"{}\"\n{} results found.".format(player, len(matches)))
        return ""
    #Final catch 
    else:
        print("You searched for \"{}\"\n{} result found.\n{}".format(player, len(matches), matches[0][0]))
        print("Results for {}:\n".format(matches[0][0]))
        return matches[0][0]
