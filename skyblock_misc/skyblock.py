import requests


def uuid(ign):
    """Get the UUID of the player using Mojang's api"""
    data = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{ign}').json()
    x = data["id"]
    return x


def getSkillAV(ign, key):
    """Get the Skill Average of the player"""
    data = requests.get(f'https://hypixel-api.senither.com/v1/profiles/{uuid(ign)}/weight/?key={key}').json()
    skill_avg = data['data']['skills']['average_skills']
    return f"Skill Average: {round(skill_avg, 2)}"


def getSlayer(ign, key):
    """Get the Slayer lvl of the player"""
    data = requests.get(f'https://hypixel-api.senither.com/v1/profiles/{uuid(ign)}/weight/?key={key}').json()
    rev_lvl = data['data']['slayers']['bosses']['revenant']['level']
    tara_lvl = data['data']['slayers']['bosses']['tarantula']['level']
    sven_lvl = data['data']['slayers']['bosses']['sven']['level']
    return f'Revenant: {round(rev_lvl)}\nTarantula: {round(tara_lvl)}\nSven: {round(sven_lvl)}'


def getDungeonStats(ign, key):
    """Get the Dungeon Stats of the player"""
    data = requests.get(f'https://hypixel-api.senither.com/v1/profiles/{uuid(ign)}/weight/?key={key}').json()
    secrets_found = data['data']['dungeons']['secrets_found']
    catacomb_lvl = round(data['data']['dungeons']['types']['catacombs']['level'], 2)
    times_completed_f7 = data['data']['dungeons']['types']['catacombs']['tier_completions']['tier_7']
    if times_completed_f7 == 0:
        times_completed_f7 = "Haven't beaten f7 yet"
    fastest_time = data['data']['dungeons']['types']['catacombs']['fastest_time']['tier_7']['time']
    return f'Catacombs Lvl: {catacomb_lvl}\nSecrets Found: {secrets_found}\nf7 completion: {times_completed_f7} times' \
           f'\nFastest Time(f7): {fastest_time}'


def getSkillLvl(ign, key):
    """Get the skill lvl of the player"""
    data = requests.get(f'https://hypixel-api.senither.com/v1/profiles/{uuid(ign)}/weight/?key={key}').json()
    skill_types = ['mining', 'foraging', 'enchanting', 'farming', 'combat', 'fishing', 'alchemy', 'taming']
    skills_lvl = []
    for i in skill_types:
        skills_lvl.append(data['data']['skills'][i]['level'])
    for i in range(len(skills_lvl)):
        skills_lvl[i] = round(skills_lvl[i], 1)

    '#Note: there are 2 ways to return these values, you pick which one you prefer and uncomment them'
    '#First:'
    # for i in range(8):
    #     if i == 8:
    #         break
    #     print(f'{skill_types[i]}: {skills_lvl[i]}')

    '#Second:'
    return f'Mining: {skills_lvl[0]}\nForaging: {skills_lvl[1]}\nEnchanting: {skills_lvl[2]}\nFarming: ' \
           f'{skills_lvl[3]}\nCombat: {skills_lvl[4]}\nFishing: {skills_lvl[5]}\nAlchemy: {skills_lvl[6]}' \
           f'\nTaming: {skills_lvl[7]}'


def getBalance(ign, key):
    """Get the player's balance"""
    """Currently in Beta Mode"""
    data = requests.get(f'https://hypixel-api.senither.com/v1/profiles/{uuid(ign)}/weight/?key={key}').json()
    purse = round(data['data']['coins']['purse'])
    bank = data['data']['coins']['bank']
    
    '#Only displayed purse\'value if bank\'api is disabled'
    try:
        round(bank)
    except TypeError:
        return f'Total balance: {purse}'
    total = purse + bank
    return f'Total balance: {total} coins'
