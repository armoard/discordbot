from random import randint
import requests
from dotenv import load_dotenv
import os 
from keys import get_api_key
load_dotenv()
API = get_api_key()

def get_response(user_input: str):
    if validate_lp_compare(user_input):
        parsed = parse_lp_compare(user_input)
        print(parsed)
        print(compare_lp(parsed[0], parsed[1], parsed[2], parsed[3]))
        return compare_lp(parsed[0], parsed[1], parsed[2], parsed[3])
        

    # if validate_other_command(user_input):
        #blablala del otro comando, como arriba
    
    else:
        return generate_response(user_input)
    



  
        

def get_puuid(gameName, tagLine):
    api_url1 = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}"
    print(f"account by riot id url = {api_url1}")

    api_url1 = api_url1 + '?api_key=' + API

    response = requests.get(api_url1)
    data = response.json()

    encryptedPUUID = data['puuid']
    return encryptedPUUID
    

def get_id(encryptedPUUID):
    api_url1 = f"https://la2.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{encryptedPUUID}"
    print(f"encrypted PUUID url = {api_url1}")

    api_url1 = api_url1 + '?api_key=' + API

    response = requests.get(api_url1)
    data = response.json()
    summoner_id = data['id']

    return summoner_id

def get_lp(encryptedSummonerId):
    api_url1 = f"https://la2.api.riotgames.com/lol/league/v4/entries/by-summoner/{encryptedSummonerId}"
    print(f"entries by summoner url = {api_url1}")
    api_url1 = api_url1 + '?api_key=' + API
    
    response = requests.get(api_url1)
    data = response.json()
    
    lp1 = data[0]['leaguePoints']
    return lp1
       

def compare_lp(name1, tag1, name2, tag2):
    summoner_puuid1 = get_puuid(name1, tag1)
    summoner_puuid2 = get_puuid(name2, tag2)

    summoner_id1 = get_id(summoner_puuid1)
    summoner_id2 = get_id(summoner_puuid2)

    summoner_lp1 = get_lp(summoner_id1)
    summoner_lp2 = get_lp(summoner_id2)

    difference_lp = (summoner_lp1 - summoner_lp2)
    return abs(difference_lp)

def validate_lp_compare(a: str) -> bool:
    lowered: str = a.lower()
    if a[0] != '!':
        return False
    if ("#") not in a:
        return False
    if len(a) <= 21:
        return False
    # mas validaciones que salgan en False
    return True

def parse_lp_compare(input: list):
    replaced = input.replace("!compare ", "")
    first, second = replaced.split(" ")
    user1_info = first.strip().split('#')
    user2_info = second.strip().split('#')
    ##.strip sacas los espacios
    ## dividis por tags
    
    name1 = user1_info[0]
    tag1 = user1_info[1]
    name2 = user2_info[0]
    tag2 = user2_info[1]

    return [name1, tag1, name2, tag2]

def generate_response(a:str):
    
    if a == '': 
        return 'alo'
    elif 'hello' in a:
        return 'hola'
    elif 'roll dice' in a:
        return f'You rolled:{randint(1,6)}'
    elif 'peak' in a:
        return '765lp'
    elif 'liz' in a:
        return 'mmh'
    
    else:
        return "no te entendi amiguito"
    




