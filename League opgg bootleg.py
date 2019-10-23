from datetime import datetime
from pprint import pprint
import json
import requests as r
import os
import time


curent_date = datetime.today().strftime("%Y-%m-%d_%H_%M")
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
    summoner_entries = r.get("https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{}".format(user_data["id"]),headers=headers).json()
except Exception as e:
    print("failed to pull user data: error: {}".format(e))

write_to_file("{}'s_SummonerEntries_{}.json".format(league_name, curent_date), summoner_entries)

# pprint(summoner_entries)

try:
    match_history = r.get("https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/{}".format(user_data["accountId"]),headers=headers).json()
except Exception as e:
    print("failed to pull user data: error: {}".format(e))

write_to_file("{}'s_MatchHistory_{}.json".format(league_name, curent_date), match_history)


game_ids = [x["gameId"] for x in match_history["matches"]]
os.makedirs("MatchHistory", exist_ok=True)
for x in game_ids:
    try:
        match_info = r.get("https://na1.api.riotgames.com/lol/match/v4/matches/{}".format(x),headers=headers).json()
        write_to_file("./MatchHistory/Match{}_MatchInfo_{}.json".format(x, curent_date), match_info)
        time.sleep(2)
    except Exception as e:
        print("failed to pull user data: error: {}".format(e))









# pprint(match_history)
# json.loads("")

# with open(file_name, "a") as f:
#     f.write(str(user_data))
#     f.write(str(summoner_entries[0]))
#     f.write(str(match_history))
