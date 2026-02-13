# the README explains how to use this in depth. look there first

# it is very entertaining (and useful) to tweak a lot of this stuff to see different results.
# if you read through this you should be able to make some changes. i tried to make it clear.

from collections import defaultdict
from core.models import make_player, make_comp, make_role_comp
from core.parsing import parse_name_and_mvp, parse_game_line
from games.hero_shooter import get_role_comp_key, extract_players, winrate, sized_comps_sort_key, role_comp_team_size



# change file name below. a clear explanation and examples are in README, mvp is entirely optional
#            |
#            |
#            V
# --------------------------
# INPUT FILE
# --------------------------
with open("games.txt") as f: # (change the name of "games.txt" here to your text document)
    games = [line.strip() for line in f if line.strip()]


# create dicts to save multiple players/comps
# defaultdict calls the given function automatically
# whenever a new key is accessed.
# example:
#   player_stats["luke"]  -> make_player() is called automatically
player_stats = defaultdict(make_player)
comp_stats = defaultdict(make_comp)
role_comp_stats = defaultdict(make_role_comp)


# --------------------------
# AGGREGATION (main)
# --------------------------
# total process is:
# parse_game_line -> parse_name_and_mvp for each roleon that line -> adjust winrates for players 
# -> extract and adjust both comp types -> print (TODO based on gametype)

# for each game, add relevant stats
for line in games:
    team, result = parse_game_line(line)

    # add stats for each player from the current game
    for role, names in team.items():
        if names == "none":
            continue

        # if multiple names, split with , and run for each
        for raw in names.split(","):
            name, is_mvp = parse_name_and_mvp(raw) # remove mvp from name if present, save mvp status

            player_stats[name]["games"] += 1 # yeah man they played a game

            if is_mvp:
                player_stats[name]["mvps"] += 1

            # im considering adding mvp tracking for each role. might be cluttered. but also i really enjoy how specific the data is. future thing anyway. if youd like to add it go ahead
            if result == "win":
                player_stats[name][f"{role}wins"] += 1 # add 1 to role winrate
                player_stats[name]["wins"] += 1
                player_stats[name]["mvpwins"] += is_mvp # add 1 if true, 0 if false to mvpwins
            else:
                player_stats[name][f"{role}losses"] += 1 # add 1 to role winrate
                player_stats[name]["losses"] += 1
                player_stats[name]["mvplosses"] += is_mvp # add 1 if true, 0 if false to mvpwins


    # for this game, adjust the comp stats
    comp_key = tuple(sorted(extract_players(team))) # sort the set, make it a sorted tuple so that we can use it as a key with no duplicates
    comp_stats[comp_key]["games"] += 1

    if result == "win":
        comp_stats[comp_key]["wins"] += 1
    else:
        comp_stats[comp_key]["losses"] += 1


    # for this game, adjust the role comp stats
    role_comp_key = get_role_comp_key(team) # more complicated. view the function, but it gets the key
    role_comp_stats[role_comp_key]["games"] += 1

    if result == "win":
        role_comp_stats[role_comp_key]["wins"] += 1
    else:
        role_comp_stats[role_comp_key]["losses"] += 1



# --------------------------
# PRINTING
# --------------------------
# print individual players stats. if deadlock print lane instead of tank type
for player, stats in sorted(player_stats.items()):
    print(f"\n===== {player} =====") # 5 ='s on left plus a space centers it above the following
    print(f"  Tank:    {stats['tankwins']}W / {stats['tanklosses']}L")
    print(f"  DPS:     {stats['dpswins']}W / {stats['dpslosses']}L")
    print(f"  Support: {stats['supportwins']}W / {stats['supportlosses']}L")
    print(f"  Overall: {stats['wins']}W / {stats['losses']}L")
    print(f"  Winrate: {winrate(stats['wins'],stats['games']):.1f}%") # colon here is a format specifier. just set to 1 decimal point

    # im making it so mvp only prints if they have mvp stats for those who dont want to measure it (or if its irrelevant)
    if stats['mvps'] > 0:
        print(f"    MVPs: {stats['mvps']}")
        print(f"    MVP in: {winrate(stats['mvps'],stats['games']):.1f}% of games")
        print(f"    MVP vs SVP: {stats['mvpwins']}W / {stats['mvplosses']}L")


# print non role comps (2 or more) to avoid some clutter, 1 is reasonable if you want to change this. i just prefer less clutter and who cares about 1 game.
# this is one of the most interesting parts. you can see who is weak. and strong i suppose
# TODO make this print only if it should (same with ROLE BASED COMPS. this should always print though, just for if someone changes the value down there so it doesnt)
print("\n\n===== NON-ROLE-BASED COMPS =====")

# print in order of smallest to largest team size first
team_sizes = sorted({len(comp) for comp in comp_stats})

for size in team_sizes:

    # use list comprehension to make a new list
    # gather comps of this size. you can limit the number of games needed here with stats["games"] > x
    # result is a list of tuples: (("aiden", "luke"), {"wins": 1.....}), and so on
    sized_comps = [
        (comp, stats) # we are adding comps and their stats to the list, output
        for comp, stats in comp_stats.items() # this gets all comps, iteration
        if len(comp) == size and stats["games"] > 0 # get only comps of this size, filter
    ]

    # if its empty, we dont print the title card and move on
    if not sized_comps:
        continue

    print(f"\n----- {size}-PLAYER COMPS -----")

    # sort by winrate, the key is winrate first, games played as backup
    sized_comps.sort(key=sized_comps_sort_key, reverse=True)
    
    # print the comps in order
    for comp, stats in sized_comps:
        names = ", ".join(comp) # combine names for the comp
        print(f"{names:30} {winrate(stats["wins"], stats["games"]):5.1f}% ({stats['games']} games)") # pad to reach 30 spaces, 5 spaces to have it line up nice


# print role comps (3 or more) would be really cluttered with less
# i also like this one. you can see who is weak on what. gotta play more though
# proccess is super similar to above, but role_comps have a function to get the size instead.
print("\n===== ROLE-BASED COMPS =====")

# print in order of smallest to largest team size first
team_sizes = sorted({role_comp_team_size(role_comp) for role_comp in role_comp_stats})

# print all games for each size
for size in team_sizes:
    # use list comprehension to make a new list
    # gather comps of this size. you can limit the number of games needed here with stats["games"] > x
    # result is a list of tuples: (("aiden", "luke"), {"wins": 1.....}), and so on
    sized_role_comps = [
        (role_comp, stats) # we are adding comps and their stats to the list, output
        for role_comp, stats in role_comp_stats.items() # this gets all comps, iteration
        if role_comp_team_size(role_comp) == size and stats["games"] > 2 # need at least 3 games. theres not much of a pattern before that. the clutter is crazy. you can change it if youd like to play around
    ]

    # if its empty, we dont print the title card and move on
    if not sized_role_comps:
        continue
    
    print(f"\n----- {size}-PLAYER COMPS -----")

    # we have the comps for this size, print them nicely
    sized_role_comps.sort(key=sized_comps_sort_key, reverse=True)
    for role_comp, stats in sized_role_comps:
        print(f"{role_comp:50} {winrate(stats['wins'], stats['games']):5.1f}% ({stats['games']} games)")
        