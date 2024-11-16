import matplotlib.pyplot as plt
import datetime
import pandas as pd
import matplotlib.dates as mdates

from sentiment_scores import SentimentScores

labels = ['kind/bug','status/duplicate','kind/feature','kind/enhancement','kind/question']

class SentimentTrends:

    def __init__(self):
        sentiment_scores = SentimentScores()
        self.issues_by_label = sentiment_scores.get_issues_by_label()
        self.sentiment_scores = sentiment_scores.get_sentiment_scores()
        

    def run(self):
        for label in labels:
            dates = []
            scores = []
            for issue_id in self.issues_by_label[label]:
                issue = self.sentiment_scores[issue_id]
                dates.extend(issue['dates'])
                scores.extend(issue['scores'])
            
            self.plot_issues_overtime(dates, scores, label)


    def plot_issues_overtime(self, dates, scores, label):
        df = pd.DataFrame({'date': dates, 'score': scores})

        # Transform date by year and month
        df['date'] = df['date'].dt.tz_localize(None)
        df['month'] = df['date'].dt.to_period('M')

        # Group by the month and calculate average sentiment per month
        monthly_avg = df.groupby('month')['score'].mean()

        plt.figure(figsize=(10, 6))

        monthly_avg.plot(kind='bar', edgecolor='black')

        plt.xlabel('Month')
        plt.ylabel('Average Sentiment Score')
        plt.title('Average ' + label + ' Sentiment Score by Month')
        plt.xticks(rotation=45)

        plt.tight_layout()
        plt.show()