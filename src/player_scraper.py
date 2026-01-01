import requests
from bs4 import BeautifulSoup
import json

url = "https://www.vlr.gg/stats/?event_group_id=all&region=all&min_rounds=200&min_rating=1600&agent=all&map_id=all&timespan=all"

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
    "FNC": "Fnatic",
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

players_list = {}
# get each players name from the roster link above and add it to the set
def get_players():
    pass

def scrape_player():
    pass

if __name__ == "__main__":
    pass