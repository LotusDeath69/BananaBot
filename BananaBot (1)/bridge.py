import requests
from pain import s
"""
In Beta, DM Tree#7109 if you find any errors
Bridge_Duel =  solo mode (1v1)
Bridge_doubles = double mode (2v2)
Bridge_four = 4s mode (4v4)
There are also modes for 3v3v3v3 and 2v2v2v2 but they WILL NOT be included
Final stats are calculated by adding all of these modes up
Total_games_played = wins + losses + ties
"""


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


def CalculateStat(mode, data, stat):
    total = 0
    for i in mode:
        try:
            total += data['player']['stats']['Duels'][f'bridge_{i}_{stat}']
        except KeyError:
            continue

    if total == 0:
        return f'Player has no {stat}'
    return total 


def checkBridgeStats(ign, key):
    data = requests.get(f'https://api.hypixel.net/player?key={key}&uuid={uuid(ign)}').json()
    try:
        deaths = data['player']['stats']['Duels']['bridge_deaths']
        kills = data['player']['stats']['Duels']['bridge_kills']
    except KeyError:
        return f'{ign} has no bridge stats'
    
    modes = ['duel', 'doubles', 'four']
    total_wins = CalculateStat(modes, data, 'wins')
    total_losses = CalculateStat(modes, data, 'losses')
    total_games_played = CalculateStat(modes, data, 'rounds_played')
    total_goals = CalculateStat(modes, data, 'goals')
    KD_ratio = s(round(kills/deaths, 2))
    winrate = formatPercentage(round(total_wins / (total_losses + total_wins), 2))
    ties = total_games_played - (total_wins + total_losses)

    return f'Wins: {total_wins} \nLosses: {total_losses} \nTies: {ties} \nKills: {kills} \nDeaths: {deaths} \n\nKD Ratio: {KD_ratio} \nWin rate:'\
    f' {winrate} \nGames Played: {total_games_played} \nGoals: {total_goals}'
