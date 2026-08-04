import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, roc_auc_score, log_loss


def get_match_history(df, team_a, team_b, N=20):
  team_a_matches = df[df['Team'] == team_a].tail(N)
  team_b_matches = df[df['Team'] == team_b].tail(N)
  stats_cols = ['Kills', 'Gold/sec', 'Towers', 'Dragons',
                  'Kills/15 minute', 'Gold/sec/15 minute',
                  'Towers/15 minute', 'Dragons/15 minute']
  team_a_stats = team_a_matches[stats_cols].mean()
  team_b_stats = team_b_matches[stats_cols].mean()

  diff_features = team_a_stats - team_b_stats

  diff_features.index = [f'{col}_diff' for col in diff_features.index]

  return diff_features


df_al = pd.read_csv('assets/AL_match_history.csv')
df_blg = pd.read_csv('assets/BLG_match_history.csv')
df_EDG = pd.read_csv('assets/EDG_match_history.csv')
df_IG = pd.read_csv('assets/IG_match_history.csv')
df_LGD = pd.read_csv('assets/LGD_match_history.csv')
df_LNG = pd.read_csv('assets/LNG_match_history.csv')
df_NIP = pd.read_csv('assets/NIP_match_history.csv')
df_TES = pd.read_csv('assets/TES_match_history.csv')
df_TT = pd.read_csv('assets/TT_match_history.csv')
df_WBG = pd.read_csv('assets/WBG_match_history.csv')
df_WE = pd.read_csv('assets/WE_match_history.csv')

dfs = [df_al, df_blg, df_EDG, df_IG, df_LGD, df_LNG, df_NIP, df_TES, df_TT, df_WBG, df_WE]
dfs_fixed = []
X_list = []
y_list = []

for df in dfs:
  df_temp = df.copy()
  result_col = [col for col in df_temp.columns if 'Result' in col][0]
  team_name = result_col.replace(' Result', '').strip()
  df_temp['Team'] = team_name
  df_temp['Result'] = df_temp[result_col]
  df_temp = df_temp.drop(columns=[result_col])

  dfs_fixed.append(df_temp)

df_all = pd.concat(dfs_fixed, ignore_index=True)
df_all = df_all.drop(columns=['Score', 'Tournament', 'Week', 'Game'])
df_all = df_all.rename({'Kills.1':'Kills/15 minute', 'Golds.1':'Gold/sec/15 minute', 'Towers.1':'Towers/15 minute', 'Dragons.1':'Dragons/15 minute', 'Golds':'Gold/sec'})
df_all['Result'] = df_all['Result'].map({'WIN':1, 'LOSS':0})
df_all['Side'] = df_all['Side'].map({'Blue':1, 'Red':0})
df_all = df_all.rename(columns={'Kills.1':'Kills/15 minute', 'Golds.1':'Gold/sec/15 minute', 'Towers.1':'Towers/15 minute', 'Dragons.1':'Dragons/15 minute', 'Golds':'Gold/sec'})

for idx, row in df_all.iterrows():
    team_a = row['Team']
    team_b = row['Vs']

    features = get_match_history(df_all, team_a=team_a, team_b=team_b, N=20)
    features.name = f"{team_a}_vs_{team_b}_{idx}"

    if features is not None and not features.isna().any():
        X_list.append(features)
        y_list.append(row['Result'])

X = pd.DataFrame(X_list)
y = pd.Series(y_list, name='Result')
split_idx = int(len(X) * 0.8)
X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

teams = ['AL', 'BLG', 'EDG', 'IG', 'NIP', 'LGD', 'LNG', 'TES', 'TT', 'WBG', 'WE']
teams_enumerated = enumerate(teams)

for i, team in teams_enumerated:
   print(f'{i}.{team} ')
   
idx_a = int(input('Choose first team from above (enter number): '))
team_a = teams[idx_a]
idx_b = int(input('Choose second team from above (enter number): '))
team_b = teams[idx_b]

model_to_use = GradientBoostingClassifier(learning_rate=0.01, max_depth=2, n_estimators=100)
model_to_use.fit(X_train_scaled, y_train)
#i skip gridsearchcv part to save time because i already got parameters i want
f_ab = get_match_history(df_all, team_a=team_a, team_b=team_b, N=20).to_frame().T[X.columns].fillna(0)
f_ba = get_match_history(df_all, team_a=team_b, team_b=team_a, N=20).to_frame().T[X.columns].fillna(0)

prob_a_dir1 = model_to_use.predict_proba(scaler.transform(f_ab))[0][1]
prob_b_dir2 = model_to_use.predict_proba(scaler.transform(f_ba))[0][1]

prob_a = ((prob_a_dir1 + (1 - prob_b_dir2)) / 2) * 100
prob_b = 100 - prob_a

print(f"Calculating match odds for: {team_a} vs {team_b}")
print(f"Win chance for {team_a}: {prob_a:.1f}%")
print(f"Win chance for {team_b}: {prob_b:.1f}%")

