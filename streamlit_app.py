from espn_api.football import League
import pandas as pd
import numpy as np
import requests
import streamlit as st
from collections import defaultdict

league_id = 115999423
year = 2022

league = League(league_id, year)

st.title("Sunnyvale Ballers")
st.subheader(f"{league.year} Season")

max_week = league.current_week
week = st.slider("Select NFL Week to view", 1,maxWeek, maxWeek)

def team_scores(league, max_week):
    teams = defaultdict()
    for team in league.teams:
            teams[team.team_name] = team.scores[:max_week-1]
    return dict(teams)

scores = team_scores(league, max_week)

df = pd.DataFrame.from_dict(scores)
st.line_chart(df)


