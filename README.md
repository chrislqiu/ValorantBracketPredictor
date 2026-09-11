## Goal

Inspired by traditional sports bracket challenges like March Madness, Valorant offers its own in-game bracket challenge where players earn exclusive rewards based on prediction accuracy. This project was created to hopefully make very accurate predictions in order to earn those in-game rewards.

## Directions:
1. Install all libraries requirements.txt
- Run Files Below **In Order**
2. *vlr_scraper.py* ➜ Scrapes 230+ pages of matches from vlr.gg, outputs **matches_raw.json**
3. *build_csv.py* ➜ Takes in **matches_raw.json**, and flattens the data for ML model, outputs **matches_dataset.csv**
4. *player_stats_scraper.py* ➜ Scrapes org pages on vlr to store player names, then using player names, finds each player stats and stores them with their respective team, outputs **team_stats.json**
5. *team_db_builder.py* ➜ Takes in **team_stats.json**, builds the json for each team with match and player stats, outputs **teams_database.json**
6.  *add_players_to_csv.py* ➜ Takes in **matches_dataset.csv** and **teams_database.json**, then adds the extra features (team stats) to the csv and outputs a new copy, outputs **matches_with_player_stats**
7. *train_model.py* ➜ Takes in **matches_with_player_stats.csv**, creates the model and trains it on the data from the input, outputs **model.pkl**
8. *predictor.py* ➜ Takes in **model.pkl** and **teams_database.json**, allows user to choose matchup between two teams, outputs percentage of victory for both teams

> Note: model.pkl might be different, i.e. model(v1).pkl, model(v2).pkl, etc to indicate different versions, scrapers might not work if website html is changed  
> Data Last Scraped: 8/9/2026

## TODO 

- General Goals
    - implement a system where you can enter all the matchups and output final bracket

- v1 (64.8% Accuracy on Model using data from 1/14/2026)
    - [x] scrape map score for each map in a match
    - [x] train on winrate/ winrate diff, form/ form differential, round diff (when winning/losing)/ round diff differential

- v2 (67.3% Accuracy on Model using data from 1/14/2026)
    - [x] scraper player stats
    - [x] include player statistics: acs, adr, kd, etc
    - [x] update and retrain model

- v2.5 (67.7% Accuracy on Model using data from 1/14/2026)
    - [x] log transformation to to create more normal distribution, small difference in like a certain stat has more weight

- v3 (63.6% Accuracy on Model using data from 1/2026 to 5/3/2026)
    - [X] tested on data as of (6/14/26) with current year's data

- v4 (59.3% Accuracy on Model using data from 1/2026 to 8/9/2026)
    - [x] playoffs completed

- v5 (68.1% Accuracy on Model using data from 1/2026 to 9/10/2026)
    - [x] All relevant data gathered for Champs Shanghai


## Predictions (More in Folder)

* VCT 2026 Champs Shanghai Group Stage Predictions (v5 Model)
![alt text](/predictions/Champs%202026%20Group%20A%20Prediction.png)

![alt text](/predictions/Champs%202026%20Group%20B%20Prediction.png)

![alt text](/predictions/Champs%202026%20Group%20C%20Prediction.png)

![alt text](/predictions/Champs%202026%20Group%20D%20Prediction.png)

## Results & Reflection


