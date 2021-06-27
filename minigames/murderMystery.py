import requests 
import os 
from dotenv import load_dotenv
api_key = load_dotenv('API')


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

  
def getMurderMysteryStats(ign, key):
  gamemode = 'MurderMystery'
  endpoint = ['wins', 'games', 'coins', 'kills', 'deaths', 'murderer_wins', 'detective_wins', 'quickest_murderer_win_time_seconds', 'quickest_detective_win_time_seconds']
  stats = []
  data = requests.get(f'https://api.hypixel.net/player?key={key}&uuid={uuid(ign)}').json()
  
  for i in endpoint:
    try:
      stats.append(data['player']['stats'][gamemode][i])
    except KeyError:
      stats.append('None')

  wins = stats[0]
  games_played = stats[1]
  coins = stats[2]
  kills = stats[3]
  deaths = stats[4]
  murderer_wins = stats[5]
  detective_wins = stats[6]
  quickest_murderer_win_time_seconds = stats[7]
  quickest_detective_win_time_seconds = stats[8]
  kd_ratio = 'None'
  try:
    kd_ratio = round(kills / deaths, 1)
  except TypeError:
    kd_ratio = 'None'
  try:
    winrate = formatPercentage(round(wins / games_played, 2))
  except TypeError:
    winrate = 'None'
  try:
    losses = games_played - wins
  except TypeError:
    losses = 'None'
  if quickest_murderer_win_time_seconds != 'None':
    quickest_murderer_win_time_seconds = str(quickest_murderer_win_time_seconds) + ' seconds'
  
  if quickest_detective_win_time_seconds != 'None':
    quickest_detective_win_time_seconds = str(quickest_detective_win_time_seconds) + ' seconds'

  return  f'Wins: {wins}\nLosses: {losses}\nGames played: {games_played}\nWin rate: {winrate}\n\nKills:' \
  f' {kills}\nDeaths: {deaths}\nK/D rate: {kd_ratio}\nMurderer wins: {murderer_wins}\nDetective wins: {detective_wins}\n\n' \
  f'Coins: {coins}\nFastest Murder win: {quickest_murderer_win_time_seconds}\nFastest Detective win: ' \
  f'{quickest_detective_win_time_seconds}'
