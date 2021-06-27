import requests 
tracker_list = ['ThatBananaKing']

def uuid(ign):
    try:
        data = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{ign}').json()
        return data['id']
    except ValueError:
        return 'Invalid Name\nPlease Try Again'

def getOnline(ign, key):
  check = True
  while check:
    data = requests.get(f'https://api.hypixel.net/status?key={key}&uuid={uuid(ign)}')
    online = data['session']['online']
    game_type = data['session']['gameType']
    if online == True or game_type != 'SKYBLOCK':
      check = False
      data = requests.get('http://worldtimeapi.org/api/timezone/america/toronto')
      date_time = data['datetime']
      date_time = date_time[:9]
      print(date_time)

