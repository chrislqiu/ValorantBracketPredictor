import requests
from bs4 import BeautifulSoup
import json
from constants import TEAMS, TEAMS_URL

URL = "https://www.vlr.gg/stats/?event_group_id=all&region=all&min_rounds=200&min_rating=1600&agent=all&map_id=all&timespan=all"

# get each players name from the roster link above and add it to the set
def get_players():
    players = []

    for u in TEAMS_URL:
        res = requests.get(u)

        soup = BeautifulSoup(res.text, "html.parser")
        # team roster item contains member info
        member_card = soup.find_all('div', class_="team-roster-item")

        for card in member_card:
            # card only exists if the player is inactive or a sub or a non-player
            non_playing = card.find('div', class_="wf-tag mod-light team-roster-item-name-role")

            # if any of those above, exclude their stats
            if non_playing:
                continue
            
            # finds and saves alias
            alias = card.find('div', class_="team-roster-item-name-alias").text.strip()
            players.append(alias)
        '''MANUALLY ADDING PLAYER BC TEAM NOT UPDATED ON ROSTER'''
        players.append("cNed")
        players.append("qpert")
        players.append("al0rante")
        players.append("seven")
        players.append("NINJA")

    return players

# scrapes players that are in the current list of teams
def scrape_player(players_list):
    res = requests.get(URL)

    soup = BeautifulSoup(res.text, "html.parser")

    # body containing player rows
    body = soup.find('tbody')
    # obtaining list of the rows
    all_players = body.find_all('tr')

    # dict to store each player stats
    player_stats = {}
    stat_names = ["rating", "acs", "KD", "kast", "adr", "kpr", "apr", "fkpr"]

    for player in all_players:

        player_name_cell = player.find('td', class_="mod-player")

        team_div = player_name_cell.find('div', class_='stats-player-country')
        team = team_div.text.strip() if team_div else ""
        alias = player_name_cell.find('div', class_="text-of").text.strip()

        # check if player is on a roster
        if alias not in players_list:
            continue
        
        # unique key for dup names
        unique_key = f"{alias}_{team}" if team else alias

        # get stat cells
        stat_cells = player.find_all('td', class_="mod-color-sq")

        stats = {"team": team}

        # getting stats from the cells
        for i in range(min(len(stat_cells), 8)):
            cell = stat_cells[i]
            cell_text = cell.text.strip()
            if cell_text:
                stats[stat_names[i]] = cell_text
        
        #stores the stats
        player_stats[unique_key] = stats

    return player_stats

# create json file of the teams with their player stats
def create_team_stats_json(player_stats):
    team_stats = {}

    for full_name in TEAMS.values():
        team_stats[full_name] = {
            "rating": [],
            "acs": [],
            "KD": [],
            "kast": [],
            "adr": [],
            "kpr": [],
            "apr": [],
            "fkpr": []
        }
    
    for player, stats in player_stats.items():
        team_abbrev = stats.get("team", "")
        alias = stats.get("alias", player.split('_')[0] if '_' in player else player)

        '''TEMP CHANGES SINCE TEAM ISNT UPDATED'''
        if alias == "whzy":
            team_abbrev = "BLG"
        elif alias == "Reduxx":
            team_abbrev = "SEN"
        elif alias == "xeus":
            team_abbrev = "FUT"
        elif alias == "cNed":
            team_abbrev = "PCF"
        elif alias == "qpert":
            team_abbrev = "PCF"
        elif alias == "al0rante":
            team_abbrev = "PCF"
        elif alias == "al0rante":
            team_abbrev = "PCF"
        elif alias == "seven":
            team_abbrev = "PCF"
        elif alias == "NINJA":
            team_abbrev = "PCF"

        # Skip if team not found in TEAMS 
        if team_abbrev not in TEAMS:
            print(f"SKIPPED {alias} (team: {team_abbrev})")
            continue

        full_team_name = TEAMS[team_abbrev]

        # converts str val to float val
        def convert_to_float(val_str):
            # remove %
            if "%" in val_str:
                val_str = val_str.replace("%", "")
                return float(val_str) / 100
            else:
                return float(val_str)
        
        for stat_key in ["rating", "acs", "KD", "kast", "adr", "kpr", "apr", "fkpr"]:
            if stat_key in stats:
                
                # converts the value at each key to float
                float_val = convert_to_float(stats[stat_key])
                team_stats[full_team_name][stat_key].append(float_val)
            else:
                team_stats[full_team_name][stat_key].append(None)
    
    return team_stats



if __name__ == "__main__":

    # get list of players on a roster
    players = get_players()
    print(f"Found {len(players)} Players")

    # scrape stats for selected players
    player_stats = scrape_player(players)
    print(f"Got stats for {len(players)} Players")
    with open('../data/player_stats.json', 'w', encoding='utf-8') as f:
        json.dump(player_stats, f, indent=2, ensure_ascii=False)

    team_stats_json = create_team_stats_json(player_stats)

    with open('../data/team_stats.json', 'w', encoding='utf-8') as f:
        json.dump(team_stats_json, f, indent=2, ensure_ascii=False)

