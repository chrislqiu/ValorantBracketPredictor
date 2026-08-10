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
            if stat in team_data and team_data[stat]:
                # Filter out None values and convert to float
                for value in team_data[stat]:
                    if value is not None:
                        try:
                            all_values.append(float(value))
                        except (ValueError, TypeError):
                            # Skip values that can't be converted to float
                            continue
        
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

# Helper function to safely get mean of stats, ignoring None values
def safe_mean(stats_list):
    if not stats_list:
        return None
    # Filter out None values
    valid_values = [x for x in stats_list if x is not None]
    if not valid_values:
        return None
    return np.mean(valid_values)

# collect stats for normalization
team_records = []

for team, data in team_stats.items():
    # Safely get team stats
    team_rating = safe_mean(player_stats.get(team, {}).get('rating', []))
    team_acs = safe_mean(player_stats.get(team, {}).get('acs', []))
    team_KD = safe_mean(player_stats.get(team, {}).get('KD', []))
    team_kast = safe_mean(player_stats.get(team, {}).get('kast', []))
    team_adr = safe_mean(player_stats.get(team, {}).get('adr', []))
    team_kpr = safe_mean(player_stats.get(team, {}).get('kpr', []))
    team_apr = safe_mean(player_stats.get(team, {}).get('apr', []))
    team_fkpr = safe_mean(player_stats.get(team, {}).get('fkpr', []))

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
        'rating': team_rating if team_rating is not None else 1.0,
        'acs': team_acs if team_acs is not None else 197.0,
        'KD': team_KD if team_KD is not None else 1.0,
        'kast': team_kast if team_kast is not None else 0.72,
        'adr': team_adr if team_adr is not None else 132.0,
        'kpr': team_kpr if team_kpr is not None else 0.7,
        'apr': team_apr if team_apr is not None else 0.25,
        'fkpr': team_fkpr if team_fkpr is not None else 0.1,
        'total_matches': data['matches']
    })

# save as dataframe for normalization
df_teams = pd.DataFrame(team_records)

# Log transform multiplicative stats
mult_stats = ['KD', 'kpr', 'fkpr']
for stat in mult_stats:
    if stat in df_teams.columns:
        # Ensure we have valid values before logging
        valid_mask = df_teams[stat] > 0
        df_teams[f'{stat}_norm'] = np.nan  # Initialize with NaN
        df_teams.loc[valid_mask, f'{stat}_norm'] = np.log(
            df_teams.loc[valid_mask, stat] / PRO_BASELINES.get(stat, 1.0)
        )

# Logit transformation for percentages
percent_stats = ['kast', 'winrate', 'recent_form']
epsilon = 0.001
for stat in percent_stats:
    if stat in df_teams.columns:
        baseline = PRO_BASELINES.get(stat, 0.5)
        team_clipped = np.clip(df_teams[stat], epsilon, 1 - epsilon)
        base_clipped = np.clip(baseline, epsilon, 1 - epsilon)

        logit_team = np.log(team_clipped / (1 - team_clipped))
        logit_base = np.log(base_clipped / (1 - base_clipped))
        df_teams[f'{stat}_norm'] = logit_team - logit_base

# Additive stats
linear_stats = ['acs', 'adr', 'apr', 'rating']
for stat in linear_stats:
    if stat in df_teams.columns:
        df_teams[f'{stat}_norm'] = df_teams[stat] - PRO_BASELINES.get(stat, 0)

# Z-score normalization (ignore NaN values)
for norm_col in [col for col in df_teams.columns if col.endswith('_norm')]:
    if df_teams[norm_col].notna().sum() > 1:  # Need at least 2 values for zscore
        df_teams[norm_col] = stats.zscore(df_teams[norm_col].fillna(0), nan_policy='omit')
    else:
        df_teams[norm_col] = df_teams[norm_col].fillna(0)

# Weight importance
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
        'composite_score': round(float(row['composite_score']), 3),
    }

with open('../data/teams_database.json', 'w') as f:
    json.dump(database, f, indent=4)