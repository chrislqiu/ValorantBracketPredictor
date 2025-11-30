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

    def get_esports_schedule(self):
        url = f"{BASE_URL}/v1/esports/schedule?region=international"
        response = requests.get(url, headers=self.headers)
        return response.json()