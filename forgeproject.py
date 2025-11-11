import requests
import time
import statsapi

GEMINI_API_KEY = "AIzaSyAbjlLIYsFcByuigBqfajUeOPf4P8CEmsk"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def get_player_id_by_name(name):
    players = statsapi.lookup_player(name)
    if len(players) == 0:
        print("Player not found. Please try again.")
        time.sleep(1)
        return None
    elif len(players) == 1:
        return players[0]['id']
    else:
        print("Multiple players found. Please be more specific")
        time.sleep(1)
        return None

def get_player_stats(player_id):
    stats_text = statsapi.player_stats(player_id, group='hitting', type='season')
    if stats_text:
        # Parse the stats text to extract values
        stats_dict = {}
        lines = stats_text.split('\n')
        
        for line in lines:
            if ': ' in line:
                key, value = line.split(': ', 1)
                key = key.strip()
                value = value.strip()
                stats_dict[key] = value
        
        # Display only the stats you want
        print("\nPlayer's Current Stats:")
        desired_stats = ['age', 'gamesPlayed', 'avg', 'homeRuns', 'strikeOuts', 'rbi', 'ops', 'obp', 'slg']
        
        filtered_stats = {}
        for stat in desired_stats:
            if stat in stats_dict:
                print(f"{stat}: {stats_dict[stat]}")
                filtered_stats[stat] = stats_dict[stat]
        
        return filtered_stats
    else:
        print("No stats found for this player.")
        return None

def get_pitcher_stats(player_id):
    stats_text = statsapi.player_stats(player_id, group='pitching', type='season')
    if stats_text:
        # Parse the stats text to extract values
        stats_dict = {}
        lines = stats_text.split('\n')
        
        for line in lines:
            if ': ' in line:
                key, value = line.split(': ', 1)
                key = key.strip()
                value = value.strip()
                stats_dict[key] = value
        
        # Display pitcher stats
        print("\nPitcher's Current Stats:")
        desired_stats = ['age', 'gamesPlayed', 'wins', 'losses', 'era', 'strikeOuts', 'walks', 'saves', 'inningsPitched', 'whip']
        
        filtered_stats = {}
        for stat in desired_stats:
            if stat in stats_dict:
                print(f"{stat}: {stats_dict[stat]}")
                filtered_stats[stat] = stats_dict[stat]
        
        return filtered_stats
    else:
        print("No stats found for this pitcher.")
        return None

def project_player_stats_with_ai(player_name, stats):
    if not stats:
        print("No stats available to project.")
        return
        
    prompt = f"""
You are an advanced baseball analytics model.
Based on the following player stats, project realistic hitting stats for next season.

Player: {player_name}
Stats: {stats}

Please output projected values for:
- Batting Average (AVG)
- Home Runs (HR)
- Runs Batted In (RBI)
- On-Base Percentage (OBP)
- Slugging Percentage (SLG)
- OPS
- Games Played

Keep your response concise and formatted cleanly.
"""

    try:
        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        response = requests.post(
            f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result['candidates'][0]['content']['parts'][0]['text']
            print("\nProjected Stats for Next Season:")
            print(ai_response)
        
    except:
        pass

def project_pitcher_stats_with_ai(pitcher_name, stats):
    if not stats:
        print("No stats available to project.")
        return
        
    prompt = f"""
You are an advanced baseball analytics model.
Based on the following pitcher stats, project realistic pitching stats for next season.

Pitcher: {pitcher_name}
Stats: {stats}

Please output projected values for:
- Wins
- Losses
- ERA
- Strikeouts
- Walks
- Saves
- Innings Pitched
- WHIP
- Games Played

Keep your response concise and formatted cleanly.
"""

    try:
        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        response = requests.post(
            f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result['candidates'][0]['content']['parts'][0]['text']
            print("\nProjected Stats for Next Season:")
            print(ai_response)
        
    except:
        pass
        
while True:
    print("Welcome to the MLB Player Stat Projector!")
    time.sleep(1)
    while True:
        decision = input("Would you like to project next years stats for a player or pitcher? ")
        if decision == "player":
            player_id = None
            while player_id is None:
                name = input("What is the player's name? ")
                player_id = get_player_id_by_name(name)
            print(f"Player ID found: {player_id}")
            time.sleep(1)
            stats = get_player_stats(player_id)
            project_player_stats_with_ai(name, stats)
            break
        elif decision == "pitcher":
            pitcher_id = None
            while pitcher_id is None:
                name = input("What is the pitcher's name? ")
                pitcher_id = get_player_id_by_name(name)
            print(f"Pitcher ID found: {pitcher_id}")
            time.sleep(1)
            stats = get_pitcher_stats(pitcher_id)
            project_pitcher_stats_with_ai(name, stats)
            break
        else:
            print("Enter input exactly as 'player' or 'pitcher'")
            time.sleep(1)
    # continue with code
