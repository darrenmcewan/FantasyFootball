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

class Trophies:
    def __init__(self, league, week):
        self.league = league
        self.week = week
        pass

    def high_score(self):
        high_score = self.league.top_scorer()
        pattern = r'\(([^)]+)\)'
        match = re.search(pattern, str(high_score))
        extracted_text = match.group(1)
        return extracted_text

    def low_score(self):
        low_score = self.league.least_scorer()
        pattern = r'\(([^)]+)\)'
        match = re.search(pattern, str(low_score))
        extracted_text = match.group(1)
        return extracted_text


    def blow_out(self):
        matchups = self.league.scoreboard(week=self.week)
        biggest_score_diff = 0
        for matchup in matchups:
            score_diff = abs(matchup.home_score - matchup.away_score)
            if score_diff > biggest_score_diff:
                biggest_score_diff = score_diff
                biggest_score_diff_matchup = matchup

        if biggest_score_diff_matchup.home_score > biggest_score_diff_matchup.away_score:
            output = f"{biggest_score_diff_matchup.home_team.team_name} won by **{round(biggest_score_diff, 2)}** points!"
        else:
            output = f"{biggest_score_diff_matchup.away_team.team_name} won by **{round(biggest_score_diff, 2)}** points!"
        return output


    def close_win(self):
        matchups = self.league.scoreboard(week=self.week)
        smallest_score_diff = 1000
        for matchup in matchups:
            score_diff = abs(matchup.home_score - matchup.away_score)
            if score_diff < smallest_score_diff:
                smallest_score_diff = score_diff
                smallest_score_diff_matchup = matchup

        if smallest_score_diff_matchup.home_score > smallest_score_diff_matchup.away_score:
            output = f"{smallest_score_diff_matchup.home_team.team_name} narrowly won by **{round(smallest_score_diff, 2)}** points!"
        else:
            output = f"{smallest_score_diff_matchup.away_team.team_name} narrowly won by **{round(smallest_score_diff, 2)}** points!"
        return output
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
        overachievers = {"team": "", "difference": 0}
        for matchup in league.box_scores(week=1):
            if matchup.home_projected - matchup.home_score < overachievers['difference']:
                overachievers["team"] = matchup.home_team.team_name
                overachievers["difference"] = matchup.home_projected - matchup.home_score
            if matchup.away_projected - matchup.away_score < overachievers['difference']:
                overachievers["team"] = matchup.away_team.team_name
                overachievers["difference"] = matchup.away_projected - matchup.away_score
        return f"{overachievers['team']} was **{abs(round(overachievers['difference'], 2))}** points over their projection"

    def underachiever(self):
        league = self.league
        underachievers = {"team": "", "difference": 0}
        for matchup in league.box_scores(week=1):
            if matchup.home_projected - matchup.home_score > underachievers['difference']:
                underachievers["team"] = matchup.home_team.team_name
                underachievers["difference"] = matchup.home_projected - matchup.home_score
            if matchup.away_projected - matchup.away_score > underachievers['difference']:
                underachievers["team"] = matchup.away_team.team_name
                underachievers["difference"] = matchup.away_projected - matchup.away_score
        return f"{underachievers['team']} was **{round(underachievers['difference'], 2)}** points under their projection"

    def best_manager(self):
        pass

    def worst_manager(self):
        pass



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

league_id = 804979303
year = 2023

s2 = "AECrKRgF3ZyvfDcC2AM6K2UqRIc0gjB8gluwpbueZS3iDxR0fqimN2PtIinDV3t0QDi54c0O4rfC5%2F81ICoPNcaEk7x1HydnlvWb6wlwXi06ndzZc0mKD%2BUPZOEhld0F5LsbLMgRSz%2Bbd7IuXxoZk9%2F7NoHzBI6G1Q2m5lKwGz1V2xGyWOqNc9NvkD0QJw8%2FOrVVcETlvoW5LbDCJtQbgRtesdJD396ppalxHmJMExl6geUib2CKenpRQJfIxlARmSG5mbRRXbF5CBPshpwQS2jhkYc8rkZooK%2B8udZTI7%2BQXg%3D%3D"
swid = "{BB1E4E35-4F5B-4919-9BD2-AF0C3F972162}"
league = League(league_id=league_id, year=year, espn_s2=s2, swid=swid)
league.refresh()

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
    st.markdown(f"### 👑 High Score 👑\n {Trophies.high_score()} with **{team_scores(league, selected_matchup)[Trophies.high_score()][selected_matchup-1]}** points")
    st.markdown(f"### 💩 Low Score 💩\n {Trophies.low_score()} with **{team_scores(league, selected_matchup)[Trophies.low_score()][selected_matchup-1]}** points")
    st.markdown(f"### 🤯 Blowout 🤯 \n {Trophies.blow_out()}")
    st.markdown(f"### 😅 Close Win 😅 \n {Trophies.close_win()}")
    st.markdown(f"### 🍀 Lucky Win 🍀 \n {Trophies.lucky_win()}")
    st.markdown(f"### 🥺 Unlucky Loss 🥺 \n {Trophies.unlucky_loss()}")
    st.markdown(f"### 📈 Overachiever 📈 \n {Trophies.overachiever()}")
    st.markdown(f"### 📉 Underachiever 📉 \n {Trophies.underachiever()}")
    st.markdown(f"### 🤖 Best Manager 🤖 \n {Trophies.best_manager()}")
    st.markdown(f"### 🤡 Worst Manager 🤡 \n {Trophies.worst_manager()}")



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


