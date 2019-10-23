from datetime import datetime
import json
import requests as r
import os
import time


curent_date = datetime.today().strftime("%Y-%m-%d_%H-%M")
league_name = input("Enter your league username ")

def write_to_file(file_name, inputdata):
    """Writes all given input data to a file dumped as json"""
    with open(file_name, "a") as f:
        # f.write(str(inputdata).replace("'", '"'))
        json.dump(inputdata, f, indent=4)


headers = {"Content-Type": "application/json","Application-Type": "application/json", "X-Riot-Token": "RGAPI-1506528b-8ec1-455f-8178-d73f719f6f32"}#
url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}".format(league_name)
try:
    user_data = r.get(url=url, headers=headers).json()
except Exception as e:
    print("failed to pull user data: error: {}".format(e))

write_to_file("{}'s_UserData_{}.json".format(league_name, curent_date), user_data)




try:
    summoner_entries = r.get("https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{}?endIndex=50&beginIndex=0".format(user_data["id"]),headers=headers).json()
except Exception as e:
    print("failed to pull user data: error: {}".format(e))

write_to_file("{}'s_SummonerEntries_{}.json".format(league_name, curent_date), summoner_entries)

try:
    match_history = r.get("https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/{}".format(user_data["accountId"]),headers=headers).json()
except Exception as e:
    print("failed to pull user data: error: {}".format(e))

write_to_file("{}'s_MatchHistory_{}.json".format(league_name, curent_date), match_history)

# List comprehension for getting game ids
game_ids = [x["gameId"] for x in match_history["matches"]]
os.makedirs("{} Match History".format(league_name), exist_ok=True)
for x in game_ids:
    try:
        match_info = r.get("https://na1.api.riotgames.com/lol/match/v4/matches/{}".format(x),headers=headers).json()
        write_to_file("./{} Match History/Match{}_MatchInfo_{}.json".format(league_name, x, curent_date), match_info)
        time.sleep(2)
        participant_id = [x['participantId'] for x in match_info["participantIdentities"] if x['player']['summonerName'].lower() == league_name.lower() ]
        write_to_file("./{} Match History/Match{}_PlayerPerformance_{}.json".format(league_name, x, curent_date), match_info['participants'][participant_id[0]-1])
        if match_info['participants'][participant_id[0]-1]['stats']['pentaKills'] > 0:
            print("Penta Kill found in file Match{}_PlayerPerformance_{}.json".format(x, curent_date))
        else:
            print("No penta kill found")
    except Exception as e:
        print("failed to pull user data: error: {}".format(e))



# os.makedirs("MatchTimelines", exist_ok=True)
# for x in game_ids:
#     try:
#         match_timeline = r.get("https://na1.api.riotgames.com/lol/match/v4/timelines/by-match/{}".format(x),headers=headers).json()
#         write_to_file("./MatchTimelines/Match{}_MatchTimeline_{}.json".format(x, curent_date), match_timeline)
#         time.sleep(2)
#     except Exception as e:
#         print("failed to pull user data: error: {}".format(e))



# directory = "G:\Code\OPGG-bootleg\MatchHistory"
# for matches in os.listdir(directory):
#     with open(matches) as f:
#         if match_history["participants"][]> 0:
#             print("dab")
#         else:
#             print("sad")
