from operator import le
from espn_api.football import League
import pandas as pd
import numpy as np
import requests
import streamlit as st

league_id = 115999423
year = 2022

league = League(league_id, year)

st.text(league.teams)
