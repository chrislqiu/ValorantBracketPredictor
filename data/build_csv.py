import json
import csv

JSON = "matches_raw.json"
CSV = "matches_dataset.csv"


with open(JSON, "r", encoding="utf-8") as f:
    matches = json.load(f)

rows = []

for match in matches:
    maps = match["maps"]

    if not maps:
        continue

    #finds round differential for each map in the series
    round_diffs = [map["round_diff"] for map in maps]

    row = {
        "match_id" : match["match_id"],
        "team1": match["team1"],
        "team2": match["team2"],
        "event": match["event"],
        "series": match["series"],
        "winner": match["winner"],
        "score_diff": match["score1"] - match["score2"],
        "total_rnd_diff": match["total_rnd_diff"],
        "num_maps": len(maps),
        "avg_round_diff": sum(round_diffs) / len(round_diffs),
        "max_round_diff": max(round_diffs),
        "min_round_diff": min(round_diffs),
        "maps_played": "|".join(map["map_name"] for map in maps),
    }

    rows.append(row)

    with open(CSV, "w", newline = "", encoding = "utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)