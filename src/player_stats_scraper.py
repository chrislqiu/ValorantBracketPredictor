import requests
from bs4 import BeautifulSoup
import json
from constants import TEAMS, TEAMS_URL, DEFAULT_STATS

URL = "https://www.vlr.gg/stats/?sort=rating2&dir=desc&tier=vct&region=all&span=2026&side=all&role=all&agent=all&map_id=all&min_rounds=0&min_rating=0&page=1"

# get each players name from the roster link above and add it to the set
def get_players():
    players = []

    for u in TEAMS_URL:
        res = requests.get(u)
        soup = BeautifulSoup(res.text, "html.parser")
        member_card = soup.find_all('div', class_="team-roster-item")

        for card in member_card:
            non_playing = card.find('div', class_="wf-tag mod-light team-roster-item-name-role")
            if non_playing:
                continue
            
            alias = card.find('div', class_="team-roster-item-name-alias").text.strip()
            players.append(alias)

    # If you need to manually add players, do it here but make sure the mapping exists
    # players.append("xeus")  # Only if you're sure this player exists in the stats

    return players

# scrapes players that are in the current list of teams
# map each stat_name to its column's data-col attribute
STAT_COL_MAP = {
    "rating": "rating2",
    "acs": "acs",
    "KD": "kd",
    "kast": "kast",
    "adr": "adr",
    "kpr": "kpr",
    "apr": "apr",
    "fkpr": "fkfd",
}

def scrape_player(players_list):
    with open('player_stats.html', 'r', encoding='utf-8') as f:
        res_text = f.read()

    soup = BeautifulSoup(res_text, "html.parser")
    body = soup.find('tbody')
    all_players = body.find_all('tr')

    player_stats = {}

    for player in all_players:
        player_name_cell = player.find('td', class_="mod-player")

        alias = player_name_cell.find('div', class_="text-of").text.strip()
        team_div = player_name_cell.find('div', class_="st-pl-country")
        team = team_div.text.strip() if team_div else ""

        if alias not in players_list:
            continue

        unique_key = f"{alias}_{team}" if team else alias

        stats = {"team": team, "alias": alias}
        stats.update({k: str(v) for k, v in DEFAULT_STATS.items()})

        # look up each stat by its data-col, not by position
        for stat_name, data_col in STAT_COL_MAP.items():
            cell = player.find('td', attrs={"data-col": data_col})
            if cell is None:
                continue  # keep default
            if "mod-empty" in cell.get("class", []):
                continue  # explicitly empty -> keep default
            cell_text = cell.text.strip()
            if cell_text:
                stats[stat_name] = cell_text
            # else: blank text -> keep default

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
        if alias == 'H1ber':
            team_abbrev = "M8"



        # Skip if team not found in TEAMS 
        if team_abbrev not in TEAMS:
            print(f"SKIPPED {alias} (team: {team_abbrev})")
            continue

        full_team_name = TEAMS[team_abbrev]

        # converts str val to float val
        for stat_key in DEFAULT_STATS:
            stat_value = stats[stat_key]

            if "%" in str(stat_value):
                float_value = float(
                    str(stat_value).replace("%", "")
                ) / 100
            else:
                float_value = float(stat_value)

            team_stats[full_team_name][stat_key].append(float_value)
    
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

