import requests
from pain import s

def uuid(ign):
    data = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{ign}').json()
    x = data["id"]
    return x


def checkFKDR(ign, key):
    try:
        data = requests.get(f'https://api.hypixel.net/player?key='
                            f'{key}&uuid={uuid(ign)}').json()
        total_final_kills = s(data['player']['stats']['Bedwars']['final_kills_bedwars'])
        total_final_deaths = s(data['player']['stats']['Bedwars']['final_deaths_bedwars'])
        total_fkdr = total_final_kills / total_final_deaths

        solo_final_kills = s(data['player']['stats']['Bedwars']['eight_one_final_kills_bedwars'])
        solo_final_deaths = s(data['player']['stats']['Bedwars']['eight_one_final_deaths_bedwars'])
        solo_fkdr = solo_final_kills / solo_final_deaths

        doubles_final_kills = s(data['player']['stats']['Bedwars']['eight_two_final_kills_bedwars'])
        doubles_final_deaths = s(data['player']['stats']['Bedwars']['eight_two_final_deaths_bedwars'])
        doubles_fkdr = doubles_final_kills / doubles_final_deaths

        triples_final_kills = s(data['player']['stats']['Bedwars']['four_three_final_kills_bedwars'])
        triples_final_deaths = s(data['player']['stats']['Bedwars']['four_three_final_deaths_bedwars'])
        triples_fkdr = triples_final_kills / triples_final_deaths

        fours_final_kills = s(data['player']['stats']['Bedwars']['four_four_final_kills_bedwars'])
        fours_final_deaths = s(data['player']['stats']['Bedwars']['four_four_final_deaths_bedwars'])
        fours_fkdr = fours_final_kills / fours_final_deaths

        return f'Overall: {round(total_fkdr, 2)} \nSolo: {round(solo_fkdr, 2)} \nDoubles: {round(doubles_fkdr, 2)} ' \
               f'\n3s: {round(triples_fkdr, 2)} \n4s: {round(fours_fkdr, 2)}\n'
    except KeyError:
        return "Player haven't played bw yet????"