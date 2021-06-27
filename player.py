import requests
import datetime
from pain import s

def uuid(ign):
    try:
        data = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{ign}').json()
        return data['id']
    except ValueError:
        return 'Invalid Name\nPlease Try Again'


def checkStats(ign, key):
    if ign.lower() == 'thatbananaking':
        return ThatBananaKing()
    data = requests.get(f'https://api.hypixel.net/player?key={key}&uuid={uuid(ign)}').json()
    unix_time_first_joined = s(data['player']['firstLogin'])
    normal_time_first_joined = datetime.datetime.fromtimestamp(unix_time_first_joined/1000.0)
    unix_time_last_joined = s(data['player']['lastLogin'])
    normal_time_last_joined = datetime.datetime.fromtimestamp(unix_time_last_joined/1000.0)

    achievement_points =  s(data['player']['achievementPoints'])
    karma = s(data['player']['karma'])
    rank = getRank(data)
    current_level = getLevel(data['player']['networkExp'])
    current_guild = getGuild(ign, key)
    friend = getFriend(ign, key)
    status = getStatus(ign, key)


    return f'Rank: {rank} \nGuild: {current_guild} \nStatus: {status} \nFriends: {friend} \nLevel: {current_level} \n\nAchievement Point: {achievement_points} \nKarma: {karma} '\
    f'\nFirst Join: {normal_time_first_joined} \nLast Joined: {normal_time_last_joined}'


def getRank(data):
    try:
        if data['player']['monthlyPackageRank'] == 'NONE':
            rank =  data['player']['newPackageRank']
    
        else: 
            rank = data['player']['monthlyPackageRank']
    except KeyError:
        return 'non'
    
    if rank == 'SUPERSTAR':
        return 'MVP ++'
    if rank == 'MVP_PLUS':
        return 'MVP +'
    if rank == 'VIP_PLUS':
        return 'VIP +'
    return rank


def getLevel(exp):
    next_level = 10_000
    level = 1
    for _ in range(1000):
        if exp < next_level:
            return level
        else:
            exp -= next_level
            next_level += 2_500
            level += 1


def getGuild(ign, key):
    data = requests.get(f'https://api.hypixel.net/guild?player={uuid(ign)}&key={key}').json()
    try:
        return data['guild']['name']
    except KeyError:
        return f'{ign} is not currently in a guild.'


def getFriend(ign, key):
    data = requests.get(f'https://api.hypixel.net/friends?key={key}&uuid={uuid(ign)}').json()
    return len(data['records'])


def getStatus(ign, key):
    data = requests.get(f'https://api.hypixel.net/status?key={key}&uuid={uuid(ign)}').json()
    if data['session']['online'] == 'true':
      return 'Online'
    else:
      return 'Offline'
        

def ThatBananaKing():
    return 'rank: Banana Guild: Lunar Guard Friends: 45 Level: 420 Achievement Points: 6969 Status: ¯\_(ツ)_/¯'

