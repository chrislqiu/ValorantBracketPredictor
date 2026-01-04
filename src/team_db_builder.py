import pandas as pd
import json
import numpy as np
from constants import TEAMS

CSV = "../data/matches_dataset.csv"

df = pd.read_csv(CSV)
with open('../data/team_stats.json', 'r', encoding='utf-8') as f:
    player_stats = json.load(f)

# creates dict struct 
team_stats = {team: {
    'matches': 0,
    'wins': 0,
    'round_diffs': [],
    'recent_wins': []
} for team in TEAMS.values()}

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
        'team_avg_rating': round(np.mean(player_stats[team]['rating']), 1) if player_stats[team]['rating'] else 1.0,
        'team_avg_acs': round(np.mean(player_stats[team]['acs']), 1) if player_stats[team]['acs'] else 197.0,
        'team_avg_KD': round(np.mean(player_stats[team]['KD']), 2) if player_stats[team]['KD'] else 1.0,
        'team_avg_kast': round(np.mean(player_stats[team]['kast']), 2) if player_stats[team]['kast'] else 0.72,
        'team_avg_adr': round(np.mean(player_stats[team]['adr']), 1) if player_stats[team]['adr'] else 132.0,
        'team_avg_kpr': round(np.mean(player_stats[team]['kpr']), 1) if player_stats[team]['kpr'] else 0.7,
        'team_avg_apr': round(np.mean(player_stats[team]['apr']), 2) if player_stats[team]['apr'] else 0.25,
        'team_avg_fkpr': round(np.mean(player_stats[team]['fkpr']), 3) if player_stats[team]['fkpr'] else 0.1,
        'total_matches': data['matches']
    }

with open('../data/teams_database.json', 'w') as f:
    json.dump(database, f, indent=4)