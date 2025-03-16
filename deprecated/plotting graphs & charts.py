import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("PRA12.csv") # Load dataset

# Filter rows to only all offences and rate of reoffending within 1 year
reoffending_rate_all_offences = data[
    (data["Subsequent Reoffence"] == "All offences") &
    (data["Statistic Label"] == "Rate of re-offending within 1 year")
]
# Save the filtered data to a new csv file
reoffending_rate_all_offences.to_csv("reoffending_rate_all_offences.csv", index=False)


#specify data to plot
years = data['Year']
values = data['VALUE']
# Plot a scatter plot
plt.subplot(2,2,1)
plt.scatter(years, values, color="red")

# Customise the plot
plt.title("Scatter plot") #Set title
plt.xticks([2017,2018,2019,2020,2021])  # Set tick locations
plt.xlabel("Year")
plt.ylabel("Values")

# Plot a bar chart
plt.subplot(2,2,2)
plt.bar(years, values, color="green")

# Customise the graph
plt.title("Bar chart") #Set title
plt.xticks([2017,2018,2019,2020,2021])  # Set tick locations
plt.xlabel("Year")
plt.ylabel("Values")

years = reoffending_rate_all_offences['Year']
rates = reoffending_rate_all_offences['VALUE']

# Plot a bar chart
plt.subplot(2,2,3)
plt.bar(years, rates, color="purple")

# Customize the graph
plt.title("Rate of reoffending within 1 year\nfor all offences") #Set title
plt.xticks([2017,2018,2019,2020,2021])  # Set tick locations
plt.xlabel("Year")
plt.ylabel("Rate %")

# Display the figures
plt.tight_layout(pad=2)
plt.show()
