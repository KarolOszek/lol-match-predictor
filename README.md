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

### PyTorch Model Evaluation
![PyTorch model shap values](assets/shap_values.png)
#### How to Interpret the SHAP Summary Plot
The plot illustrates the global impact of each team differential feature on the model's win prediction. Here is the breakdown:

Feature Importance (Vertical Axis): The features are sorted from most important (top) to least important (bottom) based on their overall impact on the final output. The top feature, Towers_diff, has the most spread and furthest dots from the center, making it the strongest predictor.

Feature Value (Color Scale): The color of each dot shows the actual numerical value of that statistic in a specific match from the test set.

Red: A large advantage for Team A (e.g., Team A took many more towers).

Blue: A large disadvantage for Team A (e.g., Team A has fewer towers).

Impact on Model Output (Horizontal Axis): This axis shows how much a particular feature value pushed the model's final win probability up or down.

Positive SHAP Value (Right side): The feature pushed the model to predict "Team A wins".

Negative SHAP Value (Left side): The feature pushed the model to predict "Team A loses".

#### XAI Insights: Why the Neural Network Underperformed
​By applying SHAP (DeepExplainer) to the PyTorch model, we uncovered a fascinating flaw in how the network interpreted the game. While it correctly identified Towers_diff and Gold/sec_diff as massive win conditions, it developed a counter-intuitive understanding of other crucial metrics.
​Specifically, the SHAP summary plot revealed that the network assigned negative impacts to positive advantages in Dragons_diff and Kills_diff (with high/red values pushing the prediction toward a loss).
​Why did this happen?
In League of Legends, objectives are highly correlated (multicollinearity). A team taking multiple towers is naturally also securing gold, dragons, and kills. To avoid overestimating the win probability past 100%, the neural network mathematically "compensated" by heavily penalizing dragons and kills to balance the massive weights it assigned to towers and gold.
​This Explainable AI (XAI) analysis perfectly demonstrates why the baseline Gradient Boosting Classifier achieved a higher accuracy (~83% vs 78.5%). Tree-based algorithms inherently handle highly correlated, tabular features much better than a simple Multi-Layer Perceptron, which ultimately got confused by the collinear nature of the match statistics
## Automated Data Pipeline (Web Scraping)
The project features a built-in, automated web scraping module designed to extract the most up-to-date match history and team statistics directly from gol.gg.

### Key features of the data ingestion pipeline include:

Dynamic Scraping with Selenium: Utilizes selenium with a headless Chrome browser configuration to navigate dynamic, JavaScript-rendered tables and interactive elements.

Responsive Design Handling: Enforces a strict virtual window size (--window-size=1920,1080) to ensure all hidden statistical columns are rendered and captured by the scraper.

HTML Parsing & Cleaning: Leverages pandas.read_html to efficiently parse the raw DOM elements, automatically mapping them to structured DataFrames and cleaning missing headers on the fly.

Smart Data Caching: Implements a conditional local storage mechanism using the os module. The script checks for existing .csv datasets before execution, giving the user the option to load cached data instantly or trigger a fresh scrape to avoid redundant server requests and save time.

