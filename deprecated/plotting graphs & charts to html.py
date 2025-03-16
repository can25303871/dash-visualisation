import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import mpld3


data = pd.read_csv("artefact//PRA12.20241202165959.csv") # Load dataset

#print(data.head(426))

# Filter rows to only all offences and rate of reoffending within 1 year
reoffending_rate_all_offences = data[
    (data["Subsequent Reoffence"] == "All offences") &
    (data["Statistic Label"] == "Rate of re-offending within 1 year")
]
# Save the filtered data to a new csv file
reoffending_rate_all_offences.to_csv("reoffending_rate_all_offences.csv", index=False)

# Display the filtered data
#print(reoffending_rate_all_offences)

years = data['Year']
values = data['VALUE']

# Plot a scatter plot
plt.subplot(2,2,1)
plt.scatter(years, values, color="red")

# Customise the plot
plt.title("Scatter plot")
plt.xticks([2017,2018,2019,2020,2021])  # Set tick locations
plt.xlabel("Year")
plt.ylabel("Values")

# Plot a bar chart
plt.subplot(2,2,2)
plt.bar(years, values, color="green")

# Customise the graph
plt.title("Bar chart")
plt.xticks([2017,2018,2019,2020,2021])  # Set tick locations
plt.xlabel("Year")
plt.ylabel("Values")

years = reoffending_rate_all_offences['Year']
rates = reoffending_rate_all_offences['VALUE']

# Plot a bar chart
plt.subplot(2,2,3)
plt.bar(years, rates, color="purple")

# Customize the graph
plt.title("Rate of reoffending within 1 year\nfor all offences")
plt.xticks([2017,2018,2019,2020,2021])  # Set tick locations
plt.xlabel("Year")
plt.ylabel("Rate %")

# Display the figures
plt.tight_layout(pad=2)

# Convert the plot to HTML
html_str = mpld3.fig_to_html(plt.gcf())
# Write the HTML to a file called plot.html'
with open('plot.html', 'w') as f:
    f.write(html_str)

plt.show()
