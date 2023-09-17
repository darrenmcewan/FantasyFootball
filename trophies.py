from espn_api.football import League

league_id = 804979303
year = 2023
s2 = "AECrKRgF3ZyvfDcC2AM6K2UqRIc0gjB8gluwpbueZS3iDxR0fqimN2PtIinDV3t0QDi54c0O4rfC5%2F81ICoPNcaEk7x1HydnlvWb6wlwXi06ndzZc0mKD%2BUPZOEhld0F5LsbLMgRSz%2Bbd7IuXxoZk9%2F7NoHzBI6G1Q2m5lKwGz1V2xGyWOqNc9NvkD0QJw8%2FOrVVcETlvoW5LbDCJtQbgRtesdJD396ppalxHmJMExl6geUib2CKenpRQJfIxlARmSG5mbRRXbF5CBPshpwQS2jhkYc8rkZooK%2B8udZTI7%2BQXg%3D%3D"
swid = "{BB1E4E35-4F5B-4919-9BD2-AF0C3F972162}"
league = League(league_id=league_id, year=year, espn_s2=s2, swid=swid)

matchups = league.scoreboard(week=1)


# find each teams record as if they played every team every week
league_scores = {league.teams[i].team_name: league.teams[i].scores[0] for i in range(len(league.teams))}


underachievers = {"team": "", "difference": 0}
for matchup in league.box_scores(week=1):
    if matchup.home_projected - matchup.home_score > underachievers['difference']:
        underachievers["team"] = matchup.home_team.team_name
        underachievers["difference"] = matchup.home_projected - matchup.home_score
    if matchup.away_projected - matchup.away_score > underachievers['difference']:
        underachievers["team"] = matchup.away_team.team_name
        underachievers["difference"] = matchup.away_projected - matchup.away_score

print(underachievers)

overachievers = {"team": "", "difference": 0}
for matchup in league.box_scores(week=1):
    if matchup.home_projected - matchup.home_score < overachievers['difference']:
        overachievers["team"] = matchup.home_team.team_name
        overachievers["difference"] = matchup.home_projected - matchup.home_score
    if matchup.away_projected - matchup.away_score < overachievers['difference']:
        overachievers["team"] = matchup.away_team.team_name
        overachievers["difference"] = matchup.away_projected - matchup.away_score
print(overachievers)
