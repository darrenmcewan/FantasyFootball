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


class Trophies:
    def __init__(self, league, week):
        self.league = league
        self.week = week
        pass

    def high_score(self):
        return cursor.execute(f"select team_name, note from trophies where week_num = {self.week} and trophy_name = 'Highest Score'").fetchone()
    

    def low_score(self):
        return cursor.execute(f"select team_name, note from trophies where week_num = {self.week} and trophy_name = 'Lowest Score'").fetchone()

    def blow_out(self):
        return cursor.execute(f"select team_name, note from trophies where week_num = {self.week} and trophy_name = 'Biggest Blowout'").fetchone()


    def close_win(self):
        return cursor.execute(f"select team_name, note from trophies where week_num = {self.week} and trophy_name = 'Closest Win'").fetchone()


    def lucky_win(self):
        league = self.league
        league_scores = {league.teams[i].team_name: league.teams[i].scores[0] for i in range(len(league.teams))}
        records = {}
        for team, score in league_scores.items():
            wins = 0
            losses = 0

            for opponent, opponent_score in league_scores.items():
                if team != opponent:
                    if score > opponent_score:
                        wins += 1
                    else:
                        losses += 1

            total_games = wins + losses
            win_percentage = (wins / total_games) * 100
            loss_percentage = (losses / total_games) * 100
            matchups = league.scoreboard(week=1)

            # find out if they won their game this week
            for matchup in matchups:
                if matchup.home_team.team_name == team:
                    if matchup.home_score > matchup.away_score:
                        records[team] = {
                            "W-L Record": f"{wins}-{losses}",
                            "Win Percentage": win_percentage,
                            "Loss Percentage": loss_percentage,
                            "Outcome": 1
                        }
                    else:
                        records[team] = {
                            "W-L Record": f"{wins}-{losses}",
                            "Win Percentage": win_percentage,
                            "Loss Percentage": loss_percentage,
                            "Outcome": 0
                        }
                elif matchup.away_team.team_name == team:
                    if matchup.away_score > matchup.home_score:
                        records[team] = {
                            "W-L Record": f"{wins}-{losses}",
                            "Win Percentage": win_percentage,
                            "Loss Percentage": loss_percentage,
                            "Outcome": 1
                        }
                    else:
                        records[team] = {
                            "W-L Record": f"{wins}-{losses}",
                            "Win Percentage": win_percentage,
                            "Loss Percentage": loss_percentage,
                            "Outcome": 0
                        }

        lucky_victory = {
            "Team": "",
            "W-L Record": "",
            "Win Percentage": 100,
            "Loss Percentage": 0,
            "Outcome": 0
        }

        for team, record in records.items():
            if record["Outcome"] == 1 and record["Win Percentage"] < lucky_victory["Win Percentage"]:
                lucky_victory["Team"] = team
                lucky_victory["W-L Record"] = record["W-L Record"]
                lucky_victory["Win Percentage"] = record["Win Percentage"]
                lucky_victory["Loss Percentage"] = record["Loss Percentage"]
                lucky_victory["Outcome"] = record["Outcome"]

        return f"{lucky_victory['Team']} went **{lucky_victory['W-L Record']}** against the league but still caught the dub"

    def unlucky_loss(self):
        league = self.league
        league_scores = {league.teams[i].team_name: league.teams[i].scores[0] for i in range(len(league.teams))}
        records = {}
        for team, score in league_scores.items():
            wins = 0
            losses = 0

            for opponent, opponent_score in league_scores.items():
                if team != opponent:
                    if score > opponent_score:
                        wins += 1
                    else:
                        losses += 1

            total_games = wins + losses
            win_percentage = (wins / total_games) * 100
            loss_percentage = (losses / total_games) * 100
            matchups = league.scoreboard(week=1)

            # find out if they won their game this week
            for matchup in matchups:
                if matchup.home_team.team_name == team:
                    if matchup.home_score > matchup.away_score:
                        records[team] = {
                            "W-L Record": f"{wins}-{losses}",
                            "Win Percentage": win_percentage,
                            "Loss Percentage": loss_percentage,
                            "Outcome": 1
                        }
                    else:
                        records[team] = {
                            "W-L Record": f"{wins}-{losses}",
                            "Win Percentage": win_percentage,
                            "Loss Percentage": loss_percentage,
                            "Outcome": 0
                        }
                elif matchup.away_team.team_name == team:
                    if matchup.away_score > matchup.home_score:
                        records[team] = {
                            "W-L Record": f"{wins}-{losses}",
                            "Win Percentage": win_percentage,
                            "Loss Percentage": loss_percentage,
                            "Outcome": 1
                        }
                    else:
                        records[team] = {
                            "W-L Record": f"{wins}-{losses}",
                            "Win Percentage": win_percentage,
                            "Loss Percentage": loss_percentage,
                            "Outcome": 0
                        }
        unlucky_loss = {
            "Team": "",
            "W-L Record": "",
            "Win Percentage": 0,
            "Loss Percentage": 100,
            "Outcome": 1
        }

        for team, record in records.items():
            if record["Outcome"] == 0 and record["Win Percentage"] > unlucky_loss["Win Percentage"]:
                unlucky_loss["Team"] = team
                unlucky_loss["W-L Record"] = record["W-L Record"]
                unlucky_loss["Win Percentage"] = record["Win Percentage"]
                unlucky_loss["Loss Percentage"] = record["Loss Percentage"]
                unlucky_loss["Outcome"] = record["Outcome"]

        return f"{unlucky_loss['Team']} went **{unlucky_loss['W-L Record']}** against the league but went down with the L"



    def overachiever(self):
        return cursor.execute(f"select team_name, note from trophies where week_num = {self.week} and trophy_name = 'Overachiever'").fetchone()


    def underachiever(self):
        return cursor.execute(f"select team_name, note from trophies where week_num = {self.week} and trophy_name = 'Underachiever'").fetchone()


    def best_manager(self):
        return cursor.execute(f"select team_name, note from trophies where week_num = {self.week} and trophy_name = 'Best Manager'").fetchone()


    def worst_manager(self):
        return cursor.execute(f"select team_name, note from trophies where week_num = {self.week} and trophy_name = 'Worst Manager'").fetchone()



