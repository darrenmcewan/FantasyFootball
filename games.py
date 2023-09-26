from espn_api.football import League
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import streamlit as st

year = 2023
league = League(league_id=st.secrets["league_id"], year=year, espn_s2=st.secrets["s2"], swid=st.secrets["swid"])



df = pd.DataFrame(columns=['WEEK_NUM', 'TEAM_NAME', 'TEAM_SCORE','TEAM_PROJECTED', 'OPP_NAME', 'OPP_SCORE', 'OPP_PROJECTED','GAME_WON','IS_PLAYOFF'])

for i in range(1,league.nfl_week+1):
    for j in league.box_scores(i):
        df = pd.concat([df, pd.DataFrame(
            {'WEEK_NUM': [i], 'TEAM_NAME': [j.home_team.team_name], 'TEAM_SCORE': [j.home_score],
             'TEAM_PROJECTED': [j.home_projected], 'OPP_NAME': [j.away_team.team_name], 'OPP_SCORE': [j.away_score],
             'OPP_PROJECTED': [j.away_projected],
             'GAME_WON': [j.home_score > j.away_score], 'IS_PLAYOFF': [j.is_playoff]})], ignore_index=True)
        df = pd.concat([df, pd.DataFrame(
            {'WEEK_NUM': [i], 'TEAM_NAME': [j.away_team.team_name], 'TEAM_SCORE': [j.away_score],
             'TEAM_PROJECTED': [j.away_projected], 'OPP_NAME': [j.home_team.team_name], 'OPP_SCORE': [j.home_score],
             'OPP_PROJECTED': [j.home_projected],
             'GAME_WON': [j.away_score > j.home_score], 'IS_PLAYOFF': [j.is_playoff]})], ignore_index=True)

conn = snowflake.connector.connect(
    user=st.secrets["user"],
    password=st.secrets["password"],
    account=st.secrets["account"],
    warehouse=st.secrets["warehouse"],
    database=st.secrets["database"],
    schema=st.secrets["schema"]
)

cursor = conn.cursor()

cursor.execute("TRUNCATE TABLE FANTASYFOOTBALL.GRIDDYS_HEROS_23.GAMES")
success, nchunks, nrows, _ = write_pandas(conn, df, 'GAMES')
