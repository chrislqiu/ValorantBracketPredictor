import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://www.vlr.gg"
match_results_url = "https://www.vlr.gg/matches/results"

TEAMS = {
    "Sentinels", "LOUD", "FURIA", "NRG", "Cloud9", "Gen.G", "DRX", "T1",
    "Paper Rex", "Team Secret", "Fnatic", "Team Liquid", "Karmine Corp",
    "G2 Esports", "Natus Vincere", "100 Thieves", "Evil Geniuses",
    "Bilibili Gaming", "EDward Gaming", "MIBR", "Rex Regum Qeon",
    "Xi Lai Gaming", "GIANTX", "Team Heretics", "KRÜ Esports",
    "LEVIATÁN", "ENVY", "BBL Esports", "FUT Esports", "Gentle Mates",
    "Team Vitality", "DetonatioN FocusMe", "Global Esports", "ZETA DIVISION",
    "FunPlus Phoenix", "All Gamers", "Trace Esports", "TYLOO", "Nova Esports",
    "JDG Esports", "Titan Esports Club", "Wolves Esports",
    "Team Liquid Brazil", "Shopify Rebellion Gold", "MIBR GC", "KRÜ BLAZE",
    "Karmine Corp GC", "G2 Gozen", "Nova Esports GC", "Xipto Esports GC", "Nongshim RedForce"
}

def extract_map_scores(match_url: str):
    
    res = requests.get(match_url)
    soup = BeautifulSoup(res.text, "html.parser")

    map_data = []

    #finds div with class name, and looks for attribute data-game-id where it is not all
    map_container = soup.select('div.vm-stats-game[data-game-id]:not([data-game-id="all"])')
    
    for i, map in enumerate(map_container, 1):

        # Skip hidden containers
        style = map.get("style", "")
        if 'display: none' in style:
            continue

        #map name
        map_div = map.select_one(".map")
        map_name = map_div.get_text().split("\n")[3].strip()

        # score
        scores = map.select(".score")

        if len(scores) < 2:
            continue
        
        team1_score = int(scores[0].get_text(strip=True))
        team2_score = int(scores[1].get_text(strip=True))
        
        map_data.append({
            "map_num" : i,
            "map_name" : map_name,
            "t1_score" : team1_score,
            "t2_score" : team2_score,
            "round_diff" : team1_score - team2_score,
            "winner" : 1 if team1_score > team2_score else 0

        })

    return map_data

    


def scrape_vlr_page(page_num: int):

    matches = []

    # base url for first page, params for the other pages
    url = f"https://www.vlr.gg/matches/results?page={page_num}"
    res = requests.get(url)

    #converts the resp into text using html parser
    soup = BeautifulSoup(res.text, "html.parser")

    #selects html with <a> tags with classes "wf-module-item" and "match-item"
    match_card = soup.select("a.wf-module-item.match-item")

    for match in match_card:

        #splits by / using the href then accesses the index with match id
        match_id = match["href"].split("/")[1]
        match_url = BASE_URL + match["href"]

        #.match-item-vs-team is the class name where it contains info on the teams that played
        team_elements = match.select(".match-item-vs-team")

        #check for invalid match (1 team)
        if len(team_elements) < 2:
            continue
        
        #goes into the match-item-vs-team-name div, then looks into the text-of, which contains the name of the team
        t1_name = team_elements[0].select_one(".match-item-vs-team-name .text-of").text.strip()
        t1_score = int(team_elements[0].select_one(".match-item-vs-team-score").text.strip())

        t2_name = team_elements[1].select_one(".match-item-vs-team-name .text-of").text.strip()
        t2_score = int(team_elements[1].select_one(".match-item-vs-team-score").text.strip())

        #checks if at least one team is in the list
        if t1_name not in TEAMS and t2_name not in TEAMS:
            continue

        series_info = match.select_one(".match-item-event-series")
        series = series_info.text.strip() if series_info else ""

        event_info = match.select_one(".match-item-event")
        event = event_info.get_text().split("\n")[3].strip() if event_info else ""

        # extract map data
        maps = extract_map_scores(match_url)

        #find total round diff over all maps
        total_rnd_differential = sum(map["round_diff"] for map in maps)

        #BO1 checker
        if t1_score + t2_score > 5:
            if t1_score > t2_score:
                t1_score = 1
                t2_score = 0
            else:
                t1_score = 0
                t2_score = 1

        matches.append({
            "match_id" : match_id,
            "match_url" : match_url,
            "team1" : t1_name,
            "team2" : t2_name,
            "score1" : t1_score,
            "score2" : t2_score,
            "total_rnd_diff" : total_rnd_differential,
            "winner" : 1 if t1_score > t2_score else 0,
            "event" : event,
            "series" : series,
            "maps" : maps
        })
    
    return matches


def scrape_multiple_pages(end: int):
    all_matches = []

    for page in range(1, end + 1):
        print(f"Scraping Page: {page}")
        matches = scrape_vlr_page(page)
        all_matches.extend(matches)
        #time.sleep(1)
    
    return all_matches

def write_to_json(data, filename = "../data/matches_raw.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":

    matches = scrape_multiple_pages(200)
    write_to_json(matches)
    print(f"Wrote to file")
