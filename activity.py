from espn_api.football import League
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from datetime import datetime
import streamlit as st

year = 2023
league = League(league_id=st.secrets["league_id"], year=year, espn_s2=st.secrets["s2"], swid=st.secrets["swid"])


df = pd.DataFrame(columns=['TEAM_NAME', 'PLAYER_NAME', 'ACTION_TYPE', 'PLAYER_SEASON_POINTS', 'ACTIVITY_DATE'])

data = league.recent_activity()
for activity in data:
    datetime_obj = datetime.fromtimestamp(activity.date/1000)
    actions = activity.actions
    for i in range(len(actions)):
        team_name = actions[i][0].team_name
        action_type = actions[i][1]
        player_name = actions[i][2].name
        player_points = league.player_info(player_name).total_points
        df = pd.concat([df, pd.DataFrame({'TEAM_NAME': [team_name], 'PLAYER_NAME': [player_name], 'ACTION_TYPE': [action_type], 'PLAYER_SEASON_POINTS': [player_points], 'ACTIVITY_DATE': [datetime_obj]})], ignore_index=True)



conn = snowflake.connector.connect(
    user=st.secrets["user"],
    password=st.secrets["password"],
    account=st.secrets["account"],
    warehouse=st.secrets["warehouse"],
    database=st.secrets["database"],
    schema=st.secrets["schema"]
)

cursor = conn.cursor()

cursor.execute("TRUNCATE TABLE FANTASYFOOTBALL.GRIDDYS_HEROS_23.ACTIVITY")
success, nchunks, nrows, _ = write_pandas(conn, df, 'ACTIVITY')
