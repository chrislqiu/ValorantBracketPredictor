import json
from collections import defaultdict

RAW_MATCHES = "matches_raw.json"
TEAM_STATS = "team_stats.json"

# team stats model
team_stats = defaultdict(lambda: {
    "matches": 0,
    "wins": 0,
    "map_diff": 0, # difference in the SERIES
    "round_diff": 0 # total rounds diff throughout all maps
})

with open(RAW_MATCHES, "r", encoding = "utf-8") as f:
    matches = json.load(f)

for match in matches:
    t1 = match["team1"]
    t2 = match["team2"]

    team_stats[t1]["matches"] += 1
    team_stats[t2]["matches"] += 1

    # tracks how many wins
    if match["winner"] == 1:
        team_stats[t1]["wins"] += 1
    else:
        team_stats[t2]["wins"] += 1

    # tracks series differential
    team_stats[t1]["map_diff"] += (match["score1"] - match["score2"])
        # -= bc we are taking in perspective of t1
    team_stats[t2]["map_diff"] -= (match["score1"] - match["score2"])

    # tracks total round differential
    team_stats[t1]["round_diff"] += match["total_rnd_diff"]
    team_stats[t2]["round_diff"] -= match["total_rnd_diff"]

with open(TEAM_STATS, "w", encoding="utf-8") as f:
    json.dump(team_stats, f, ensure_ascii=False, indent=2)