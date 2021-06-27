import requests
import math
"""
pip install requesats
This will only return the stats of the following gamemodes:
Solo: (1v1)
Doubles: (2v2)
Mega: (50v50)
Ranked: (1v1)
total_games_played = wins + losses 
EXP leveling: https://hypixel.fandom.com/wiki/SkyWars#:~:text=In%20SkyWars%2C%20players%20spawn%20on,their%20own%20loot%20when%20killed.
tl.dr from lvl 1 - 12: 15k required and after lvl 12: 10k per level
"""


def round_decimals_down(number:float, decimals:int=0):
    """
    Returns a value rounded down to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return math.floor(number)

    factor = 10 ** decimals
    return math.floor(number * factor) / factor


def uuid(ign):
    try:
        data = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{ign}').json()
        return data['id']
    except ValueError:
        # print('Decoding JSON has failed')
        print('Invalid username \nPlease try again')
        exit()


def formatPercentage(x):
    return "{:.0%}".format(x)


def calculateLevel(exp):
    level_requirement_first12 = [0, 20, 70, 150, 250, 500, 1000, 2000, 3500, 6000, 10000, 15000]
    total_xp_first12 = 15_000
    if exp > total_xp_first12:
        lvl = round_decimals_down((exp - total_xp_first12) / 10_000)
        lvl += 12
        return lvl

    for i in range(len(level_requirement_first12)):
        if exp <= level_requirement_first12[i]:
            return i


def getSkywarsStats(ign, key):
    data = requests.get(f'https://api.hypixel.net/player?key={key}&uuid={uuid(ign)}').json()
    try:
        wins = data['player']['stats']['SkyWars']['wins']
        losses = data['player']['stats']['SkyWars']['losses']
    except KeyError:
        print(f'{ign} has no skywars stats')
        exit()
    win_rate = formatPercentage(round(wins / (wins + losses), 2))

    kills = data['player']['stats']['SkyWars']['kills']
    deaths = data['player']['stats']['SkyWars']['deaths']
    assists =  data['player']['stats']['SkyWars']['assists']
    kill_death_ratio = round(kills / deaths, 2)

    experience = data['player']['stats']['SkyWars']['skywars_experience']
    current_winstreak = data['player']['stats']['SkyWars']['win_streak']
    games_played = wins + losses
    level = calculateLevel(experience)
    

    return f"Levels: {level}\nWins: {wins}\nLosses: {losses}\nWin Rate: {win_rate}" \
           f"\n\nKills: {kills}\nDeaths: {deaths}\nAssists: {assists}\nK/D Ratio: {kill_death_ratio}\nGames Played: " \
           f"{games_played}\nCurrent Winstreak: {current_winstreak}" 
