import requests 
import os 
from dotenv import load_dotenv
key = load_dotenv('API')
def uuid(ign):
    try:
        data = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{ign}').json()
        return data['id']
    except ValueError:
        return 'Invalid Name\nPlease Try Again'


def getFriends(ign, key):
  friend_list = []
  guild_list = []
  common_list = []
  id = uuid(ign)
  data = requests.get(f'https://api.hypixel.net/friends?uuid={uuid(ign)}&key={key}').json()
  for i in data['records']:
    if i['uuidSender'] != id:
      friend_list.append(i['uuidSender'])
    if i['uuidReceiver'] != id:
      friend_list.append(i['uuidReceiver'])

  data = requests.get(f'https://api.hypixel.net/guild?name=lunar%20guard&key={key}').json()
  for i in data['guild']['members']:
    guild_list.append(i['uuid'])

  for i in friend_list:
    if i in guild_list:
      common_list.append(getIGN(i))
  return common_list


def getIGN(uuid):
  data = requests.get(f'https://api.mojang.com/user/profiles/{uuid}/names').json()
  latest_name = len(data) 
  return data[latest_name -1]['name']
