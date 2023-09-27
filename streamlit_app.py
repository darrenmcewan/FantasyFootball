from espn_api.football import League
import pandas as pd
import numpy as np
import requests
import streamlit as st
from collections import defaultdict
import plotly.express as px
from statistics import variance
import re
from datetime import datetime
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

conn = snowflake.connector.connect(
    user=st.secrets["user"],
    password=st.secrets["password"],
    account=st.secrets["account"],
    warehouse=st.secrets["warehouse"],
    database=st.secrets["database"],
    schema=st.secrets["schema"]
)
cursor = conn.cursor()

@st.cache_data
def get_data(_cursor):
    players = cursor.execute("select * from players;").fetch_pandas_all()
    games = cursor.execute("select * from games;").fetch_pandas_all()
    trophies = cursor.execute("select * from trophies;").fetch_pandas_all()
    activity = cursor.execute("select * from activity;").fetch_pandas_all()
    rosters = cursor.execute("select * from rosters;").fetch_pandas_all()
    teams = cursor.execute("select * from teams;").fetch_pandas_all()
    return players, games, trophies, activity, rosters, teams


@st.cache_data
def team_scores(_league, week):
    teams = defaultdict()
    for team in league.teams:
        teams[team.team_name] = team.scores[:week]
    return dict(teams)

@st.cache_data
def power_rankings(_league, week):
    dict_1 = dict()
    for i in range(week):
        power_rankings = league.power_rankings(i)
        for ranking, team in power_rankings:
            dict_1.setdefault(team, []).append(ranking)
    return dict_1


def melt(df, col_vals, key, value):
    assert type(df) is pd.DataFrame
    keep_vars = df.columns.difference(col_vals)
    melted_sections = []
    for c in col_vals:
        melted_c = df[keep_vars].copy()
        melted_c[key] = c
        melted_c[value] = df[c]
        melted_sections.append(melted_c)
    melted = pd.concat(melted_sections)

    return melted

year = 2023

league = League(league_id=st.secrets["league_id"], year=year, espn_s2=st.secrets["s2"], swid=st.secrets["swid"])
players, games, trophies, activity, rosters, teams = get_data(cursor)

best_matchup = 100
ind = 0
for i, match in enumerate(league.scoreboard()):
    matchupVar = variance([match.home_team.standing, match.away_team.standing])
    if matchupVar < best_matchup:
        best_matchup = matchupVar
        ind = i

matchup_week = league.scoreboard()[ind]

st.title("Fantasy Football Dashboard")
st.subheader(f"{league.year} Season Overview")
st.markdown(f'### Current NFL Week: {league.current_week}', unsafe_allow_html=False)
st.markdown(
    f'#### This weeks matchup of the week is {matchup_week.home_team.team_name} ({matchup_week.home_team.standing}) vs {matchup_week.away_team.team_name} ({matchup_week.away_team.standing})')
projected_winner = league.box_scores()[ind].home_projected > league.box_scores()[ind].away_projected
if projected_winner:
    st.markdown(f"{league.box_scores()[ind].home_team.team_name} is expected to win **{league.box_scores()[ind].home_projected}** - {league.box_scores()[ind].away_projected}")
else:
    st.markdown(f" {league.box_scores()[ind].away_team.team_name} is expected to win **{league.box_scores()[ind].away_projected}** - {league.box_scores()[ind].home_projected}")


