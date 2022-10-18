from espn_api.football import League
import pandas as pd
import numpy as np
import requests
import streamlit as st
from collections import defaultdict
import plotly.express as px


league_id = 115999423
year = 2022

league = League(league_id, year)

st.title("Sunnyvale Ballers")
st.subheader(f"{league.year} Season")

max_week = league.current_week-1
week = st.slider("Select NFL Week to view", 1,max_week, max_week)

def team_scores(league, week):
    teams = defaultdict()
    for team in league.teams:
        teams[team.team_name] = team.scores[:week]
    return dict(teams)

scores = team_scores(league, week)


df = pd.DataFrame.from_dict(scores)
df.index = df.index+1
fig = px.line(df)
fig.update_layout(
    title="Scores Through the Weeks",
    xaxis_title="Week Num",
    yaxis_title="Points Scored",
    legend_title="Team",
)
fig.update_yaxes(showgrid=False)
st.plotly_chart(fig)


def power_rankings(league, max_week):
    dict_1=dict()
    for i in range(max_week):
      power_rankings = league.power_rankings(i)
      
      for ranking,team in power_rankings:
        dict_1.setdefault(team, []).append(ranking)
    return dict_1

power_ranks = power_rankings(league, max_week)
df_pr = pd.DataFrame.from_dict(power_ranks)
df_pr.index = df_pr.index+1
fig_pr = px.line(df_pr)
fig_pr.update_layout(
    title="Week by Week Power Ranking",
    xaxis_title="Week Num",
    yaxis_title="Power Ranking",
    legend_title="Team",
)
fig_pr.update_yaxes(showgrid=False)
fig_pr.update_yaxes(autorange="reversed")
st.plotly_chart(fig_pr)