import joblib
import json

def main():

    model = joblib.load('../model/model(v2.5).pkl')
    with open('../data/teams_database.json', 'r') as f:
        teams = json.load(f)

    # listing teams
    team_list = sorted(list(teams.keys()))
    print("\nTeams:")
    for i, t in enumerate(team_list, 1):
        print(f"{i}. {t}")
    
    # get user selection
    i1 = int(input("\nTeam 1 Number: ")) - 1
    i2 = int(input("Team 2 Number: ")) - 1

    t1, t2 = team_list[i1], team_list[i2]

    # v1, calc features
    winrate_diff = teams[t1]['winrate'] - teams[t2]['winrate']
    form_diff = teams[t1]['recent_form'] - teams[t2]['recent_form']
    rnd_diff_diff = teams[t1]['avg_round_diff'] - teams[t2]['avg_round_diff']
    
    #v2 features
    team_avg_rating_diff = teams[t1]['team_avg_rating'] - teams[t2]['team_avg_rating']
    team_avg_acs_diff = teams[t1]['team_avg_acs'] - teams[t2]['team_avg_acs']
    team_avg_KD_diff = teams[t1]['team_avg_KD'] - teams[t2]['team_avg_KD']
    team_avg_kast_diff = teams[t1]['team_avg_kast'] - teams[t2]['team_avg_kast']
    team_avg_adr_diff = teams[t1]['team_avg_adr'] - teams[t2]['team_avg_adr']
    team_avg_kpr_diff = teams[t1]['team_avg_kpr'] - teams[t2]['team_avg_kpr']
    team_avg_apr_diff = teams[t1]['team_avg_apr'] - teams[t2]['team_avg_apr']
    team_avg_fkpr_diff = teams[t1]['team_avg_fkpr'] - teams[t2]['team_avg_fkpr']

    #v2.5 features
    norm_rating_diff = teams[t1]['normalized']['rating'] - teams[t2]['normalized']['rating']
    norm_acs_diff = teams[t1]['normalized']['acs'] - teams[t2]['normalized']['acs']
    norm_KD_diff = teams[t1]['normalized']['KD'] - teams[t2]['normalized']['KD']
    norm_kast_diff = teams[t1]['normalized']['kast'] - teams[t2]['normalized']['kast']
    norm_adr_diff = teams[t1]['normalized']['adr'] - teams[t2]['normalized']['adr']
    norm_kpr_diff = teams[t1]['normalized']['kpr'] - teams[t2]['normalized']['kpr']
    norm_apr_diff = teams[t1]['normalized']['apr'] - teams[t2]['normalized']['apr']
    norm_fkpr_diff = teams[t1]['normalized']['fkpr'] - teams[t2]['normalized']['fkpr']
    composite_score_diff = teams[t1]['composite_score'] - teams[t2]['composite_score']

    #predict
    #v1
    #pred = model.predict([[winrate_diff, form_diff, rnd_diff_diff]])[0]
    #prob = model.predict_proba([[winrate_diff, form_diff, rnd_diff_diff]])[0]
    #v2
   #pred = model.predict([[winrate_diff, form_diff, rnd_diff_diff, team_avg_rating_diff, team_avg_acs_diff, team_avg_KD_diff, team_avg_kast_diff,
   #                        team_avg_adr_diff, team_avg_kpr_diff, team_avg_apr_diff, team_avg_fkpr_diff]])[0]
   #prob = model.predict_proba([[winrate_diff, form_diff, rnd_diff_diff, team_avg_rating_diff, team_avg_acs_diff, team_avg_KD_diff, team_avg_kast_diff,
   #                              team_avg_adr_diff, team_avg_kpr_diff, team_avg_apr_diff, team_avg_fkpr_diff]])[0]

    #v2.5
    pred = model.predict([[winrate_diff, form_diff, rnd_diff_diff, team_avg_rating_diff, team_avg_acs_diff, team_avg_KD_diff, team_avg_kast_diff,
                           team_avg_adr_diff, team_avg_kpr_diff, team_avg_apr_diff, team_avg_fkpr_diff, norm_rating_diff, norm_acs_diff, norm_KD_diff,
                           norm_kast_diff, norm_adr_diff, norm_kpr_diff, norm_apr_diff, norm_fkpr_diff, composite_score_diff]])[0]
    prob = model.predict_proba([[winrate_diff, form_diff, rnd_diff_diff, team_avg_rating_diff, team_avg_acs_diff, team_avg_KD_diff, team_avg_kast_diff,
                                 team_avg_adr_diff, team_avg_kpr_diff, team_avg_apr_diff, team_avg_fkpr_diff, norm_rating_diff, norm_acs_diff, norm_KD_diff,
                           norm_kast_diff, norm_adr_diff, norm_kpr_diff, norm_apr_diff, norm_fkpr_diff, composite_score_diff]])[0]

    # Show result
    winner = t1 if pred == 1 else t2
    print(f"\nPrediction: {winner} wins")
    print(f"{t1}: {prob[1]:.1%}")
    print(f"{t2}: {prob[0]:.1%}")

if __name__ == "__main__":
    main()