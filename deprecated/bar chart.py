import pandas as pd
import matplotlib.pyplot as plt
import mpld3

# Load dataset
data = pd.read_csv("PRA12.20241202165959.csv")


print(data.head(426))

years = data['Year']
values = data['VALUE']

# Plot a bar chart
plt.bar(years, values, color="green")

# Customize the graph
plt.title("Bar chart")
plt.xlabel("Years")
plt.ylabel("Values")

# Convert the plot to HTML
html_str = mpld3.fig_to_html(plt.gcf())
# Write the HTML to a file called plot.html'
with open('plot.html', 'w') as f:
    f.write(html_str)

# Display the graph
plt.show()