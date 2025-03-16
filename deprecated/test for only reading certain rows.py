import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the Excel file
data = pd.read_csv("PRA12.20241202165959.csv")

# Filter rows to only all offences and rate of reoffending within 1 year
reoffending_rate_all_offences = data[
    (data["Subsequent Reoffence"] == "All offences") &
    (data["Statistic Label"] == "Rate of re-offending within 1 year")
]

# Display the filtered data
print(reoffending_rate_all_offences)

# Optionally save the filtered data to a new csv file
reoffending_rate_all_offences.to_csv("reoffending_rate_all_offences.csv", index=False)

years = reoffending_rate_all_offences['Year']
rates = reoffending_rate_all_offences['VALUE']

# Plot a bar chart
plt.subplot(2,2,3)
plt.bar(years, rates, color="green")

# Customize the graph
plt.title("Rate of reoffending within 1 year for all offences")
plt.xlabel("Year")
plt.ylabel("Rate %")

# Display the graph
plt.show()