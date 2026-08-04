# lol-match-predictor
Predictive ML model for League of Legends pro matches using historical team performance and chronological data splitting. [Python / scikit-learn]


## Model Evaluation & Visualizations

### Baseline Models Comparison
Initial benchmark comparing default classifiers (Logistic Regression, Random Forest, Gradient Boosting, SVM) evaluated on the test set:

![Baseline Models Comparison](assets/baseline%20models%20accuracy%20comparision.png)

### Feature Importance
Feature importance extraction from the Gradient Boosting model. Mid-game differentials (especially objective and gold metrics) have the strongest impact on model predictions:

![Feature Importance](assets/baseline%20gradient%20boosting%20feature%20importance.png)
note: Adding Side Flag yielded minimal performance gain (~X%), suggesting that overall team form and objective control heavily outweigh static side advantages in this dataset.


#### Data scraped from gol.gg
