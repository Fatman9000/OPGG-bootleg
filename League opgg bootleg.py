import json
import os
import time
from datetime import datetime
import pprint
import requests as r

while True:
    try:
        with open("api_key.txt") as f:
            api_key = f.read()
        break
    except FileNotFoundError:
        print("No api key file found")
        input("Please create api key file and press enter to continue ")
        continue

print("Press Ctrl + c to exit")
curent_date = datetime.today().strftime("%Y-%m-%d_%H-%M")
league_name = input("Enter your league username ")
headers = {"Content-Type": "application/json",
           "Application-Type": "application/json", "X-Riot-Token": api_key}


def write_to_file(file_name, inputdata):
    """Writes all given input data to a file dumped as json"""
    with open(file_name, "a") as f:
        json.dump(inputdata, f, indent=4)


url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}".format(
    league_name)
try:
    user_data = r.get(url=url, headers=headers).json()
except Exception as e:
    print("failed to pull user data: error: {}".format(e))

write_to_file("{}'s_UserData_{}.json".format(
    league_name, curent_date), user_data)


try:
    summoner_entries = r.get("https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/{}".format(
        user_data["id"]), headers=headers).json()  # end_index, start_index),
except Exception as e:
    print("failed to pull user data: error: {}".format(e))

write_to_file("{}'s_SummonerEntries_{}.json".format(
    league_name, curent_date), summoner_entries)

try:
    match_history = r.get("https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/{}".format(
        user_data["accountId"]), headers=headers).json()
except Exception as e:
    print("failed to pull user data: error: {}".format(e))

write_to_file("{}'s_MatchHistory_{}.json".format(
    league_name, curent_date), match_history)

# List comprehension for getting game ids
game_ids = [x["gameId"] for x in match_history["matches"]]
if input("Would you like to get new matches y/n ") == "y":
    os.makedirs("{}_MatchHistory".format(league_name), exist_ok=True)
    for x in game_ids:
        my_files = os.listdir(path="./{}_MatchHistory".format(league_name))
        if "{}_MatchInfo.json".format(x) in my_files:
            print("Already have match {}".format(x))
            continue
        print("Getting match {}".format(x))
        try:
            match_info = r.get(
                "https://na1.api.riotgames.com/lol/match/v4/matches/{}".format(x), headers=headers).json()
            write_to_file(
                "./{}_MatchHistory/{}_MatchInfo.json".format(league_name, x), match_info)
            participant_id = [x['participantId'] for x in match_info["participantIdentities"]
                              if x['player']['summonerName'].lower() == league_name.lower()]
            write_to_file("./{}_MatchHistory/{}_PlayerPerformance.json".format(
                league_name, x), match_info['participants'][participant_id[0]-1])
            time.sleep(2)
        except Exception as e:
            print("failed to pull user data: error: {}".format(e))
        except KeyboardInterrupt:
            print("User exited")
            break
else:
    for x in game_ids:
        my_files = os.listdir(path="./{}_MatchHistory".format(league_name))
        if "{}_MatchInfo.json".format(x) in my_files:
            print("Already have match {}".format(x))
            continue

# Json parsing below here
try:
    while True:
        selected_id = input("Choose a game id that you want to view ")
        with open("./{}_MatchHistory/{}_PlayerPerformance.json".format(league_name, selected_id)) as j:
            json_file = json.load(j)
            pprint.pprint(json_file["stats"], indent=4)
            # selected_stat = input("Choose a stat that you want to view ")
            # print(selected_stat, json_file["stats"][selected_stat])
except FileNotFoundError:
    print("file not found")
except KeyboardInterrupt:
    print("\nUser exited")
