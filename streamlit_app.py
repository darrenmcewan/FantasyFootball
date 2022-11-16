from espn_api.football import League
import pandas as pd
import numpy as np
import requests
import streamlit as st
from collections import defaultdict
import plotly.express as px
from statistics import variance

league_id = 115999423
year = 2022

league = League(league_id, year)
league.refresh()

best_matchup = 100
ind = 0
for i, match in enumerate(league.scoreboard()):
    matchupVar = variance([match.home_team.standing, match.away_team.standing])
    if matchupVar < best_matchup:
        best_matchup = matchupVar
        ind = i

matchup_week = league.scoreboard()[ind]

st.title("Sunnyvale Ballers")
st.subheader(f"{league.year} Season Overview")
st.markdown(f'### Current NFL Week: {league.current_week}', unsafe_allow_html=False)
st.markdown(
    f'#### This weeks matchup of the week is {matchup_week.home_team.team_name} ({matchup_week.home_team.standing}) vs {matchup_week.away_team.team_name} ({matchup_week.away_team.standing})')
projected_winner = league.box_scores()[ind].home_projected > league.box_scores()[ind].away_projected
if projected_winner:
    st.markdown(
        f"#### The home team {league.box_scores()[ind].home_team.team_name} is expected to win with {league.box_scores()[ind].home_projected}")
else:
    st.markdown(
        f"#### The away team {league.box_scores()[ind].away_team.team_name} is expected to win with {league.box_scores()[ind].away_projected}")

max_week = league.current_week - 1
week = st.slider("Select NFL Week to view", 1, max_week, max_week)


def team_scores(league, week):
    teams = defaultdict()
    for team in league.teams:
        teams[team.team_name] = team.scores[:week]
    return dict(teams)


def power_rankings(league, week):
    dict_1 = dict()
    for i in range(week):
        power_rankings = league.power_rankings(i)
        for ranking, team in power_rankings:
            dict_1.setdefault(team, []).append(ranking)
    return dict_1


def melt(df, col_vals, key, value):
    assert type(df) is pd.DataFrame
    keep_vars = df.columns.difference(col_vals)
    melted_sections = []
    for c in col_vals:
        melted_c = df[keep_vars].copy()
        melted_c[key] = c
        melted_c[value] = df[c]
        melted_sections.append(melted_c)
    melted = pd.concat(melted_sections)

    return melted


scores = team_scores(league, week)
df = pd.DataFrame.from_dict(scores)
df.index = df.index + 1

fig = px.line(df)
fig.update_layout(
    title="Scores Through the Weeks",
    xaxis_title="Week Num",
    yaxis_title="Points Scored",
    legend_title="Team",
)
fig.update_yaxes(showgrid=False)
st.plotly_chart(fig)

##power ranking
power_ranks = power_rankings(league, week)
df_pr = pd.DataFrame.from_dict(power_ranks)
df_pr.iloc[:, 0:] = df_pr.iloc[:, 0:].astype(str).astype(float)
df_pr.index = df_pr.index + 1
df_pr.reset_index(inplace=True)
df_pr = df_pr.rename(columns={'index': 'Week'})

melted = melt(df_pr, df_pr.iloc[:, 1:], key='Team', value='Power Ranking')
melted_df = melted[['Week', 'Team', 'Power Ranking']]

fig_pr = px.line(melted_df, x='Week', y='Power Ranking', color='Team')
fig_pr.update_layout(
    title="Week by Week Power Rankings",
    xaxis_title="Week Num",
    yaxis_title="Power Ranking",
    legend_title="Team",
)
fig_pr.update_yaxes(showgrid=False)
st.plotly_chart(fig_pr)

colnames = ['Player', 'Percent_owned', 'percent_started', 'projected_points', 'position rank', 'position',
            'current week opponent', 'opp rank']
positions = ['QB', 'WR', 'RB', 'TE', 'K']

free_agents = list()
st.markdown(f"### Week {max_week} Free Agents")
selected_positions = st.multiselect("Select Free Agent Position", positions)

for i in selected_positions:
    for free_agent in league.free_agents(7, 50, position=i):
        free_agents.append((free_agent.name, free_agent.percent_owned, free_agent.percent_started,
                            free_agent.projected_points, free_agent.posRank, free_agent.position,
                            free_agent.pro_opponent, free_agent.pro_pos_rank))

df = pd.DataFrame(free_agents, columns=colnames)
st.dataframe(df)

#Create plot showing unlucky win, lucky win, unlucky loss, lucky loss, quadrants

df2 = pd.DataFrame(scores)

st.dataframe(df2)

st.text(df2.describe())
