import pandas as pd
import json
import numpy as np
from constants import TEAMS, DEFAULT_STATS
from scipy import stats

CSV = "../data/matches_dataset.csv"

df = pd.read_csv(CSV)
with open('../data/team_stats.json', 'r', encoding='utf-8') as f:
    player_stats = json.load(f)

# median stats of all players on the list
def calculate_baselines(player_stats):
    baselines = {}
    
    stats_to_calc = ['rating', 'acs', 'KD', 'kast', 'adr', 'kpr', 'apr', 'fkpr']
    
    for stat in stats_to_calc:
        all_values = []
        for team_data in player_stats.values():
            if stat in team_data:
                all_values.extend(team_data[stat])
        
        if all_values:
            baselines[stat] = np.median(all_values)
        else:
            baselines[stat] = DEFAULT_STATS[stat]
    
    return baselines

# Calculate baselines from your data
PRO_BASELINES = calculate_baselines(player_stats)

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

# collect stats for normalization
team_records = []

for team, data in team_stats.items():

    if data['matches'] > 0:
        # calc winrate
        winrate = data['wins'] / data['matches']

        # Recent form (last 10 matches winrate)
        recent_wins = data['recent_wins'][-10:]
        recent_form = sum(recent_wins) / len(recent_wins) if recent_wins else 0.5

        # Average round difference (last 5 matches)
        recent_diffs = data['round_diffs'][-5:]
        avg_round_diff = sum(recent_diffs) / len(recent_diffs) if recent_diffs else 0.0
    else:
        winrate = 0.5
        recent_form = 0.5
        avg_round_diff = 0.0

    # save raw data
    team_records.append({
        'team': team,
        'winrate': winrate,
        'recent_form': recent_form,
        'avg_round_diff': avg_round_diff,
        'rating': np.mean(player_stats[team]['rating']) if player_stats[team]['rating'] else 1.0,
        'acs': np.mean(player_stats[team]['acs']) if player_stats[team]['acs'] else 197.0,
        'KD': np.mean(player_stats[team]['KD']) if player_stats[team]['KD'] else 1.0,
        'kast': np.mean(player_stats[team]['kast']) if player_stats[team]['kast'] else 0.72,
        'adr': np.mean(player_stats[team]['adr']) if player_stats[team]['adr'] else 132.0,
        'kpr': np.mean(player_stats[team]['kpr']) if player_stats[team]['kpr'] else 0.7,
        'apr': np.mean(player_stats[team]['apr']) if player_stats[team]['apr'] else 0.25,
        'fkpr': np.mean(player_stats[team]['fkpr']) if player_stats[team]['fkpr'] else 0.1,
        'total_matches': data['matches']
    })

# save as dataframe for normalization
df_teams = pd.DataFrame(team_records)

# log transform multiplicative stats, 1.1 -> 1.2 kd is not the same as 1.2 -> 1.3
mult_stats = ['KD', 'kpr', 'fkpr']
# loops can checks to make sure stats exist
for stat in mult_stats:
    if stat in df_teams.columns:
        # logging the value
        df_teams[f'{stat}_norm'] = np.log(df_teams[stat] / PRO_BASELINES[stat])

# log it transformation, bc we are dealing with percentages
percent_stats = ['kast', 'winrate', 'recent_form']
# used in clipping to prevent log(0) and log(inf or 1/0)
epsilon = 0.001
for stat in percent_stats:
    if stat in df_teams.columns:
        baseline = PRO_BASELINES.get(stat, 0.5)
        team_clipped = np.clip(df_teams[stat], epsilon, 1 - epsilon)
        base_clipped = np.clip(baseline, epsilon, 1 - epsilon)

        logit_team = np.log(team_clipped / (1 - team_clipped))
        logit_base = np.log(base_clipped / (1 - base_clipped))
        df_teams[f'{stat}_norm'] = logit_team - logit_base

# additive stats, since increase is proportional
linear_stats = ['acs', 'adr', 'apr', 'rating']
for stat in linear_stats:
    if stat in df_teams.columns:
        df_teams[f'{stat}_norm'] = df_teams[stat] - PRO_BASELINES[stat]

# zscore for the stats
for norm_col in [col for col in df_teams.columns if col.endswith('_norm')]:
    df_teams[norm_col] = stats.zscore(df_teams[norm_col], nan_policy='omit')

# weight importance
weights = {
    'rating_norm': 0.25,
    'kpr_norm': 0.15,
    'KD_norm': 0.12,
    'acs_norm': 0.10,
    'adr_norm': 0.08,
    'kast_norm': 0.10,
    'fkpr_norm': 0.08,
    'apr_norm': 0.05,
    'winrate_norm': 0.05,
    'recent_form_norm': 0.02,
}

df_teams['composite_score'] = 0
for norm_stat, weight in weights.items():
    if norm_stat in df_teams.columns:
        df_teams['composite_score'] += df_teams[norm_stat].fillna(0) * weight

database = {}

for _, row in df_teams.iterrows():
    team = row['team']
    
    normalized_scores = {}
    for stat in ['rating', 'acs', 'KD', 'kast', 'adr', 'kpr', 'apr', 'fkpr']:
        norm_col = f'{stat}_norm'
        if norm_col in row and not pd.isna(row[norm_col]):
            normalized_scores[stat] = round(float(row[norm_col]), 3)
    
    database[team] = {
        'winrate': round(float(row['winrate']), 3),
        'recent_form': round(float(row['recent_form']), 3),
        'avg_round_diff': round(float(row['avg_round_diff']), 1),
        'team_avg_rating': round(float(row['rating']), 3),
        'team_avg_acs': round(float(row['acs']), 1),
        'team_avg_KD': round(float(row['KD']), 3),
        'team_avg_kast': round(float(row['kast']), 3),
        'team_avg_adr': round(float(row['adr']), 1),
        'team_avg_kpr': round(float(row['kpr']), 3),
        'team_avg_apr': round(float(row['apr']), 3),
        'team_avg_fkpr': round(float(row['fkpr']), 3),
        'total_matches': int(row['total_matches']),
        
        'normalized': normalized_scores,
        # overall team strength
        'composite_score': round(float(row['composite_score']), 3),
    }

with open('../data/teams_database.json', 'w') as f:
    json.dump(database, f, indent=4)