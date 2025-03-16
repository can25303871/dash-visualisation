import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# here I'm reading in the player data
# I created this file in "data_extraction_and_manipulation.py"
# it contains player statistics, from the origninal "players_raw.csv" file, but also team name and colour information, which I added in
# I also removed all managers from the file and saved them to "managers.csv", which I import below
df_players = pd.read_csv("players_only_no_managers.csv")

# this is the file that contains the extracted manager statistics and information
df_managers = pd.read_csv("managers.csv")

# this initialises the Dash app
app = dash.Dash(__name__)
server = app.server


# I start by defining the layout of the app
app.layout = html.Div([
    dcc.Dropdown(
        id='team-filter',
        options=[{'label': team, 'value': team} for team in df_players['name'].unique()],
        value=None,
        placeholder="Select a team to filter by"
    ),
    dcc.Graph(id='visualisations')
])

# this is the callback to update the visualizations based on the selected team
@app.callback(
    Output('visualisations', 'figure'),
    [Input('team-filter', 'value')]
)
def update_visualisations(selected_team):
    if selected_team:
        filtered_df_players = df_players[df_players['name'] == selected_team]
    else:
        filtered_df_players = df_players

    # here I'm creating a subplot grid (so that I can display multiple plots side by side) and naming each subplot
    # I have also set the bottom right plot to be empty, but doubled the width of the bottom middle plot, so it takes up the space of two plots
    fig = make_subplots(
        rows=2, cols=3,
        specs=[[{}, {}, {}],
                [{}, {"colspan": 2}, None]],
        subplot_titles=(
            "Goals Scored versus Expected Goals",
            "Total Points versus Price",
            "Expected versus Actual Goal Involvements for 10 most expensive players",
            "Form versus Ownership",
            "Total Points (Managers)",
            ""
        )
    )

    # Plot 1: expected goals versus goals scored
    exp_goals = filtered_df_players['expected_goals']
    goals_scored = filtered_df_players['goals_scored']
    fig.add_trace(
        go.Scatter(
            x=exp_goals, # x-axis
            y=goals_scored, # y-axis
            mode='markers', # this means the scatter points are displayed as coloured dots
            marker=dict(color=filtered_df_players['team_colour']), # I'm using the team colors (which I added to the dataframe earlier) for markers
            hovertext=filtered_df_players['web_name'],
            hovertemplate=(
                "<b>%{hovertext}</b><br>" # I'm making the player name bold
                "Team: %{text}<br>" # this is the team name
                "Position: %{customdata[0]}<br>" # this is the player position
                "Price: £%{customdata[1]}M<br>" # this is the in-game player price
                "Expected goals: %{x}<br>"
                "Goals scored: %{y}<br>"
                "<extra></extra>" # this line prevents the plot name from appearing next to the hover box
            ),
            text=filtered_df_players['name'],
            # since I am displaying so many lines in the hover template, I have to use the zip function here
            # this converts the 2 arrays into a list of tuples, which I can call in the hover template
            # I use this again in the later plots
            customdata=list(zip(filtered_df_players['element_type'], filtered_df_players['now_cost'] / 10)),
            name='Goals Scored versus Expected Goals'
        ),
        row=1, col=1
    )
    # here I'm making a trendline for plot 1 using numpy, then placing it on the scatter plot using plotly
    # this code is used for all of the trendlines
    # this line generates an array containing the 2 coefficients for the line of best fit(m and c from y=mx+c)
    coefficients_exp_goals_goals_scored = np.polyfit(exp_goals, goals_scored, 1) 
    # this line takes the 2 coeffiecient and makes them into a function, which returns a y-value when given an x-value
    trendline_exp_goals_goals_scored = np.poly1d(coefficients_exp_goals_goals_scored) 
    # this line generates 100 points between the min and max x-values, to serve as x-values for the trendline
    x_trend_exp_goals_goals_scored = np.linspace(min(exp_goals), max(exp_goals), 100)
    # this line generates the y values for the trendline, using the function defined above
    y_trend_exp_goals_goals_scored = trendline_exp_goals_goals_scored(x_trend_exp_goals_goals_scored)
    # this line adds the trendline to the scatter plot
    fig.add_trace(
        go.Scatter(x=x_trend_exp_goals_goals_scored, y=y_trend_exp_goals_goals_scored, mode='lines', line=dict(color='#37003c'), name='Trendline'),
        row=1, col=1
    )
    # here I'm adding labels to the axes
    fig.update_xaxes(title_text= "Expected Goals", row=1, col=1)
    fig.update_yaxes(title_text= "Goals Scored", row=1, col=1)

    # Plot 2: price versus total points
    total_points = filtered_df_players['total_points']
    fig.add_trace(
        go.Scatter(
            x=filtered_df_players['now_cost'] / 10,
            y=total_points,
            mode='markers',
            marker=dict(color=filtered_df_players['team_colour']),
            hovertext=filtered_df_players['web_name'],
            hovertemplate=(
                "<b>%{hovertext}</b><br>"
                "Team: %{text}<br>"
                "Position: %{customdata}<br>"
                "Price: £%{x:.1f}M<br>"
                "Total Points: %{y}<br>"
                "<extra></extra>"
            ),
            text=filtered_df_players['name'],
            customdata=filtered_df_players['element_type'],
            name='Total Points versus Price'
        ),
        row=1, col=2
    )
    coefficients_price_total_points = np.polyfit(filtered_df_players['now_cost'] / 10, total_points, 1)
    trendline_price_total_points = np.poly1d(coefficients_price_total_points)
    x_trend_price_total_points = np.linspace(min(filtered_df_players['now_cost'] / 10), max(filtered_df_players['now_cost'] / 10), 100)
    y_trend_price_total_points = trendline_price_total_points(x_trend_price_total_points)
    fig.add_trace(
        go.Scatter(
            x=x_trend_price_total_points,
            y=y_trend_price_total_points,
            mode='lines',
            line=dict(color='#37003c'),
            name='Trendline'
        ),
        row=1, col=2
    )
    fig.update_xaxes(title_text="Price", row=1, col=2)
    fig.update_yaxes(title_text="Total Points", row=1, col=2)

    # Plot 3: expected goal involvements for top 10 most expensive players
    top_10_most_expensive_players_unordered = df_players[(df_players['now_cost_rank'] <= 10)]
    top_10_most_expensive_players = top_10_most_expensive_players_unordered.sort_values(by='now_cost_rank')
    names_top_10_most_expensive_players = top_10_most_expensive_players['web_name']
    team_names_top_10 = top_10_most_expensive_players['name']
    positions_top_10 = top_10_most_expensive_players['element_type']
    team_colours_top_10 = top_10_most_expensive_players['team_colour']
    top_10_expected_goal_involvements = top_10_most_expensive_players['expected_goal_involvements']
    top_10_actual_goal_involvements = top_10_most_expensive_players['goal_involvements']
    price_top_10 = top_10_most_expensive_players['now_cost'] / 10
    fig.add_trace(
        go.Bar(
            x=names_top_10_most_expensive_players,
            y=top_10_expected_goal_involvements,
            marker_color=team_colours_top_10,
            hovertext=names_top_10_most_expensive_players,
            offsetgroup=0,
            hovertemplate=(
                "<b>%{hovertext}</b><br>"
                "Team: %{text}<br>"
                "Position: %{customdata[0]}<br>"
                "Price: £%{customdata[1]}M<br>"
                "Expected goal involvements: %{y}<br>(Expected goals + Expected assists)<br>"
                "Actual goal involvements: %{customdata[2]}<br>(Goals + Assists)"
                "<extra></extra>"
            ),
            text=team_names_top_10,
            # since I am displaying so many lines in the hover template, I have to use the zip function here, then convert to a list
            # this converts the 2 arrays into a list of tuples, which I can call in the hover template
            customdata=list(zip(positions_top_10, price_top_10, top_10_actual_goal_involvements)),
            name='Expected goal involvements for 10 most expensive players'
        ),
        row=1, col=3
    )
    fig.add_trace(
        go.Bar(
            x=names_top_10_most_expensive_players,
            y=top_10_actual_goal_involvements,
            marker_color=team_colours_top_10,
            hovertext=names_top_10_most_expensive_players,
            offsetgroup=1,
            hovertemplate=(
                "<b>%{hovertext}</b><br>"
                "Team: %{text}<br>"
                "Position: %{customdata[0]}<br>"
                "Price: £%{customdata[1]}M<br>"
                "Expected goal involvements: %{customdata[2]}<br>(Expected goals + Expected assists)<br>"
                "Actual goal involvements: %{y}<br>(Goals + Assists)"
                "<extra></extra>"
            ),
            text=team_names_top_10,
            customdata=list(zip(positions_top_10, price_top_10, top_10_expected_goal_involvements)),
            name='Actual goal involvements for 10 most expensive players'
        ),
        row=1, col=3
    )
    fig.update_xaxes(title_text="Player Name", tickangle=45, row=1, col=3)
    fig.update_yaxes(title_text="Actual/Expected Goal Involvements", row=1, col=3)

    # Plot 4: form versus ownership
    form = filtered_df_players['form']
    ownership_percentage = filtered_df_players['selected_by_percent']
    fig.add_trace(
        go.Scatter(
            x=ownership_percentage,
            y=form,
            mode='markers',
            marker=dict(color=filtered_df_players['team_colour']),
            hovertext=filtered_df_players['web_name'],
            hovertemplate=(
                "<b>%{hovertext}</b><br>"
                "Team: %{text}<br>"
                "Position: %{customdata[0]}<br>"
                "Price: £%{customdata[1]}M<br>"
                "Ownership percentage: %{x}%<br>"
                "Form: %{y}<br>"
                "<extra></extra>"
            ),
            text=filtered_df_players['name'],
            customdata=list(zip(filtered_df_players['element_type'], filtered_df_players['now_cost'] / 10)),
            name='Form versus Ownership'
        ),
        row=2, col=1
    )
    coefficients_ownper_form = np.polyfit(ownership_percentage, form, 1)
    trendline_ownper_form = np.poly1d(coefficients_ownper_form)
    x_trend_ownper_form = np.linspace(min(ownership_percentage), max(ownership_percentage), 100)
    y_trend_ownper_form = trendline_ownper_form(x_trend_ownper_form)
    fig.add_trace(
        go.Scatter(x=x_trend_ownper_form, y=y_trend_ownper_form, mode='lines', line=dict(color='#37003c'), name='Trendline'),
        row=2, col=1
    )
    fig.update_xaxes(title_text="Ownership (percentage)", row=2, col=1)
    fig.update_yaxes(title_text="Form", row=2, col=1)

    # Plot 5: Total Points for Managers
    manager_points = df_managers['total_points']
    manager_names = df_managers['web_name']
    manager_teams = df_managers['name']
    manager_colours = df_managers['team_colour']
    manager_price = df_managers['now_cost'] / 10
    fig.add_trace(
        go.Bar(
            x=manager_names,
            y=manager_points,
            marker_color=manager_colours,
            hovertext=manager_names,
            hovertemplate=(
                "<b>%{hovertext}</b><br>"
                "Team: %{text}<br>"
                "Price: £%{customdata}M<br>"
                "Total Points: %{y}<br>"
                "<extra></extra>"
            ),
            text=manager_teams,
            customdata=manager_price,
            name='Total Points (Managers)'
        ),
        row=2, col=2
    )
    fig.update_xaxes(title_text="Manager Name", tickangle=45, row=2, col=2)
    fig.update_yaxes(title_text="Total Points", row=2, col=2)

    # Update layout
    fig.update_layout(
        showlegend=False,
        height=1000,
        width=1880,
        template="plotly_white"
    )

    return fig

# this runs the app
if __name__ == '__main__':
    app.run_server(debug=True)
