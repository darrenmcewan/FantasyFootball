from espn_api.football import League
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import streamlit as st

year = 2023
league = League(league_id=st.secrets["league_id"], year=year, espn_s2=st.secrets["s2"], swid=st.secrets["swid"])

df = pd.DataFrame(columns=['NAME', 'PLAYERID', 'POSRANK', 'ACQUISITIONTYPE', 'PROTEAM', 'ONTEAMID', 'POSITION', 'INJURYSTATUS', 'INJURED', 'TOTAL_POINTS', 'PROJECTED_TOTAL_POINTS', 'PERCENT_OWNED', 'PERCENT_STARTED'])

for team in league.teams:
    for player in team.roster:
        df = pd.concat([df, pd.DataFrame({'NAME': [player.name], 'PLAYERID': [player.playerId], 'POSRANK': [player.posRank], 'ACQUISITIONTYPE': [player.acquisitionType], 'PROTEAM': [player.proTeam], 'ONTEAMID': [player.onTeamId], 'POSITION': [player.position], 'INJURYSTATUS': [player.injuryStatus], 'INJURED': [player.injured], 'TOTAL_POINTS': [player.total_points], 'PROJECTED_TOTAL_POINTS': [player.projected_total_points], 'PERCENT_OWNED': [player.percent_owned], 'PERCENT_STARTED': [player.percent_started]})], ignore_index=True)



conn = snowflake.connector.connect(
    user=st.secrets["user"],
    password=st.secrets["password"],
    account=st.secrets["account"],
    warehouse=st.secrets["warehouse"],
    database=st.secrets["database"],
    schema=st.secrets["schema"]
)

cursor = conn.cursor()

cursor.execute("TRUNCATE TABLE FANTASYFOOTBALL.GRIDDYS_HEROS_23.PLAYERS")
success, nchunks, nrows, _ = write_pandas(conn, df, 'PLAYERS')


