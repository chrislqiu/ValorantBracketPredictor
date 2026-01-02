import requests
from bs4 import BeautifulSoup
import json

URL = "https://www.vlr.gg/stats/?event_group_id=all&region=all&min_rounds=200&min_rating=1600&agent=all&map_id=all&timespan=all"

TEAMS = {
    "SEN": "Sentinels",
    "LOUD": "LOUD",
    "FUR": "FURIA",
    "NRG": "NRG",
    "C9": "Cloud9",
    "GEN": "Gen.G",
    "DRX": "DRX",
    "T1": "T1",
    "PRX": "Paper Rex",
    "TS": "Team Secret",
    "FNC": "FNATIC",
    "TL": "Team Liquid",
    "KC": "Karmine Corp",
    "G2": "G2 Esports",
    "NAVI": "Natus Vincere",
    "100T": "100 Thieves",
    "EG": "Evil Geniuses",
    "BLG": "Bilibili Gaming",
    "EDG": "EDward Gaming",
    "MIBR": "MIBR",
    "RRQ": "Rex Regum Qeon",
    "XLG": "Xi Lai Gaming",
    "GX": "GIANTX",
    "TH": "Team Heretics",
    "KRÜ": "KRÜ Esports",
    "LEV": "LEVIATÁN",
    "NV": "ENVY",
    "BBL": "BBL Esports",
    "FUT": "FUT Esports",
    "M8": "Gentle Mates",
    "VIT": "Team Vitality",
    "DFM": "DetonatioN FocusMe",
    "GE": "Global Esports",
    "ZETA": "ZETA DIVISION",
    "FPX": "FunPlus Phoenix",
    "AG": "All Gamers",
    "TE": "Trace Esports",
    "TYL": "TYLOO",
    "NOVA": "Nova Esports",
    "JDG": "JDG Esports",
    "TEC": "Titan Esports Club",
    "WOL": "Wolves Esports",
    "TLV": "Team Liquid Brazil",
    "SRG": "Shopify Rebellion Gold",
    "MIBR.GC": "MIBR GC",
    "KRÜB": "KRÜ BLAZE",
    "KC.GC": "Karmine Corp GC",
    "G2G": "G2 Gozen",
    "NOVA.GC": "Nova Esports GC",
    "XIP.GC": "Xipto Esports GC",
    "NS" : "Nongshim RedForce"
}

TEAM_URL = ["https://www.vlr.gg/team/2/sentinels", "https://www.vlr.gg/team/6961/loud", "https://www.vlr.gg/team/2406/furia",
            "https://www.vlr.gg/team/1034/nrg", "https://www.vlr.gg/team/188/cloud9", "https://www.vlr.gg/team/17/gen-g", 
            "https://www.vlr.gg/team/8185/drx", "https://www.vlr.gg/team/14/t1", "https://www.vlr.gg/team/624/paper-rex", 
            "https://www.vlr.gg/team/6199/team-secret", "https://www.vlr.gg/team/2593/fnatic", "https://www.vlr.gg/team/474/team-liquid",
            "https://www.vlr.gg/team/8877/karmine-corp", "https://www.vlr.gg/team/11058/g2-esports", "https://www.vlr.gg/team/4915/natus-vincere",
            "https://www.vlr.gg/team/120/100-thieves", "https://www.vlr.gg/team/5248/evil-geniuses", "https://www.vlr.gg/team/12010/bilibili-gaming",
            "https://www.vlr.gg/team/1120/edward-gaming", "https://www.vlr.gg/team/7386/mibr", "https://www.vlr.gg/team/878/rex-regum-qeon",
            "https://www.vlr.gg/team/13581/xi-lai-gaming", "https://www.vlr.gg/team/14419/giantx", "https://www.vlr.gg/team/1001/team-heretics",
            "https://www.vlr.gg/team/2355/kr-esports", "https://www.vlr.gg/team/2359/leviat-n", "https://www.vlr.gg/team/427/envy", 
            "https://www.vlr.gg/team/397/bbl-esports", "https://www.vlr.gg/team/1184/fut-esports", "https://www.vlr.gg/team/12694/gentle-mates",
            "https://www.vlr.gg/team/2059/team-vitality", "https://www.vlr.gg/team/278/detonation-focusme", "https://www.vlr.gg/team/918/global-esports",
            "https://www.vlr.gg/team/5448/zeta-division", "https://www.vlr.gg/team/11328/funplus-phoenix", "https://www.vlr.gg/team/1119/all-gamers",
            "https://www.vlr.gg/team/12685/trace-esports", "https://www.vlr.gg/team/731/tyloo", "https://www.vlr.gg/team/12064/nova-esports",
            "https://www.vlr.gg/team/13576/jdg-esports", "https://www.vlr.gg/team/14137/titan-esports-club", "https://www.vlr.gg/team/13790/wolves-esports",
            "https://www.vlr.gg/team/7055/team-liquid-brazil", "https://www.vlr.gg/team/14278/shopify-rebellion-gold", "https://www.vlr.gg/team/8050/mibr-gc",
            "https://www.vlr.gg/team/7511/kr-blaze", "https://www.vlr.gg/team/12255/karmine-corp-gc", "https://www.vlr.gg/team/6530/g2-gozen", 
            "https://www.vlr.gg/team/13807/nova-esports-gc", "https://www.vlr.gg/team/15317/xipto-esports-gc", "https://www.vlr.gg/team/11060/nongshim-redforce"]

# get each players name from the roster link above and add it to the set
def get_players():
    players = []

    for u in TEAM_URL:
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
            span = cell.find('span')
            if span and i < len(stat_names):
                stats[stat_names[i]] = span.text.strip()
        
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

    team_stats_json = create_team_stats_json(player_stats)

    with open('../data/team_stats.json', 'w', encoding='utf-8') as f:
        json.dump(team_stats_json, f, indent=2, ensure_ascii=False)

