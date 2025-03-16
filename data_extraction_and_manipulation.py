import pandas as pd

# here I'm loading the main player data file sourced from https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/refs/heads/master/data/2024-25/players_raw.csv
# this file does not contain player positions or team names, but there are other files from the same project which I will use to add this information in
# 'df' stands for dataframe
df_players_managers = pd.read_csv("players_raw.csv")

# here I'm loading a second file from the same source https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/refs/heads/master/data/2024-25/cleaned_players.csv
# this second file contains information on player positions (eg Goalkeeper, Defender) but not detailed information on player performance, which is in the first file
# these two files have the same  players on the same row, so they can be easily combined together
df_positions = pd.read_csv("cleaned_players.csv")

# this file is from https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/refs/heads/master/data/2024-25/teams.csv
# it contains the team codes as well as team names and information about team performance, wins, draws, losses etc.
df_teams = pd.read_csv("teams.csv")

# here I'm reading in the fixtures file, this is used for the recommendation
df_fixtures = pd.read_csv("fixtures.csv")

# I'm combining the element_type (which is actually player positions) from the second player dataset (cleaned_players.csv) with the main player data file (players_raw.csv), 
# then writing it to a new csv file called players_with_positions.csv
# every player is on the same row in both files, so I can assign them like this
df_players_managers['element_type'] =  df_positions['element_type']
df_players_managers.to_csv("players_with_positions.csv", index=False)

# here I'm adding a new column to teams_df called team_colour, as colours are not included in the original dataset
# I found these team colours on https://encycolorpedia.com/teams/football/epl
df_teams = df_teams.assign( team_colour = [ '#ef0107' , '#7b003a' , '#bf080a', '#e30613', '#005daa', '#034694', '#292d6b', '#274488', '#e5cbcb', '#3a64a3', '#0101e8', '#b31313', '#97c1e7', '#da030e', '#000000', '#e53233', '#ed1a3b', '#cccccc', '#7c2c3b', '#fdb913'])

# I'm adding team names and colours to the player data, in the players_raw.csv the team name is not included, only a team_code 
# the teams.csv file contains these team codes, next to team names, I am adding these team names to the player data based on the team codes
# I also added team colour data to the teams dataframe earlier, I am also combining this colour data with the player data, again based on team codes
df_with_teams = pd.merge(df_players_managers, df_teams[['code', 'name', 'team_colour']], left_on='team_code', right_on='code', how='left')

# for plot 5, I want to only use managers, so I am filtering out players here, and also saving the manager data to a new csv file
df_managers = df_with_teams[(df_with_teams['element_type'] == 'AM')]
# here I'm saving a new csv containg only managers, but with information I added about team name and colours
df_managers.to_csv("managers.csv", index=False) # this file is used by graphs.py

# here I'm filtering the player data, for use in the 1st 4 graphs, as I only want to look at players, not managers. Element type 'AM' corresponds to managers
df_players = df_with_teams[(df_with_teams['element_type'] != 'AM')]

# the player positions are displayed as 'GK', 'DEF', 'MID', and 'FWD'
# I am replacing these with 'Goalkeeper', 'Defender', 'Midfielder', and 'Forward'
df_players.loc[:, 'element_type'] = df_players['element_type'].replace({'GK': 'Goalkeeper', 'DEF': 'Defender', 'MID': 'Midfielder', 'FWD': 'Forward'})
df_players = df_players.assign(goal_involvements = df_players['assists']+df_players['goals_scored'])
# here I'm saving a new csv containg only players, without managers
df_players.to_csv("players_only_no_managers.csv", index=False) # this file is used by graphs.py and recommendations.py

# here I'm merging df_fixtures with df_teams based on the columns 'team_h' and 'id'
# this effectively adds new columns to df_fixtures with the team name and colour for the home team
df_fixtures = pd.merge(df_fixtures,df_teams[['id', 'name', 'team_colour']], left_on='team_h', right_on='id', how='left')

# here I'm renaming the 'name' column to 'team_h_name', this follows on from the above line
df_fixtures.rename(columns={'name': 'team_h_name', 'team_colour': 'team_h_colour'}, inplace=True)

# here I'm merging df_fixtures with df_teams based on the columns 'team_a' and 'id'
# this is for away teams, but apart from that is the same as the earlier similar line
df_fixtures = pd.merge(df_fixtures,df_teams[['id', 'name', 'team_colour']], left_on='team_a', right_on='id', how='left')

# here I'm renaming the 'name' column to 'team_h_name'
df_fixtures.rename(columns={'name': 'team_a_name', 'team_colour': 'team_a_colour'}, inplace=True)

# here I'm saving a new fixtures file which includes team names and colours, for use in the recommendation
df_fixtures.to_csv("fixtures_with_teams.csv", index=False)
