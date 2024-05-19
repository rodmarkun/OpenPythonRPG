from StringProgressBar import progressBar

def show_player_info(player) -> str:
    """
    Shows all the current info (profile) about the player.

    :return: String containing the player's information.
    """

    stat_string = ''.join([f'**{stat}**: {player.status['stats']}\n' for stat in player.status["stats"].keys()])
    player_xp_bar = progressBar.filledBar(int(player.status['xp_to_next_lvl']), int(player.status['hp']), size=10)[0]

    return f'**Player Name**: {player.name.capitalize()}\n' \
            f'**Player Level**: {player.status['lvl']}\n' \
            f'**XP**: {int(player.status['xp'])}/{player.status['xp_to_next_lvl']} {player_xp_bar}\n'

def show_player_stats(player) -> str:
    """
    Returns a string containing the player's stats.

    :return: String containing the player's stats.
    """

    player_hp_bar = progressBar.filledBar(int(player.status['stats']['MAXHP']), int(player.status['stats']['HP']), size=10)[0]
    player_mp_bar = progressBar.filledBar(int(player.status['stats']['MAXMP']), int(player.status['stats']['MP']), size=10)[0]
    return f'**HP**: {player.status['stats']['HP']}/{player.status['stats']['MAXHP']} {player_hp_bar}        \n' \
            f'**MP**: {player.status['stats']['MP']}/{player.status['stats']['MAXMP']} {player_mp_bar}\n\n' \
            + ''.join([f'**{stat}**: {player.status['stats']}\n' for stat in player.status['stats'].keys() if stat not in ['HP', 'MP', 'MAXHP', 'MAXMP']])

def show_inventory(player) -> str:
    """
    Shows player's inventory

    :return: Str containing all item's info
    """

    if len(player.status['inventory']) == 0:
        return "You have no items in your inventory."
    for item in player.status['inventory'].keys():
        inventory_str += f"x{player.status['inventory'][item]} **{item}**\n"
    return inventory_str