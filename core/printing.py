from core.utils import winrate, sized_comps_sort_key, role_comp_team_size
from colorama import init, Fore, Back, Style

init(autoreset=True)  # auto-reset after each print

# --------------------------
# PRINTING
# --------------------------
# print individual players stats. if deadlock print lane instead of tank type
def print_player_stats(player_stats, role_labels):
    for player, stats in sorted(player_stats.items()):
        print(f"\n===== {player} =====") # 5 ='s on left plus a space centers it above the following
        print(f"  {role_labels[0]}:    {stats['role1wins']}W / {stats['role1losses']}L")
        print(f"  {role_labels[1]}:     {stats['role2wins']}W / {stats['role2losses']}L")
        print(f"  {role_labels[2]}: {stats['role3wins']}W / {stats['role3losses']}L")
        print(f"  Overall: {stats['wins']}W / {stats['losses']}L")
        print(f"  Winrate: {winrate(stats['wins'],stats['games']):.1f}%") # colon here is a format specifier. just set to 1 decimal point

        # im making it so mvp only prints if they have mvp stats for those who dont want to measure it (or if its irrelevant)
        if stats['mvps'] > 0:
            print(f"    MVPs: {stats['mvps']}")
            print(f"    MVP in: {winrate(stats['mvps'],stats['games']):.1f}% of games")
            print(f"    MVP vs SVP: {stats['mvpwins']}W / {stats['mvplosses']}L")

    return


def print_non_role_comps(comp_stats, min_games=1):
    # print non role comps (2 or more) to avoid some clutter, 1 is reasonable if you want to change this. i just prefer less clutter and who cares about 1 game.
    # this is one of the most interesting parts. you can see who is weak. and strong i suppose
    # TODO make this print only if it should (same with ROLE BASED COMPS. this should always print though, just for if someone changes the value down there so it doesnt)

    # if any of these statements are false, do not print the header. with the default value it always, but if its changed it may not.
    has_data = any(
        stats["games"] >= min_games
        for stats in comp_stats.values()
    )

    if not has_data:
        return


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
            if len(comp) == size and stats["games"] >= min_games # get only comps of this size, filter
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

    return


# TODO, make it work for deadlock, it prints the roles right now, no good, oh might be good, no not good
def print_role_comps(role_comp_stats, role_labels, min_games=3):
    # print role comps (3 or more) would be really cluttered with less
    # i also like this one. you can see who is weak on what. gotta play more though
    # process is super similar to above, but role_comps have a function to get the size instead.

    # if any of these statements are false, do not print the header
    has_data = any(
        stats["games"] >= min_games
        for stats in role_comp_stats.values()
    )

    if not has_data:
        return

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
            if role_comp_team_size(role_comp) == size and stats["games"] >= min_games # need at least 3 games. theres not much of a pattern before that. the clutter is crazy. you can change it if youd like to play around
        ]

        # if its empty, we dont print the title card and move on
        if not sized_role_comps:
            continue

        # sort by winrate (highest first), then by number of games (highest first as tiebreaker)
        sized_role_comps.sort(key=sized_comps_sort_key, reverse=True)


        
        print(f"\n----- {size}-PLAYER COMPS -----")
        header = " / ".join([
            f"{role_labels[0]}",
            f"{role_labels[1]}",
            f"{role_labels[2]}"
        ])

        print(f"{Style.BRIGHT}{header:30}{Style.RESET_ALL}")

        # we have the comps for this size, print them nicely
        for role_comp, stats in sized_role_comps:

            print_list = []
            # split by /'s for roles, print title for each
            slots = role_comp.split("/")
            for label, slot in zip(role_labels, slots):
                if slot:
                    print_list.append(f"{slot}")
                else:
                    print_list.append(f"none")

            role_comp_print = " / ".join(print_list)
            print(f"{role_comp_print:30} {winrate(stats['wins'], stats['games']):5.1f}% ({stats['games']} games)")

    return
            