def team_scores(league, week):
    teams = defaultdict()
    for team in league.teams:
        teams[team.team_name] = team.scores[:week]
    return dict(teams)


def power_rankings(league, week):
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
    st.markdown(
        f"{league.box_scores()[ind].home_team.team_name} is expected to win **{league.box_scores()[ind].home_projected}** - {league.box_scores()[ind].away_projected}")
else:
    st.markdown(
        f" {league.box_scores()[ind].away_team.team_name} is expected to win **{league.box_scores()[ind].away_projected}** - {league.box_scores()[ind].home_projected}")


with st.sidebar:
    max_week = league.current_week
    week = st.slider("Select NFL Week to view", 0, max_week, max_week)
    selected_matchup = st.selectbox("Select Week", range(1, max_week), index=0)

    st.markdown(f"# Trophies of Week {selected_matchup}")
    Trophies = Trophies(league, selected_matchup)
    st.markdown(f"### 👑 High Score 👑\n {Trophies.high_score()[0]} with **{round(float(Trophies.high_score()[1]),2)}** points")
    st.markdown(f"### 💩 Low Score 💩\n {Trophies.low_score()[0]} with **{round(float(Trophies.low_score()[1]),2)}** points")
    st.markdown(f"### 🤯 Blowout 🤯 \n {Trophies.blow_out()[0]} had the laregest spread with {round(float(Trophies.blow_out()[1]),2)} points")
    st.markdown(f"### 😅 Close Win 😅 \n The closest spread was {Trophies.close_win()[0]} with {round(float(Trophies.close_win()[1]),2)} points!")
    st.markdown(f"### 🍀 Lucky Win 🍀 \n {Trophies.lucky_win()}")
    st.markdown(f"### 🥺 Unlucky Loss 🥺 \n {Trophies.unlucky_loss()}")
    st.markdown(f"### 📈 Overachiever 📈 \n {Trophies.overachiever()[0]} was {round(float(Trophies.overachiever()[1]),2)} points over their projected score")
    st.markdown(f"### 📉 Underachiever 📉 \n {Trophies.underachiever()[0]} was {round(float(Trophies.underachiever()[1]),2)} points under their projected score")
    st.markdown(f"### 🤖 Best Manager 🤖 \n {Trophies.best_manager()[0]} had the most optimal lineup - only leaving {round(float(Trophies.best_manager()[1]),2)} points")
    st.markdown(f"### 🤡 Worst Manager 🤡 \n {Trophies.worst_manager()[0]} had the least optimal lineup - leaving {round(float(Trophies.worst_manager()[1]),2)} points")


stats, free_agents, recent_activity = st.tabs(["Stats", "Free Agents", "Recent Activity"])

with stats:

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


