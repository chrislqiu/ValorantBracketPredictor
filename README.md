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
> Data Last Scraped: 1/14/2026

## TODO 

- General Goals
    - rescrape matches (last updated 1/5/2026)
    - wait for roster updates to make predictions for other regions 
    - implement a system where you can enter all the matchups and output final bracket
    - improve accuracy further?

- v1 (64.8% Accuracy on Model using data from 1/4/2026)
    - [x] scrape map score for each map in a match
    - [x] train on winrate/ winrate diff, form/ form differential, round diff (when winning/losing)/ round diff differential

- v2 (67.3% Accuracy on Model using data from 1/14/2026)
    - [x] scraper player stats
    - [x] include player statistics: acs, adr, kd, etc
    - [x] update and retrain model

- v2.5 (67.7% Accuracy on Model using data from 1/14/2026)
    - [x] log transformation to to create more normal distribution, small difference in like a certain stat has more weight

- v3
    - [ ] split the team avg stats into role specific stast, because avg comes out to be very similar
        - how to assign players to a certain role?
        - flex players exist, meaning they play mutiple roles
        - vlr only contains top three agents image (.png) in the player stats page (no text)

## Predictions (More in Folder)

* Personal Prediction not based on ML
![alt text](/predictions/VCT%202026%20Americas%20Kickoff%20(Personal).png)
* v1 Model Prediction using org/team based data (historical team winrate, round differential, and recent form (win-rate in last 10 games)) 
![alt text](/predictions/VCT%202026%20Americas%20Kickoff%20(v1P).png)
* v2 Model Prediction using org/team based data, and team average player data (team avg rating, KD, acs, etc)
![alt text](/predictions/VCT%202026%20Americas%20Kickoff%20(v2P).png)
* v2.5 Model Prediction using everthing above, with the addtion of normalized player stats
![alt text](/predictions/VCT%202026%20Americas%20Kickoff%20(v2.5P).png)
