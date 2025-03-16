import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Load the data
df_with_managers = pd.read_csv("https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/refs/heads/master/data/2024-25/players_raw.csv")

# Filter the data, I only want to look at players, not managers
df = df_with_managers[(df_with_managers["now_cost"] > 16)]

# Create a subplot grid
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "Expected Goals versus Goals Scored",
        "Price versus Total Points",
        "Expected Goal Involvements for 10 most expensive players",
        "Form versus Ownership"
    )
)

# Plot 1: Expected Goals vs Goals Scored
xg = df['expected_goals']
gs = df['goals_scored']
player_names = df['web_name']
fig.add_trace(
    go.Scatter(x=xg, 
               y=gs, 
               mode='markers', 
               marker=dict(color='#ff5821'), 
               hovertext=player_names, 
               hovertemplate= (
                   "<b>%{hovertext}</b><br>"  # Player name in bold
                   "Expected goals: %{x}<br>"
                   "Goals scored: %{y}<br>"
                   "<extra></extra>"
               )
    ),
    row=1, col=1
)

# Trendline for Plot 1
coefficients_xg_gs = np.polyfit(xg, gs, 1)
trendline_xg_gs = np.poly1d(coefficients_xg_gs)
x_trend_xg_gs = np.linspace(min(xg), max(xg), 100)
y_trend_xg_gs = trendline_xg_gs(x_trend_xg_gs)
fig.add_trace(
    go.Scatter(x=x_trend_xg_gs, y=y_trend_xg_gs, mode='lines', line=dict(color='#6a73ff'), name='Trendline'),
    row=1, col=1
)

# Plot 2: Price vs Total Points
cost = df['now_cost'] / 10  # Convert cost to millions
total_points = df['total_points']
fig.add_trace(
    go.Scatter(
            x=cost,
            y=total_points, 
            mode='markers', 
            marker=dict(color='#ff5821'), 
            hovertext=player_names, 
            hovertemplate=(
                "<b>%{hovertext}</b><br>"  # Player name in bold
                "Price: %{x:.1f}M<br>"      # Price in millions
                "Total Points: %{y}<br>"    # Total points
                "<extra></extra>"           # Remove extra hover info
            )
    ),
            row=1, col=2
)

# Trendline for Plot 2
coefficients_cost_tp = np.polyfit(cost, total_points, 1)
trendline_cost_tp = np.poly1d(coefficients_cost_tp)
x_trend_cost_tp = np.linspace(min(cost), max(cost), 100)
y_trend_cost_tp = trendline_cost_tp(x_trend_cost_tp)
fig.add_trace(
    go.Scatter(
        x=x_trend_cost_tp, 
        y=y_trend_cost_tp, 
        mode='lines', 
        line=dict(color='#6a73ff'), 
        name='Trendline' 
        ),
    row=1, col=2
)

# Plot 3: Expected Goal Involvements for Top 10 Most Expensive Players
top_10_most_expensive_players = df[(df['now_cost_rank'] <= 10)]
names_top_10_most_expensive_players = top_10_most_expensive_players['web_name'].tolist()
top_10_expected_goal_involvements = top_10_most_expensive_players['expected_goal_involvements']
colours = ['red', 'brown', 'darkblue', 'red', 'lightblue', 'lightblue', 'lightblue', 'red', 'black', 'lightgrey']
fig.add_trace(
    go.Bar(
        x=names_top_10_most_expensive_players,
        y=top_10_expected_goal_involvements, 
        marker_color= colours, 
        hovertext= names_top_10_most_expensive_players,
        hovertemplate= (
            "<b>%{hovertext}</b><br>"
            "Expected goal involvements: %{y}<br>(Expected goals + Expected assists)"
            "<extra></extra>"
        )
        ),
    row=2, col=1
)

# Plot 4: Form vs Ownership
form = df['form']
ownership_percentage = df['selected_by_percent']
fig.add_trace(
    go.Scatter(
        x=form, 
        y=ownership_percentage, 
        mode='markers', 
        marker=dict(color='#ff5821'), 
        hovertext=player_names, 
        hovertemplate= (
            "<b>%{hovertext}</b><br>"  # Player name in bold
            "Form: %{x}<br>"
            "Ownership percentage: %{y}%<br>"
            "<extra></extra>"
        )
    ),
    row=2, col=2
)

# Trendline for Plot 4
coefficients_form_ownper = np.polyfit(form, ownership_percentage, 1)
trendline_form_ownper = np.poly1d(coefficients_form_ownper)
x_trend_form_ownper = np.linspace(min(form), max(form), 100)
y_trend_form_ownper = trendline_form_ownper(x_trend_form_ownper)
fig.add_trace(
    go.Scatter(x=x_trend_form_ownper, y=y_trend_form_ownper, mode='lines', line=dict(color='#6a73ff'), name='Trendline'),
    row=2, col=2
)

# Update layout for better visualization
fig.update_layout(
    showlegend=False,
    height=1000,  # Increase height of the figure
    width=1600,   # Increase width of the figure
    template="plotly_white"
)

# Rotate x-axis labels for the bar chart
fig.update_xaxes(tickangle=45, row=2, col=1)

# Save the plot as an HTML file
fig.write_html("artefact//plot_from_plotly.html")

# Show the plot
fig.show()