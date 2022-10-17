from math import degrees
from msilib import sequence
from operator import le
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

maxWeek = league.current_week
week = st.slider("Select NFL Week to view", 1,maxWeek, maxWeek)

def team_scores(league, max_week):
    teams = defaultdict()
    weeks = [i for i in range(1, max_week+1)] 
    for team in league.teams:
        for week_num in weeks:
            teams[team.team_name][week_num] = team.scores
    return teams


