from api.henrik_client import HenrikAPI

api = HenrikAPI()
data = api.get_esports_schedule()

print(data)