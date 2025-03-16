import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df_fixtures = pd.read_csv("artefact\\fixtures_with_teams.csv")

fixtures_week29 = df_fixtures[(df_fixtures['event'] == 29)]
fixtures_week30 = df_fixtures[(df_fixtures['event'] == 30)]
fixtures_week31 = df_fixtures[(df_fixtures['event'] == 31)]
easy_home_fixtures_week29 = fixtures_week29 [(fixtures_week29['team_h_difficulty'] <= 2)]
easy_away_fixtures_week29 = fixtures_week29 [(fixtures_week29['team_a_difficulty'] <= 2)]


fig = make_subplots(
    rows=1, 
    cols=3, 
    subplot_titles=(
        "Gameweek 29",
        "Gameweek 30",
        "Gameweek 31"
    )
    )

team_h_week29 = fixtures_week29['team_h_name']
team_a_week29 = fixtures_week29['team_a_name']
team_h_difficulty_week29 = fixtures_week29['team_h_difficulty']
team_a_difficulty_week29 = fixtures_week29['team_a_difficulty']
team_h_week29_colour = fixtures_week29['team_h_colour']
team_a_week29_colour = fixtures_week29['team_a_colour']
fig.add_trace(
    go.Bar(
        x=team_h_week29,
        y=team_h_difficulty_week29,
        name='Gameweek 29',
        marker_color = team_h_week29_colour,
        text=team_h_week29,
        hovertext= team_a_week29,
        hovertemplate= (
            "<b>Team: %{x}</b><br>"
            "Fixture difficulty rating: %{y}<br>"
            "Gameweek 29<br>"
            "Opponent: %{hovertext}"
            "<extra></extra>"
        )
    ),row=1,col=1
)
fig.add_trace(
        go.Bar(
        x=team_a_week29,
        y=team_a_difficulty_week29,
        name='Gameweek 29',
        marker_color = team_a_week29_colour,
        text=team_a_week29,
        hovertext= team_h_week29,
        hovertemplate= (
            "<b>Team: %{x}</b><br>"
            "Fixture difficulty rating: %{y}<br>"
            "Gameweek 29<br>"
            "Opponent: %{hovertext}"
            "<extra></extra>"
        )
    ),row=1,col=1
)

team_h_week30 = fixtures_week30['team_h_name']
team_a_week30 = fixtures_week30['team_a_name']
team_h_difficulty_week30 = fixtures_week30['team_h_difficulty']
team_a_difficulty_week30 = fixtures_week30['team_a_difficulty']
team_h_week30_colour = fixtures_week30['team_h_colour']
team_a_week30_colour = fixtures_week30['team_a_colour']
fig.add_trace(
    go.Bar(
        x=team_h_week30,
        y=team_h_difficulty_week30,
        name='Gameweek 30',
        marker_color = team_h_week30_colour,
        text=team_h_week30,
        hovertext= team_a_week30,
        hovertemplate= (
            "<b>Team: %{x}</b><br>"
            "Fixture difficulty rating: %{y}<br>"
            "Gameweek 30<br>"
            "Opponent: %{hovertext}"
            "<extra></extra>"
        )
    ),row=1,col=2
)
fig.add_trace(
    go.Bar(
        x=team_a_week30,
        y=team_a_difficulty_week30,
        name='Gameweek 30',
        marker_color = team_a_week30_colour,
        text=team_a_week30,
        hovertext= team_h_week30,
        hovertemplate= (
            "<b>Team: %{x}</b><br>"
            "Fixture difficulty rating: %{y}<br>"
            "Gameweek 30<br>"
            "Opponent: %{hovertext}"
            "<extra></extra>"
        )
    ),row=1,col=2
)

