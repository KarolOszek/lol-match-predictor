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

## Automated Data Pipeline (Web Scraping)
The project features a built-in, automated web scraping module designed to extract the most up-to-date match history and team statistics directly from gol.gg.

### Key features of the data ingestion pipeline include:

Dynamic Scraping with Selenium: Utilizes selenium with a headless Chrome browser configuration to navigate dynamic, JavaScript-rendered tables and interactive elements.

Responsive Design Handling: Enforces a strict virtual window size (--window-size=1920,1080) to ensure all hidden statistical columns are rendered and captured by the scraper.

HTML Parsing & Cleaning: Leverages pandas.read_html to efficiently parse the raw DOM elements, automatically mapping them to structured DataFrames and cleaning missing headers on the fly.

Smart Data Caching: Implements a conditional local storage mechanism using the os module. The script checks for existing .csv datasets before execution, giving the user the option to load cached data instantly or trigger a fresh scrape to avoid redundant server requests and save time.

