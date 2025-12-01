import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://www.vlr.gg"
match_results_url = "https://www.vlr.gg/matches/results"

#End on page 250
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
        t1_score = team_elements[0].select_one(".match-item-vs-team-score").text.strip()

        t2_name = team_elements[1].select_one(".match-item-vs-team-name .text-of").text.strip()
        t2_score = team_elements[1].select_one(".match-item-vs-team-score").text.strip()

        print(f"{t1_name} {t1_score} vs {t2_name} {t2_score}")

        break


scrape_vlr_page(1)