import json
import pandas as pd

matches_df = pd.read_csv("matches_dataset.csv")

with open("team_stats.json", "r", encoding = "utf-8") as f:
    team_stats = json.load(f)

# orient index keeps the dict keys as row indices
team_stats_df = pd.DataFrame.from_dict(team_stats, orient="index")
team_stats_df.index.name = "team"
# moves team name to thier own col
team_stats_df.reset_index(inplace=True)

# merge stats for team1
matches_df = matches_df.merge(
    # ensures t1 col are prefixed with t1
    team_stats_df.add_prefix("t1_"),
    #searching for name match
    left_on="team1",
    right_on="t1_team",
    how="left"
)

# merge stats for team2
matches_df = matches_df.merge(
    team_stats_df.add_prefix("t2_"),
    left_on="team2",
    right_on="t2_team",
    how="left"
)
# drop duplicate columns after merge
matches_df.drop(columns=["t1_team", "t2_team"], inplace=True)

matches_df.to_csv("merged_dataset.csv", index=False, encoding="utf-8")
