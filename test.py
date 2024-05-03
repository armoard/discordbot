
import requests
from dotenv import load_dotenv
import os 

load_dotenv()
API = os.getenv('RIOT_API')

def get_puuid(gameName, tagLine):
    api_url1 = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}"

    api_url1 = api_url1 + '?api_key=' + API

    response = requests.get(api_url1)
    data = response.json()

    encryptedPUUID = data['puuid']
    return encryptedPUUID
 

def get_id(encryptedPUUID):
    api_url1 = f"https://la2.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{encryptedPUUID}"

    api_url1 = api_url1 + '?api_key=' + API
    

    response = requests.get(api_url1)
    data = response.json()
    summoner_id = data['id']

    return summoner_id

def get_lp(encryptedSummonerId):
    api_url1 = f"https://la2.api.riotgames.com/lol/league/v4/entries/by-summoner/{encryptedSummonerId}"
    
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
    return difference_lp

def main():
    inputs = input("nicks: ")
    
    user_inputs = inputs.split(',')
    
    user1_info = user_inputs[0].strip().split('#')
    user2_info = user_inputs[1].strip().split('#')
    ##.strip sacas los espacios
    ## dividis por tags
    

    name1 = user1_info[0]
    tag1 = user1_info[1]
    name2 = user2_info[0]
    tag2 = user2_info[1]

  
    difference_lp = compare_lp(name1, tag1, name2, tag2)
    
    print("DIFERENCIA:", abs(difference_lp))

main()
    