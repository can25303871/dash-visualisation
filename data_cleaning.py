import pandas as pd

data_dirty = pd.read_csv("players_raw_dirty.csv") # load dataset
data_dirty = data_dirty.replace(r'^\s*&',float('NaN'), regex=True)# replace all empty strings or strings of only spaces with NaN (not a number) in float form
data_clean = data_dirty.dropna(thresh=20) # keep only the rows with at least 20 non-Na values
data_clean.to_csv("players_raw_cleaned.csv", index=False) # save to a new file players_cleaned.csv
print("Data cleaned and saved to players_raw_cleaned.csv")