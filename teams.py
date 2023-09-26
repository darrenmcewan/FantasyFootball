from espn_api.football import League
import pandas as pd
import snowflake.connector
import streamlit as st
from snowflake.connector.pandas_tools import write_pandas

year = 2023
league = League(league_id=st.secrets["league_id"], year=year, espn_s2=st.secrets["s2"], swid=st.secrets["swid"])

df = pd.DataFrame(columns=['TEAM_ID', 'TEAM_ABBREV', 'TEAM_NAME','DIVISION_ID', 'DIVISION_NAME', 'WINS', 'LOSSES', 'TIES', 'POINTS_FOR','POINTS_AGAINST','DROPS','TRADES','OWNER','STREAK_TYPE','STREAK_LENGTH','STANDING','FINAL_STANDING','DRAFT_PROJECTED_RANK', 'LOGO_URL'])
for team in league.teams:
    df = pd.concat([df,pd.DataFrame({'TEAM_ID': [team.team_id], 'TEAM_ABBREV': [team.team_abbrev], 'TEAM_NAME': [team.team_name], 'DIVISION_ID': [team.division_id], 'DIVISION_NAME': [team.division_name], 'WINS': [team.wins], 'LOSSES': [team.losses], 'TIES': [team.ties], 'POINTS_FOR': [team.points_for], 'POINTS_AGAINST': [team.points_against], 'DROPS': [team.drops], 'TRADES': [team.trades], 'OWNER': [team.owner], 'STREAK_TYPE': [team.streak_type], 'STREAK_LENGTH': [team.streak_length], 'STANDING': [team.standing], 'FINAL_STANDING': [team.final_standing], 'DRAFT_PROJECTED_RANK': [team.draft_projected_rank], 'LOGO_URL': [team.logo_url]})], ignore_index=True)

conn = snowflake.connector.connect(
    user=st.secrets["user"],
    password=st.secrets["password"],
    account=st.secrets["account"],
    warehouse=st.secrets["warehouse"],
    database=st.secrets["database"],
    schema=st.secrets["schema"]
)
cursor = conn.cursor()

cursor.execute("TRUNCATE TABLE FANTASYFOOTBALL.GRIDDYS_HEROS_23.TEAMS")
success, nchunks, nrows, _ = write_pandas(conn, df, 'TEAMS')
