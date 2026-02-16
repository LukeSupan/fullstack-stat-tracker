# DATA MODELS

# make a new player, contains all individual data. bulk of information.
# you can see most of these things on tracking sites. but you can control the data here
# theres also all that other stuff

from collections import defaultdict


def make_player():
    return{
        "roles": defaultdict(lambda: {"wins": 0, "losses": 0}), # makes roles as they are added.
        "wins": 0, "losses": 0, "games": 0,
        "mvps": 0, "mvpwins": 0, "mvplosses": 0,
        "roles": {}
    }




# make a new comp. these dont consider the roles of the team at all
# purely just players, interesting to have. better in small datasets
def make_comp():
    return {
        "wins": 0, "losses": 0, "games": 0
    }

# make a new role comp, considers the roles of the team
# better in large datasets but super interesting. you'll see if you fill it out.
def make_role_comp():
    return {
        "wins": 0, "losses": 0, "games": 0
    }

# defaultdict will automatically intitialize new keys when they appear
