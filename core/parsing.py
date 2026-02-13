# --------------------------
# PARSING FUNCTIONS
# --------------------------
# parse mvps out of names.
# result is the name minus (mvp) if present and true (for removal) or false (for no need).
def parse_name_and_mvp(name):
    name = name.strip()
    if name.endswith("(mvp)"):
        return name.replace("(mvp)", ""), True
    return name, False

# parse the notable game stats out of the line, mvp is still included for now
# result is dictionary of the game, showing the tanks, dps, and support, and then a result win or loss
# at this point tank could still be something like: luke,mar(mvp).
def parse_game_line(line):
    tank_player, dps_player, support_player, result = line.split("/")
    return { "tank": tank_player, "dps": dps_player, "support": support_player }, result # return 2-tuple with dictionary and result
