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