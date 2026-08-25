import pandas as pd
import numpy as np
import shap
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, roc_auc_score, log_loss
import os
from data_scraping import get_teams_data

def get_match_history(df, team_a, team_b, current_idx, N=20):
    df_past = df.loc[:current_idx-1] 
    
    team_a_matches = df_past[df_past['Team'] == team_a].tail(N)
    team_b_matches = df_past[df_past['Team'] == team_b].tail(N)
    
    stats_cols = [
        'gamelength', 'dragons', 'heralds', 
        'void_grubs', 'barons', 'firsttower', 
        'turretplates', 'dpm', 'wpm', 'golddiffat15', 
        'killsat15', 'csdiffat15'
    ]
    
    if len(team_a_matches) == 0 or len(team_b_matches) == 0:
        return None

    team_a_stats = team_a_matches[stats_cols].mean()
    team_b_stats = team_b_matches[stats_cols].mean()

    diff_features = team_a_stats - team_b_stats
    diff_features.index = [f'{col}_diff' for col in diff_features.index]

    return diff_features

if os.path.exists('teams_data.csv'):
    df_all = pd.read_csv('teams_data.csv')
else:
    raise FileNotFoundError("Error: file teams_data.csv not found. Start preprocessing first.")
X_list = []
y_list = []
for idx, row in df_all.iterrows():
    team_a = row['Team']
    team_b = row['Vs']

    features = get_match_history(df_all, team_a=team_a, team_b=team_b, current_idx=idx, N=20)

    if features is not None and not features.isna().any():
        features.name = f"{team_a}_vs_{team_b}_{idx}"
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

teams = sorted(df_all['Team'].unique())
for i, team in enumerate(teams):
   print(f'{i}. {team}')
   
idx_a = int(input('Choose first team from above (enter number): '))
team_a = teams[idx_a]
idx_b = int(input('Choose second team from above (enter number): '))
team_b = teams[idx_b]

model_to_use = GradientBoostingClassifier(learning_rate=0.05, max_depth=4, n_estimators=300)
model_to_use.fit(X_train_scaled, y_train)

#i skip gridsearchcv part to save time because i already got parameters i want
future_idx = len(df_all)
f_ab = get_match_history(df_all, team_a, team_b, current_idx=future_idx, N=20).to_frame().T[X.columns].fillna(0)
f_ba = get_match_history(df_all, team_b, team_a, current_idx=future_idx, N=20).to_frame().T[X.columns].fillna(0)

prob_a_dir1 = model_to_use.predict_proba(scaler.transform(f_ab))[0][1]
prob_b_dir2 = model_to_use.predict_proba(scaler.transform(f_ba))[0][1]

prob_a = ((prob_a_dir1 + (1 - prob_b_dir2)) / 2) * 100
prob_b = 100 - prob_a

print(f"Calculating match odds for: {team_a} vs {team_b}")
print(f"Win chance for {team_a}: {prob_a:.1f}%")
print(f"Win chance for {team_b}: {prob_b:.1f}%")

explainer = shap.TreeExplainer(model_to_use)
shap_values = explainer.shap_values(X_test_scaled)
shap.summary_plot(shap_values, X_test_scaled, feature_names=X.columns)