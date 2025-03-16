# data sourced from:
# https://github.com/vaastav/Fantasy-Premier-League/blob/master/data/2024-25/players_raw.csv

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mpld3
from mpld3 import plugins

df_with_managers = pd.read_csv("artefact//players_raw.csv")

df = df_with_managers [
    (df_with_managers["now_cost"] > 16)
]


# Create a large figure
plt.figure(figsize=(20, 10))  # Width=20 inches, Height=10 inches

xg = df['expected_goals']
gs = df['goals_scored']
plt.subplot(2,2,1)
plt.scatter(xg,gs, color = '#ff5821ff')

# Calculate linear trendline
coefficients_xg_gs = np.polyfit(xg, gs, 1)  # Degree 1 for linear
trendline_xg_gs = np.poly1d(coefficients_xg_gs)

# Generate x values for the trendline
x_trend_xg_gs = np.linspace(min(xg), max(xg), 100)
y_trend_xg_gs = trendline_xg_gs(x_trend_xg_gs)

# Plot the linear trendline
plt.plot(x_trend_xg_gs, y_trend_xg_gs, color='#6a73ffff')

plt.title("Expected Goals versus Goals Scored")
plt.xlabel("Expected goals")
plt.ylabel("Goals scored")



cost = (df['now_cost'])/10 # cost in the dataset is in terms of 100'000s, use millions for simplicity
total_points = df['total_points']
plt.subplot(2,2,2)
plt.scatter(cost,total_points, color = '#ff5821ff')

# Calculate linear trendline
coefficients_cost_tp = np.polyfit(cost, total_points, 1)  # Degree 1 for linear
trendline_cost_tp = np.poly1d(coefficients_cost_tp)

# Generate x values for the trendline
x_trend_cost_tp = np.linspace(min(cost), max(cost), 100)
y_trend_cost_tp = trendline_cost_tp(x_trend_cost_tp)

# Plot the linear trendline
plt.plot(x_trend_cost_tp, y_trend_cost_tp, color='#6a73ffff')

plt.title("Price versus Total Points")
plt.xlabel("Price of Player (millions)")
plt.ylabel("Total Points")



top_10_most_expensive_players = df[(df['now_cost_rank'] <= 10)]
names = top_10_most_expensive_players['web_name'].tolist()  # Convert to list for mpld3 compatibility
top_10_expected_goal_involvements = top_10_most_expensive_players['expected_goal_involvements']
plt.subplot(2,2,3)
bars = plt.bar(names,top_10_expected_goal_involvements, color = '#ff5821ff')
plt.title("Expected Goal Involvements for 10 most expensive players")
plt.xticks(rotation=45, ha='right')



form = df['form']
ownership_percentage = df['selected_by_percent']
plt.subplot(2,2,4)
plt.scatter(form,ownership_percentage, color = '#ff5821ff')

# Calculate linear trendline
coefficients_form_ownper = np.polyfit(form, ownership_percentage, 1)  # Degree 1 for linear
trendline_form_ownper = np.poly1d(coefficients_form_ownper)

# Generate x values for the trendline
x_trend_form_ownper = np.linspace(min(form), max(form), 100)
y_trend_form_ownper = trendline_form_ownper(x_trend_form_ownper)

# Plot the linear trendline
plt.plot(x_trend_form_ownper, y_trend_form_ownper, color='#6a73ffff')

plt.title("Form versus Ownership")
plt.xlabel("Form")
plt.ylabel("Ownership (percent)")



# Adjust the margins to reduce the left margin
plt.subplots_adjust(left=0.08)  # Reduce left margin; default is 0.125

# Add tooltips for each bar with the player names
tooltip = plugins.PointLabelTooltip(bars, labels=names)
mpld3.plugins.connect(plt.gcf(), tooltip)

# Convert the plot to HTML
html_str = mpld3.fig_to_html(plt.gcf())
# Write the HTML to a file called plot.htm
with open('website//plot.html', 'w', encoding="utf-8") as f:
    f.write(html_str)

plt.show()
