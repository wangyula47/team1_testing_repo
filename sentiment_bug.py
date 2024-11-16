import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sentiment_scores import SentimentScores
from data_loader import DataLoader

class SentimentAnalysis:
    def __init__(self, json_file):
        self.json_file = json_file
        self.data = None
        self.df = None
        self.sentimentScores = SentimentScores()

    # Function to categorize labels
    def categorize_labels(self, labels):
        bugs = ['bug', 'kind/bug', 'issue']
        features = ['feature', 'enhancement']
        for label in labels:
            if any(bug in label.lower() for bug in bugs):
                return 'Bug'
            elif any(feature in label.lower() for feature in features):
                return 'Feature'
        return 'Other'

    def process_issues(self):
        # Extract relevant data into a list, including created_date and sentiment score
        issues_list = []
        for issue in self.data:
            labels = issue.get('labels', [])
            created_date = issue.get('created_date', 'Unknown')
            issueNumber = issue.get('number')
            category = self.categorize_labels(labels)
            
            # Append the data for Bugs and Features
            if category in ["Bug", "Feature"]:
                issues_list.append({
                    'CreatedDate': created_date,
                    'SentimentScore': self.sentimentScores.get_sentiment_score(issueNumber),
                    'Category': category
                })

        # Create a DataFrame from the list
        self.df = pd.DataFrame(issues_list)

    def prepare_data(self):
        # Convert the CreatedDate to datetime, ignoring invalid formats
        self.df['CreatedDate'] = pd.to_datetime(self.df['CreatedDate'], errors='coerce')

        # Filter out rows with NaT (invalid dates)
        self.df = self.df.dropna(subset=['CreatedDate'])

        # Extract the week from CreatedDate and add it as a new column
        self.df['Week'] = self.df['CreatedDate'].dt.to_period('W')  # Year-Week period
        self.df['Year'] = self.df['CreatedDate'].dt.year  # Extract the year

    def _print_statistics(self, data):
        min_val = np.min(data['AvgSentimentScore'])
        max_val = np.max(data['AvgSentimentScore'])
        mean_val = np.mean(data['AvgSentimentScore'])
        median_val = np.median(data['AvgSentimentScore'])
        q1_val = np.percentile(data['AvgSentimentScore'], 25)  # Q1
        q3_val = np.percentile(data['AvgSentimentScore'], 75)  # Q3

        print(f"Min: {min_val:.2f}\n"
            f"Q1: {q1_val:.2f}\n"
            f"Median: {median_val:.2f}\n"
            f"Mean: {mean_val:.2f}\n"
            f"Q3: {q3_val:.2f}\n"
            f"Max: {max_val:.2f}")

    def plot_combined(self):
        # Create subplots: 1 row and 2 columns
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))

        # ---------------- 2D Plot for Sentiment vs Bugs/Features ----------------
        # Separate bugs and features into two dataframes
        bugs_df = self.df[self.df['Category'] == 'Bug']
        features_df = self.df[self.df['Category'] == 'Feature']

        # Group by Week and calculate the number of bugs/features and average sentiment score
        weekly_bugs = bugs_df.groupby('Week').agg(
            NumberOfBugs=('SentimentScore', 'count'),  # Count of bugs
            AvgSentimentScore=('SentimentScore', 'mean')  # Average sentiment score for bugs
        ).reset_index()

        weekly_features = features_df.groupby('Week').agg(
            NumberOfFeatures=('SentimentScore', 'count'),  # Count of features
            AvgSentimentScore=('SentimentScore', 'mean')  # Average sentiment score for features
        ).reset_index()

        # Plot the 2D line chart in the first subplot (ax1)
        ax1.plot(weekly_bugs['NumberOfBugs'], weekly_bugs['AvgSentimentScore'], color='blue', marker='o', label='Bugs')
        ax1.plot(weekly_features['NumberOfFeatures'], weekly_features['AvgSentimentScore'], color='red', marker='o', label='Features')

        # Customize ax1 (2D plot)
        ax1.set_title('Sentiment Score vs Number of Bugs and Features')
        ax1.set_xlabel('Number of Bugs/Features')
        ax1.set_ylabel('Average Sentiment Score')
        ax1.legend()

        print("Statistics for bugs (grouped by week): ")
        self._print_statistics(weekly_bugs)
        print("\nStatistics for features (grouped by week): ")
        self._print_statistics(weekly_features)

        # ---------------- 3D Plot for Sentiment vs Bugs (Yearly) ----------------
        # Group by Year and calculate the number of bugs and average sentiment score
        yearly_bug_count = bugs_df.groupby('Year').size().reset_index(name='NumberOfBugs')
        yearly_avg_sentiment = bugs_df.groupby('Year')['SentimentScore'].mean().reset_index()

        # Merge the two dataframes on Year
        yearly_data = pd.merge(yearly_bug_count, yearly_avg_sentiment, on='Year')

        # Create a 3D plot in the second subplot (ax2)
        ax2 = fig.add_subplot(212, projection='3d')

        # Scatter plot: X = Year, Y = Number of Bugs, Z = Average Sentiment Score
        ax2.scatter(yearly_data['Year'], yearly_data['NumberOfBugs'], yearly_data['SentimentScore'], color='blue')

        # Set labels for the 3D plot
        ax2.set_xlabel('Year')
        ax2.set_ylabel('Number of Bugs')
        ax2.set_zlabel('Average Sentiment Score')
        ax2.set_title('3D Plot: Number of Bugs vs Average Sentiment Score per Year')

        # Adjust layout to prevent overlap and add space between plots
        plt.subplots_adjust(hspace=0.4)

        # Display the combined plots
        plt.show()

    def run(self):
        self.data = DataLoader().load_data()
        self.process_issues()
        self.prepare_data()

        # Plot both charts in one window
        self.plot_combined()

# Usage
if __name__ == "__main__":
    sentiment_analysis = SentimentAnalysis('poetry_issues_all.json')
    sentiment_analysis.run()
