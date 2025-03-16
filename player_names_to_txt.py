import pandas as pd

df = pd.read_csv("artefact//players_raw.csv")

player_names = df['web_name']
player_names_list = player_names.tolist()

delimiter = ','
player_names_string = delimiter.join(player_names_list)

with open("player_names.txt", "w") as text_file:
    text_file.write(player_names_string)
