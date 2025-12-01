import requests
from bs4 import BeautifulSoup
import json
import time

match_results_url = "https://www.vlr.gg/matches/results"

#End on page 250
def scrape_vlr_results():

    all_matches = []
    a_links = []

    for page in range(1, 2):

        # base url for first page, params for the other pages
        url = f"{match_results_url}" if page == 1 else f"{match_results_url}?page={page}"
        res = requests.get(url)

        #converts the resp into text using html parser
        soup = BeautifulSoup(res.text, "html.parser")

        #selects html with <a> tags with classes "wf-module-item" and "match-item"
        match_card = soup.select("a.wf-module-item.match-item")
        with open("output_file.txt", "w", encoding="utf-8") as f:
            for match in match_card:
                f.write(str(match))
                f.write("\n\n---\n\n")


    """
    with open("output_file.txt", "w", encoding="utf-8") as f:
        for card in match_card:
            f.write(str(card))
            f.write("\n\n---\n\n")
    """


scrape_vlr_results()