with st.sidebar:
    max_week = league.current_week
    selected_matchup = st.selectbox("Select Week", range(1, max_week), index=0)

    st.markdown(f"# Trophies of Week {selected_matchup}")
    high_score = trophies[(trophies['WEEK_NUM'] == selected_matchup) & (trophies['TROPHY_NAME'] == 'Highest Score')][['TEAM_NAME', 'NOTE']]
    low_score = trophies[(trophies['WEEK_NUM'] == selected_matchup) & (trophies['TROPHY_NAME'] == 'Lowest Score')][['TEAM_NAME', 'NOTE']]
    blow_out = trophies[(trophies['WEEK_NUM'] == selected_matchup) & (trophies['TROPHY_NAME'] == 'Biggest Blowout')][['TEAM_NAME', 'NOTE']]
    close_win = trophies[(trophies['WEEK_NUM'] == selected_matchup) & (trophies['TROPHY_NAME'] == 'Closest Win')][['TEAM_NAME', 'NOTE']]
    #lucky_win = trophies[(trophies['WEEK_NUM'] == 3) & (trophies['TROPHY_NAME'] == 'Highest Score')][['TEAM_NAME', 'NOTE']]
    #unlucky_loss = trophies[(trophies['WEEK_NUM'] == 3) & (trophies['TROPHY_NAME'] == 'Highest Score')][['TEAM_NAME', 'NOTE']]
    overachiever = trophies[(trophies['WEEK_NUM'] == selected_matchup) & (trophies['TROPHY_NAME'] == 'Overachiever')][['TEAM_NAME', 'NOTE']]
    underachiever = trophies[(trophies['WEEK_NUM'] == selected_matchup) & (trophies['TROPHY_NAME'] == 'Underachiever')][['TEAM_NAME', 'NOTE']]
    best_manager = trophies[(trophies['WEEK_NUM'] == selected_matchup) & (trophies['TROPHY_NAME'] == 'Best Manager')][['TEAM_NAME', 'NOTE']]
    worst_manager = trophies[(trophies['WEEK_NUM'] == selected_matchup) & (trophies['TROPHY_NAME'] == 'Worst Manager')][['TEAM_NAME', 'NOTE']]


    st.markdown(f"### 👑 High Score 👑\n {high_score['TEAM_NAME'].values[0]} with **{high_score['NOTE'].values[0]}** points")
    st.markdown(f"### 💩 Low Score 💩\n {low_score['TEAM_NAME'].values[0]} with **{low_score['NOTE'].values[0]}** points")
    st.markdown(f"### 🤯 Blowout 🤯 \n {blow_out['TEAM_NAME'].values[0]} had the laregest spread with {blow_out['TEAM_NAME'].values[0]} points")
    st.markdown(f"### 😅 Close Win 😅 \n The closest spread was {close_win['TEAM_NAME'].values[0]} with {close_win['TEAM_NAME'].values[0]} points!")
    st.markdown(f"### 🍀 Lucky Win 🍀 \n {high_score['TEAM_NAME'].values[0]}")
    st.markdown(f"### 🥺 Unlucky Loss 🥺 \n {high_score['TEAM_NAME'].values[0]}")
    st.markdown(f"### 📈 Overachiever 📈 \n {overachiever['TEAM_NAME'].values[0]} was {overachiever['TEAM_NAME'].values[0]} points over their projected score")
    st.markdown(f"### 📉 Underachiever 📉 \n {underachiever['TEAM_NAME'].values[0]} was {underachiever['TEAM_NAME'].values[0]} points under their projected score")
    st.markdown(f"### 🤖 Best Manager 🤖 \n {best_manager['TEAM_NAME'].values[0]} had the most optimal lineup - only leaving {best_manager['TEAM_NAME'].values[0]} points")
    st.markdown(f"### 🤡 Worst Manager 🤡 \n {worst_manager['TEAM_NAME'].values[0]} had the least optimal lineup - leaving {worst_manager['TEAM_NAME'].values[0]} points")


stats, free_agents, recent_activity = st.tabs(["Stats", "Free Agents", "Recent Activity"])

with stats:
    week = st.slider("Select NFL Week to view", 0, max_week, max_week)

    scores = team_scores(league, week)
    df = pd.DataFrame.from_dict(scores)
    df.index = df.index + 1

    fig = px.line(df)
    fig.update_layout(
        title="Scores Through the Weeks",
        xaxis_title="Week Num",
        yaxis_title="Points Scored",
        legend_title="Team",
    )
    fig.update_yaxes(showgrid=False)
    st.plotly_chart(fig)

    ##power ranking
    power_ranks = power_rankings(league, week)
    df_pr = pd.DataFrame.from_dict(power_ranks)
    df_pr.iloc[:, 0:] = df_pr.iloc[:, 0:].astype(str).astype(float)
    df_pr.index = df_pr.index + 1
    df_pr.reset_index(inplace=True)
    df_pr = df_pr.rename(columns={'index': 'Week'})

    melted = melt(df_pr, df_pr.iloc[:, 1:], key='Team', value='Power Ranking')
    melted_df = melted[['Week', 'Team', 'Power Ranking']]

    fig_pr = px.line(melted_df, x='Week', y='Power Ranking', color='Team')
    fig_pr.update_layout(
        title="Week by Week Power Rankings",
        xaxis_title="Week Num",
        yaxis_title="Power Ranking",
        legend_title="Team",
    )
    fig_pr.update_yaxes(showgrid=False)
    st.plotly_chart(fig_pr)


with free_agents:

    colnames = ['Player', 'Percent_owned', 'percent_started', 'projected_points', 'position rank', 'position',
                'current week opponent', 'opp rank']
    positions = ['QB', 'WR', 'RB', 'TE', 'K']

    free_agents = list()
    st.markdown(f"### Week {max_week} Free Agents")
    selected_positions = st.multiselect("Select Free Agent Position", positions, default='QB')

    for i in selected_positions:
        for free_agent in league.free_agents(7, 50, position=i):
            free_agents.append((free_agent.name, free_agent.percent_owned, free_agent.percent_started,
                                free_agent.projected_points, free_agent.posRank, free_agent.position,
                                free_agent.pro_opponent, free_agent.pro_pos_rank))

    df = pd.DataFrame(free_agents, columns=colnames)
    st.dataframe(df)

with recent_activity:
    if league.recent_activity() is None:
        st.markdown("No recent activity")
    else:
        data = league.recent_activity()
        for activity in data:
            date = activity.date
            epoch_time_seconds = date / 1000
            datetime_obj = datetime.fromtimestamp(epoch_time_seconds)
            formatted_date = datetime_obj.strftime('%m/%d')
            st.write(f"### {formatted_date}")
            actions = activity.actions
            for i in range(len(actions)):
                st.write(f"{actions[i][0].team_name} {actions[i][1]} {actions[i][2].name}")


