from api.henrik_client import HenrikAPI
import json

api = HenrikAPI()
data = api.get_player_matches_v3("na", "queue", "IUsuk")

"""
with open("output_file.txt", "w") as f:
    # dump converts json to str
    json.dump(data, f, indent=4)
"""
