import joblib
import json

def main():

    model = joblib.load('../model/model.pkl')
    with open('../data/teams_database.json', 'r') as f:
        teams = json.load(f)

    # listing teams
    team_list = list(teams.keys())
    print("\nTeams:")
    for i, t in enumerate(team_list, 1):
        print(f"{i}. {t}")
    
    # get user selection
    i1 = int(input("\nTeam 1 Number: ")) - 1
    i2 = int(input("Team 2 Number: ")) - 1

    t1, t2 = team_list[i1], team_list[i2]

    # calc features
    winrate_diff = teams[t1]['winrate'] - teams[t2]['winrate']
    form_diff = teams[t1]['recent_form'] - teams[t2]['recent_form']
    rnd_diff_diff = teams[t1]['avg_round_diff'] - teams[t2]['avg_round_diff']

    #predict
    pred = model.predict([[winrate_diff, form_diff, rnd_diff_diff]])[0]
    prob = model.predict_proba([[winrate_diff, form_diff, rnd_diff_diff]])[0]

    # Show result
    winner = t1 if pred == 1 else t2
    print(f"\nPrediction: {winner} wins")
    print(f"{t1}: {prob[1]:.1%}")
    print(f"{t2}: {prob[0]:.1%}")

if __name__ == "__main__":
    main()