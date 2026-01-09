import pandas as pd
import json

def add_player_diff_to_csv(csv_path, teams_db_path, output_path): 

    # load csv
    df = pd.read_csv(csv_path)

    # load team db
    with open(teams_db_path, 'r', encoding='utf-8') as f:
        team_db = json.load(f)

    # for teams not in our list, we assign a default avg
    defaults = {
        'team_avg_rating': 1.0,
        'team_avg_acs': 197.0, 
        'team_avg_KD': 1.0, 
        'team_avg_kast': 0.72, 
        'team_avg_adr': 132.0,
        'team_avg_kpr': 0.7,
        'team_avg_apr': 0.25, 
        'team_avg_fkpr': 0.1 
    }

    # stats we want to add
    player_stats = {
        'team_avg_rating': 1,
        'team_avg_acs': 1,
        'team_avg_KD': 2,
        'team_avg_kast': 2,
        'team_avg_adr': 1,
        'team_avg_kpr': 1,
        'team_avg_apr': 2,
        'team_avg_fkpr': 3 
    }

    norm_stats = ['rating', 'acs', 'KD', 'kast', 'adr', 'kpr', 'apr', 'fkpr']

    # initialize new columns
    for stat in player_stats:
        df[f'team1_{stat}'] = 0.0
        df[f'team2_{stat}'] = 0.0
        df[f'{stat}_diff'] = 0.0
    
    for stat in norm_stats:
        df[f'team1_norm_{stat}'] = 0.0
        df[f'team2_norm_{stat}'] = 0.0
        df[f'norm_{stat}_diff'] = 0.0
    
    df['team1_composite_score'] = 0.0
    df['team2_composite_score'] = 0.0
    df['composite_score_diff'] = 0.0
    
    # iterate through the rows in csv
    for idx, row in df.iterrows():
        team1 = row['team1']
        team2 = row['team2']

        for stat_name, decimal_places in player_stats.items():
            # team1 value
            t1_value = team_db[team1][stat_name] if team1 in team_db else defaults[stat_name]
            #  team2 value
            t2_value = team_db[team2][stat_name] if team2 in team_db else defaults[stat_name]
            # round
            df.at[idx, f'team1_{stat_name}'] = round(t1_value, decimal_places)
            df.at[idx, f'team2_{stat_name}'] = round(t2_value, decimal_places)

            # calc diff
            diff = t1_value - t2_value
            df.at[idx, f'{stat_name}_diff'] = round(diff, decimal_places)
        
        # normalized val
        for stat_name in norm_stats:
            t1_val = team_db[team1]['normalized'][stat_name] if team1 in team_db else 0
            t2_val = team_db[team2]['normalized'][stat_name] if team2 in team_db else 0

            df.at[idx, f'team1_norm_{stat_name}'] = round(t1_val, 3)
            df.at[idx, f'team2_norm_{stat_name}'] = round(t2_val, 3)

            diff = t1_val - t2_val
            df.at[idx, f'norm_{stat_name}_diff'] = round(diff, 3)

        # composite val
        t1_composite = team_db[team1]['composite_score'] if team1 in team_db else 0
        t2_composite = team_db[team2]['composite_score'] if team2 in team_db else 0

        df.at[idx, f'team1_composite_score'] = round(t1_composite, 3)
        df.at[idx, f'team2_composite_score'] = round(t2_composite, 3)

        df.at[idx, f'composite_score_diff'] = round(t1_composite - t2_composite, 3)

    df.to_csv(output_path, index=False)

    return df

if __name__ == "__main__":
    csv_path = '../data/matches_dataset.csv'
    team_db_path = '../data/teams_database.json'
    output_path = '../data/matches_with_player_stats.csv'

    df = add_player_diff_to_csv(csv_path, team_db_path, output_path)
