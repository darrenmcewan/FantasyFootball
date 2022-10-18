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
fig = px.line(df)
st.plotly_chart(fig)


