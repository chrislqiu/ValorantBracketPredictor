# ValorantBracketPredictor

Building ML model to predict bracket outcomes for Valorant Tournaments

Order of Files to Run:
- vlr_scraper.py -> Obtain most recent matches and converts them to json
- build_csv.py -> Get csv representation
- team_db_builder.py -> Builds the json for each team, which include the inputs to the predictor
- player_stats_scraper.py -> Obtain stats for player and use as input and model training for later on
- train_model.py -> Generate model for predictor
- predictor.py -> To predict outcomes between two teams

## TODO Before Building Model

- v1 (61.4% Accuracy on Model as of 1/1/2026)
    - [x] scrape map score for each map in a match
    - [x] train on winrate/ winrate diff, form/ form differential, round diff (when winning/losing)/ round diff differential
    - [ ] vlr incldude team map stats -> not needed bc we do not know what map are being played until the day of the event
![alt text](/predictions/VCT%202026%20Americas%20Kickoff%20(v1).png)

- v2
    - [x] scraper player stats
    - [x] include player statistics: acs, adr, kd, etc
    - [ ] update and retrain model

- Need to scrape more teams and wait for more roster annoucements
