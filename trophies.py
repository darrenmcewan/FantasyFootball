from espn_api.football import League
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import streamlit as st

conn = snowflake.connector.connect(
    user=st.secrets["user"],
    password=st.secrets["password"],
    account=st.secrets["account"],
    warehouse=st.secrets["warehouse"],
    database=st.secrets["database"],
    schema=st.secrets["schema"]
)

cursor = conn.cursor()
year = 2023
league = League(league_id=st.secrets["league_id"], year=year, espn_s2=st.secrets["s2"], swid=st.secrets["swid"])


df = pd.DataFrame(columns=['WEEK_NUM','TEAM_ID','POINTS_LEFT'])

cursor.execute("TRUNCATE TABLE FANTASYFOOTBALL.GRIDDYS_HEROS_23.TROPHIES")

for i in range(1, league.nfl_week):
    max_score = cursor.execute(f'''
        select team_name, max(team_score) as highest_score from GAMES
        where week_num = {i}
        group by 1
        order by 2 desc
        limit 1;''').fetchone()

    cursor.execute('''insert into TROPHIES (week_num, team_name, trophy_name, note) values (%s, %s, %s, %s)''',
                   (i, max_score[0], 'Highest Score', max_score[1]))

    min_score = cursor.execute(f'''
        select team_name, max(team_score) as highest_score from GAMES
        where week_num = {i}
        group by 1
        order by 2 asc
        limit 1;''').fetchone()

    cursor.execute('''insert into TROPHIES (week_num, team_name, trophy_name, note) values (%s, %s, %s, %s)''',
                     (i, min_score[0], 'Lowest Score', min_score[1]))

    blowout = cursor.execute(f'''
    select team_name, (team_score - opp_score) as diff from games
    where week_num = {i}
    order by 2 desc
    limit 1;''').fetchone()

    cursor.execute('''insert into TROPHIES (week_num, team_name, trophy_name, note) values (%s, %s, %s, %s)''',
                        (i, blowout[0], 'Biggest Blowout', blowout[1]))

    closest = cursor.execute(f'''select team_name, abs(team_score - opp_score) as diff from games
    where week_num = {i} and game_won = True
    order by 2 asc
    limit 1;''').fetchone()

    cursor.execute('''insert into TROPHIES (week_num, team_name, trophy_name, note) values (%s, %s, %s, %s)''',
                        (i, closest[0], 'Closest Win', closest[1]))


    overachiever = cursor.execute(f'''select team_name, (team_projected - team_score) as diff from games
    where week_num = {i}
    order by 2 desc
    limit 1;''').fetchone()

    cursor.execute('''insert into TROPHIES (week_num, team_name, trophy_name, note) values (%s, %s, %s, %s)''',
                        (i, overachiever[0], 'Overachiever', overachiever[1]))

    underachiever = cursor.execute(f'''select team_name, (team_score - team_projected) as diff from games
    where week_num = {i}
    order by 2 asc
    limit 1;''').fetchone()

    cursor.execute('''insert into TROPHIES (week_num, team_name, trophy_name, note) values (%s, %s, %s, %s)''',
                        (i, underachiever[0], 'Underachiever', underachiever[1]))


    ## Best and worst manager
    for team in league.teams:
        sql = f'''
        SELECT r.player_position, 
        CASE 
            WHEN COALESCE(b.max_points, 0) - MIN(r.actual_points) < 0 THEN 0
            ELSE COALESCE(b.max_points, 0) - MIN(r.actual_points)
        END AS difference 
        FROM rosters r
        LEFT JOIN (
            SELECT player_position, MAX(actual_points) AS max_points 
            FROM rosters
            WHERE week_position = 'BE' AND team_id = {team.team_id} AND week_num = {i}
            GROUP BY player_position
        ) b ON r.player_position = b.player_position
        WHERE r.week_position NOT IN ('BE', 'IR') AND r.team_id = {team.team_id} AND r.week_num = {i}
        GROUP BY r.player_position, b.max_points;
        '''
        output = cursor.execute(sql).fetchall()
        df = pd.concat([df, pd.DataFrame({'WEEK_NUM': [i], 'TEAM_ID': [team.team_id], 'POINTS_LEFT': [sum([x[1] for x in output])]} )], ignore_index=True)


    min_points = df[df['WEEK_NUM'] == i]['POINTS_LEFT'].min()
    team_id = df[df['POINTS_LEFT'] == min_points]['TEAM_ID'].values[0]
    min_team_name = cursor.execute(f'''select team_name from teams where team_id = {team_id}''').fetchone()[0]

    cursor.execute('''insert into TROPHIES (week_num, team_name, trophy_name, note) values (%s, %s, %s, %s)''',
                   (i, min_team_name, 'Best Manager', min_points))

    max_points = df[df['WEEK_NUM'] == i]['POINTS_LEFT'].max()
    team_id = df[df['POINTS_LEFT'] == max_points]['TEAM_ID'].values[0]
    max_team_name = cursor.execute(f'''select team_name from teams where team_id = {team_id}''').fetchone()[0]

    cursor.execute('''insert into TROPHIES (week_num, team_name, trophy_name, note) values (%s, %s, %s, %s)''',
               (i, max_team_name, 'Worst Manager', max_points))