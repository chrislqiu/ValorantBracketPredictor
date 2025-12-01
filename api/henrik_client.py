import os
from dotenv import load_dotenv
import requests

load_dotenv()
API_KEY = os.getenv("HENRIK_API_KEY")

BASE_URL = "https://api.henrikdev.xyz/valorant"

class HenrikAPI:
    def __init__(self):
        self.headers = {
            "Authorization": API_KEY,
            "Accept" : "*/*"
        }
    
    #-----Internal helper function to reduce call redundancy-----#

    """
    api._get("/valorant/v3/matches", params={"region": "na", "size": 50}) <-- example 
    """

    def _get(self, endpoint: str, params=None):
        url = f"{BASE_URL}{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code != 200:
            raise RuntimeError(f"Request failed: {response.status_code} {response.text}")
        
        try:
            data = response.json()
        except Exception:
            raise RuntimeError(f"Invalid JSON response from {url}")
        
        return data

    #-----Esports Endpoint-----#
    def get_esports_schedule(self):
        """
        Schedule data for upcoming schedules

        Query Params (Opt):
        region: international, north america, emea, latin_america, southeast_asia, etc
        league: vct_americas, challengers_na, game_changers_na, vct_emea, challengers_apac
        """
        return self._get("/v1/esports/schedule")
    
    def get_esports_match_by_id_v4(self, match_id: str):
        """
        Gets esports match by match id
        """
        return self._get(f"/v4/esports/match/{match_id}")
    
    def get_esports_teams(self):
        """
        Gets esports teams
        """ 
        return self._get(f"/v1/esports/teams")
    
    #-----Match Endpoints-----#
    def get_match_by_id_v2(self, match_id: str):
        """
        Obtains match/game info by match id
        """
        return self._get(f"/v2/match/{match_id}")
    
    def get_match_by_region_v4(self, region: str, match_id: str):
        """
        Obtains match by region and match id
        """
        return self._get(f"/v4/match/{region}/{match_id}")
    
    #-----Player Endpoints-----#
    def get_account_v2(self, name: str, tag: str):
        """
        returns acc info
        """
        return self._get(f"/v2/account/{name}/{tag}")
    
    def get_player_matches_v3(self, region: str, name: str, tag: str):
        """
        ret player matches

        Query Params (Opt):
        mode: competitive, custom, deathmatch, teamdeathmatch, etc
        map: Ascent, Split, Fracture, Bind, Breeze, District, etc
        size: 1, 2, 3, ..., 10
        """
        return self._get(f"/v3/matches/{region}/{name}/{tag}")
