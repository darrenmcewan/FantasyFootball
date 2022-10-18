from espn_api.football import League
import pandas as pd
import numpy as np
import requests
import streamlit as st
from collections import defaultdict
import plotly.express as px

def main_page():
    st.markdown("# Main page 🎈")
    st.sidebar.markdown("# Main page 🎈")

def page2():
    st.markdown("# Page 2 ❄️")
    st.sidebar.markdown("# Page 2 ❄️")

def page3():
    st.markdown("# Page 3 🎉")
    st.sidebar.markdown("# Page 3 🎉")

page_names_to_funcs = {
    "Main Page": main_page,
    "Page 2": page2,
    "Page 3": page3,
}

selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()

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


