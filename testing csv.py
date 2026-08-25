import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

df = pd.read_csv("2026_LoL_esports_match_data_from_OraclesElixir.csv")
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

team_df_clean['date'] = pd.to_datetime(team_df_clean['date'], utc=True)
today = pd.Timestamp.now(tz='UTC')
team_df_clean['days_ago'] = (today - team_df_clean['date']).dt.days
team_df_clean = team_df_clean.drop(columns=['date'])

team_list = sorted(team_df_clean['teamname'].unique())

print(team_list)