team_h_week31 = fixtures_week31['team_h_name']
team_a_week31 = fixtures_week31['team_a_name']
team_h_difficulty_week31 = fixtures_week31['team_h_difficulty']
team_a_difficulty_week31 = fixtures_week31['team_a_difficulty']
team_h_week31_colour = fixtures_week31['team_h_colour']
team_a_week31_colour = fixtures_week31['team_a_colour']
fig.add_trace(
    go.Bar(
        x=team_h_week31,
        y=team_h_difficulty_week31,
        name='Gameweek 31',
        marker_color = team_h_week31_colour,
        text=team_h_week31,
        hovertext= team_a_week31,
        hovertemplate= (
            "<b>Team: %{x}</b><br>"
            "Fixture difficulty rating: %{y}<br>"
            "Gameweek 31<br>"
            "Opponent: %{hovertext}"
            "<extra></extra>"
        )
    ),row=1,col=3
)
fig.add_trace(
    go.Bar(
        x=team_a_week31,
        y=team_a_difficulty_week31,
        name='Gameweek 31',
        marker_color = team_a_week31_colour,
        text=team_a_week31,
        hovertext= team_h_week31 ,
        hovertemplate= (
            "<b>Team: %{x}</b><br>"
            "Fixture difficulty rating: %{y}<br>"
            "Gameweek 31<br>"
            "Opponent: %{hovertext}"
            "<extra></extra>"
        )
    ),row=1,col=3
)

# here I'm setting height and width, hiding the legend, and setting the template
fig.update_layout(
    showlegend=False,
    height=1000,
    width=1880,
    template="plotly_white",
    title_text = "<b>Fixture Difficulty Rating for the next three weeks</b>",
    title_font = dict(size=20),
    title_x= .5, # this puts the title text in the centre
    font_color = "#37003c"
)
# here I'm making sure that all the plots have the same axes
fig.update_yaxes(range=[0, 5])
# here I'm rotating the x-axis labels for the bar charts with names, so that they don't overlap and are readable
fig.update_xaxes(tickangle=45)
# here I'm saving the plot as a HTML file, to use in my recommendation area
fig.write_html("artefact//fdr_plot_for_recommendations.html")
fig.show()

df_players = pd.read_csv("artefact\\players_only_no_managers.csv")
df_players_next_round = df_players[(df_players['chance_of_playing_next_round'] == 100)]
df_players_next_round_wolves_bournemouth = df_players_next_round[(df_players_next_round['name'] == 'Bournemouth') | (df_players_next_round['name'] == 'Wolves')]
player_names_next_round_wolves_bournemouth = df_players_next_round_wolves_bournemouth['web_name']

list_player_names_next_round_wolves_bournemouth = player_names_next_round_wolves_bournemouth.tolist()

delimiter = ','
player_names_string = delimiter.join(list_player_names_next_round_wolves_bournemouth)
player_names_string = player_names_string.replace(",",", ") # I'm replacing every comma with a html line break to make the list more readable in html
with open("artefact\\player_names_next_round_wolves_bournemouth.txt", "w", encoding="utf-8") as text_file:
    text_file.write(player_names_string)


price = df_players_next_round_wolves_bournemouth['now_cost']/10
total_points = df_players_next_round_wolves_bournemouth['total_points']
team_colours = df_players_next_round_wolves_bournemouth['team_colour']
player_names = df_players_next_round_wolves_bournemouth['web_name']
team_names = df_players_next_round_wolves_bournemouth['name']
positions = df_players_next_round_wolves_bournemouth['element_type']
fig = go.Figure(
    data = go.Scatter(
        x=price, 
        y=total_points, 
        mode='markers',
        marker=dict(color=team_colours),
        hovertext= player_names,
        text= team_names,
        customdata= positions,
        hovertemplate=(
                "<b>%{hovertext}</b><br>"
                "Team: %{text}<br>"
                "Position: %{customdata}<br>"
                "Price: £%{x:.1f}M<br>"
                "Total Points: %{y}<br>"
                "<extra></extra>"
            ),
    )
)
fig.update_xaxes(title_text= "Price")
fig.update_yaxes(title_text= "Total Points")
fig.update_layout(
    showlegend=False,
    height=540,
    width=960,
    template="plotly_white",
    title_text = "<b>Total Points versus Price for Available Players</b>",
    title_font = dict(size=20),
    title_x= .5, # this puts the title text in the centre
    font_color = "#37003c"
)

fig.write_html("artefact//players_plot_for_recommendations.html")
fig.show()