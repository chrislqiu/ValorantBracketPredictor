import json
import csv
from collections import defaultdict

JSON = "matches_raw.json"
CSV = "matches_dataset.csv"

with open(JSON, "r", encoding="utf-8") as f:
    matches = json.load(f)

# team stats
team_stats = defaultdict(lambda: {
    "matches_played": 0,
    "wins": 0,
    "recent_results": [],  # Last 10 matches (1=win, 0=loss)
    "recent_round_diffs": []  # Last 5 round differences
})

rows = []

# Process from OLDEST to NEWEST (iterate backwards)
for match in reversed(matches):
    maps = match.get("maps", [])
    
    if not maps:
        continue
    
    team1 = match["team1"]
    team2 = match["team2"]
    
    # Get stats BEFORE this match
    t1_stats = team_stats[team1]
    t2_stats = team_stats[team2]
    
    # Calculate winrates from past matches
    team1_winrate = t1_stats["wins"] / max(1, t1_stats["matches_played"])
    team2_winrate = t2_stats["wins"] / max(1, t2_stats["matches_played"])
    
    # Calculate recent form (last 10 matches)
    team1_recent_form = sum(t1_stats["recent_results"][-10:]) / max(1, len(t1_stats["recent_results"]))
    team2_recent_form = sum(t2_stats["recent_results"][-10:]) / max(1, len(t2_stats["recent_results"]))
    
    # Calculate recent round differences (last 5 matches)
    team1_avg_rnd_diff = sum(t1_stats["recent_round_diffs"][-5:]) / max(1, len(t1_stats["recent_round_diffs"]))
    team2_avg_rnd_diff = sum(t2_stats["recent_round_diffs"][-5:]) / max(1, len(t2_stats["recent_round_diffs"]))
    
    # Current match map stats
    round_diffs = [m["round_diff"] for m in maps]
    avg_map_rnd_diff = sum(round_diffs) / len(round_diffs)
    maps_won_team1 = sum(1 for m in maps if m["winner"] == 1)
    
    # Create row
    row = {
        "match_id": match["match_id"],
        "team1": team1,
        "team2": team2,
        "winner": match["winner"],
        
        # Team statistics (from PAST matches)
        "team1_winrate": round(team1_winrate, 3),
        "team2_winrate": round(team2_winrate, 3),
        "winrate_diff": round(team1_winrate - team2_winrate, 3),
        
        "team1_recent_form": round(team1_recent_form, 3),
        "team2_recent_form": round(team2_recent_form, 3),
        "form_diff": round(team1_recent_form - team2_recent_form, 3),
        
        "team1_avg_rnd_diff": round(team1_avg_rnd_diff, 1),
        "team2_avg_rnd_diff": round(team2_avg_rnd_diff, 1),
        "rnd_diff_diff": round(team1_avg_rnd_diff - team2_avg_rnd_diff, 1),
        
        # Current match features
        "avg_map_rnd_diff": round(avg_map_rnd_diff, 1),
        "maps_won_team1": maps_won_team1,
        "maps_won_team2": len(maps) - maps_won_team1,
        "total_rnd_diff": match["total_rnd_diff"],
        "total_score": match["score1"] + match["score2"]
    }
    
    rows.append(row)
    
    # UPDATE stats AFTER processing (for future matches)
    # Team 1 stats
    team_stats[team1]["matches_played"] += 1
    if match["winner"] == 1:
        team_stats[team1]["wins"] += 1
    
    team_stats[team1]["recent_results"].append(1 if match["winner"] == 1 else 0)
    team_stats[team1]["recent_round_diffs"].append(match["total_rnd_diff"])
    
    # Keep only last 10 results and 5 round diffs
    if len(team_stats[team1]["recent_results"]) > 10:
        team_stats[team1]["recent_results"].pop(0)
    if len(team_stats[team1]["recent_round_diffs"]) > 5:
        team_stats[team1]["recent_round_diffs"].pop(0)
    
    # Team 2 stats
    team_stats[team2]["matches_played"] += 1
    if match["winner"] == 0:
        team_stats[team2]["wins"] += 1
    
    team_stats[team2]["recent_results"].append(1 if match["winner"] == 0 else 0)
    team_stats[team2]["recent_round_diffs"].append(-match["total_rnd_diff"])  # Reverse sign
    
    if len(team_stats[team2]["recent_results"]) > 10:
        team_stats[team2]["recent_results"].pop(0)
    if len(team_stats[team2]["recent_round_diffs"]) > 5:
        team_stats[team2]["recent_round_diffs"].pop(0)

# Reverse rows back to newest-first (original order)
rows = list(reversed(rows))

# Write to CSV
with open(CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
