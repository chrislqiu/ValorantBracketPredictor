import pandas as pd
import json
from constants import TEAMS

CSV = "../data/matches_dataset.csv"

df = pd.read_csv(CSV)
with open('../data/teams_stats.json', 'r') as f:
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
        avg_rating = 1.0
        avg_acs = 197.0
        avg_KD = 1.05
        avg_kast = .72
        avg_adr = 151.2
        avg_kpr = .8
        avg_apr = .21
        avg_fkpr = .1
        
    # Save to database
    database[team] = {
        'winrate': round(winrate, 3),
        'recent_form': round(recent_form, 3),
        'avg_round_diff': round(avg_round_diff, 1),
        'team_avg_rating' : 1.0 if len(player_stats[team]['rating']) == 0 else round(sum(player_stats[team]['rating']) / len(player_stats[team]['rating']), 1),
        'team_avg_acs' : 197.0 if len(player_stats[team]['acs']) == 0 else round(sum(player_stats[team]['acs']) / len(player_stats[team]['acs']), 1), 
        'team_avg_KD' : 1.05 if len(player_stats[team]['KD']) == 0 else round(sum(player_stats[team]['KD']) / len(player_stats[team]['KD']), 2),
        'team_avg_kast' : .72 if len(player_stats[team]['kast']) == 0 else round(sum(player_stats[team]['kast']) / len(player_stats[team]['kast']), 2),
        'team_avg_adr' : 151.2 if len(player_stats[team]['adr']) == 0 else round(sum(player_stats[team]['adr']) / len(player_stats[team]['adr']), 1),
        'team_avg_kpr' : .8 if len(player_stats[team]['kpr']) == 0 else round(sum(player_stats[team]['kpr']) / len(player_stats[team]['kpr']), 1),
        
        'total_matches': data['matches']
    }

with open('../data/teams_database.json', 'w') as f:
    json.dump(database, f, indent=4)