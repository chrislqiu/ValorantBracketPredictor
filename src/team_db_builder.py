import pandas as pd
import numpy as np
import json

CSV = "../data/matches_dataset.csv"

df = pd.read_csv(CSV)

TEAMS = [
    "Sentinels", "LOUD", "FURIA", "NRG", "Cloud9", "Gen.G", "DRX", "T1",
    "Paper Rex", "Team Secret", "FNATIC", "Team Liquid", "Karmine Corp",
    "G2 Esports", "Natus Vincere", "100 Thieves", "Evil Geniuses",
    "Bilibili Gaming", "EDward Gaming", "MIBR", "Rex Regum Qeon",
    "Xi Lai Gaming", "GIANTX", "Team Heretics", "KRÜ Esports",
    "LEVIATÁN", "ENVY", "BBL Esports", "FUT Esports", "Gentle Mates",
    "Team Vitality", "DetonatioN FocusMe", "Global Esports", "ZETA DIVISION",
    "FunPlus Phoenix", "All Gamers", "Trace Esports", "TYLOO", "Nova Esports",
    "JDG Esports", "Titan Esports Club", "Wolves Esports",
    "Team Liquid Brazil", "Shopify Rebellion Gold", "MIBR GC", "KRÜ BLAZE",
    "Karmine Corp GC", "G2 Gozen", "Nova Esports GC",
    "Xipto Esports GC", "Nongshim RedForce"
]

# creates dict struct 
team_stats = {team: {
    'matches': 0,
    'wins': 0,
    'round_diffs': [],
    'recent_wins': []
} for team in TEAMS}

for _, match in df.iterrows():
    team1, team2 = match['team1'], match['team2']
    winner = match['winner']
    
    # Update team1 
    if team1 in team_stats:
        team_stats[team1]['matches'] += 1
        if winner == 1:
            team_stats[team1]['wins'] += 1
            team_stats[team1]['recent_wins'].append(1)
        else:
            team_stats[team1]['recent_wins'].append(0)
        
        team_stats[team1]['round_diffs'].append(match['total_rnd_diff'])
    
    # Update team2 
    if team2 in team_stats:
        team_stats[team2]['matches'] += 1
        if winner == 0:
            team_stats[team2]['wins'] += 1
            team_stats[team2]['recent_wins'].append(1)
        else:
            team_stats[team2]['recent_wins'].append(0)
        
        team_stats[team2]['round_diffs'].append(-match['total_rnd_diff'])

# Calculate final stats for database
database = {}

for team, data in team_stats.items():
    # Calculate winrate
    if data['matches'] > 0:
        winrate = data['wins'] / data['matches']
        
        # Recent form (last 10 matches winrate)
        recent_wins = data['recent_wins'][-10:]
        if recent_wins:
            recent_form = sum(recent_wins) / len(recent_wins)
        else:
            recent_form = 0.5
        
        # Average round difference (last 5 matches)
        recent_diffs = data['round_diffs'][-5:]
        if recent_diffs:
            avg_round_diff = sum(recent_diffs) / len(recent_diffs)
        else:
            avg_round_diff = 0.0
    else:
        # Default stats for teams with no matches
        winrate = 0.5
        recent_form = 0.5
        avg_round_diff = 0.0
        
    # Save to database
    database[team] = {
        'winrate': round(winrate, 3),
        'recent_form': round(recent_form, 3),
        'avg_round_diff': round(avg_round_diff, 1),
        'total_matches': data['matches']
    }

with open('../data/teams_database.json', 'w') as f:
    json.dump(database, f, indent=4)