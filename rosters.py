from espn_api.football import League
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import streamlit as st

year = 2023
league = League(league_id=st.secrets["league_id"], year=year, espn_s2=st.secrets["s2"], swid=st.secrets["swid"])

df = pd.DataFrame(columns=['WEEK_NUM', 'TEAM_ID', 'PLAYER_NAME', 'PLAYER_ID', 'PROJECTED_POINTS', 'ACTUAL_POINTS', 'PLAYER_POSITION', 'WEEK_POSITION', 'STARTER'])

for i in range(1,league.nfl_week+1):
    for box_score in league.box_scores(i):
        for player in box_score.home_lineup:
            df = pd.concat([df, pd.DataFrame({'WEEK_NUM': [i], 'TEAM_ID': [box_score.home_team.team_id], 'PLAYER_NAME': [player.name], 'PLAYER_ID': [player.playerId], 'PROJECTED_POINTS': [player.projected_points], 'ACTUAL_POINTS': [player.points], 'PLAYER_POSITION': [player.position], 'WEEK_POSITION': [player.slot_position], 'STARTER': [player.slot_position != 'BE']})], ignore_index=True)
        for player in box_score.away_lineup:
            df = pd.concat([df, pd.DataFrame({'WEEK_NUM': [i], 'TEAM_ID': [box_score.away_team.team_id], 'PLAYER_NAME': [player.name], 'PLAYER_ID': [player.playerId], 'PROJECTED_POINTS': [player.projected_points], 'ACTUAL_POINTS': [player.points], 'PLAYER_POSITION': [player.position], 'WEEK_POSITION': [player.slot_position], 'STARTER': [player.slot_position != 'BE']})], ignore_index=True)

conn = snowflake.connector.connect(
    user='dmcewan',
    password='hde7UEM@ecu2dnu1tvz',
    account='wkb52928.prod3.us-west-2.aws',
    warehouse='ff_etl_wh',
    database='FANTASYFOOTBALL',
    schema='griddys_heros_23'
)

cursor = conn.cursor()

cursor.execute("TRUNCATE TABLE FANTASYFOOTBALL.GRIDDYS_HEROS_23.ROSTERS")
success, nchunks, nrows, _ = write_pandas(conn, df, 'ROSTERS')