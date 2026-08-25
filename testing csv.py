import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

df = pd.read_csv("2026_LoL_esports_match_data_from_OraclesElixir.csv", low_memory=False)
team_df = df[df['position'] == 'team'].copy()

columns_to_keep = [
    'gameid',
    'date',
    'teamname',
    'gamelength',
    'result',
    'kills',
    'deaths',
    'dragons',
    'heralds',
    'void_grubs',
    'barons',
    'towers',
    'firsttower',
    'turretplates',
    'dpm',
    'wpm',
    'golddiffat15',
    'killsat15',
    'csdiffat15'

]
team_df_clean = team_df[columns_to_keep].copy()
team_df['Vs'] = team_df.groupby('gameid')['teamname'].transform(lambda x: x.iloc[::-1].values)

team_df = team_df.rename(columns={
    'teamname': 'Team',
    'result': 'Result'
})

team_df_clean['date'] = pd.to_datetime(team_df_clean['date'], utc=True)
today = pd.Timestamp.now(tz='UTC')
team_df_clean['days_ago'] = (today - team_df_clean['date']).dt.days
team_df_clean = team_df_clean.drop(columns=['date'])

team_df.to_csv('teams_data.csv', index=False)
