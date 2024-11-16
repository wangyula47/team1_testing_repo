# System modules
import logging

# Matplotlib
import matplotlib
matplotlib.use('Qt5Agg')  # Use the TkAgg backend for interactive plots
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Scipy
from scipy.stats import linregress

# TextBlob
from textblob import TextBlob

# Project
import config
from data_loader import DataLoader

# Data structures contain sentiment scores based on the comments of issues, not the original issues itself
sentiment_scores = None  # Map containing datetimes (increasing order), scores, and issue title
average_sentiment_scores = None  # Map from issue.number to average sentiment score
issues_by_label = None  # Map label to issue.numbers

_issues = None

class SentimentScores:
    """
    Generates sentiment scores using TextBlob
    """

    def __init__(self):
        # Using global variables as they will not change
        global sentiment_scores, average_sentiment_scores, issues_by_label, _issues
        sentiment_scores = {}
        average_sentiment_scores = {}
        issues_by_label = {}
        _issues = DataLoader().get_issues()
        self._populate_maps()

    def get_sentiment_score(self, issueNumber):
        if issueNumber in average_sentiment_scores:
            return average_sentiment_scores[issueNumber]
        return 0
    
    def get_issues_by_label(self):
        return issues_by_label

    def get_sentiment_scores(self):
        return sentiment_scores

    def _populate_maps(self):
        for issue in _issues:
            # Initialize variables
            total_score = 0
            count = 0
            sentiment_scores[issue.number] = {}
            sentiment_scores[issue.number]['title'] = issue.title[:50]
            sentiment_scores[issue.number]['dates'] = []
            sentiment_scores[issue.number]['scores'] = []
            
            # Populate sentiment_scores map
            for event in issue.events:
                if event.event_type == "commented" and event.author != "github-actions[bot]":
                    blob = TextBlob(event.comment)
                    score = blob.sentiment.polarity
                    count += 1
                    total_score += score
                    sentiment_scores[issue.number]['dates'].append(event.event_date)
                    sentiment_scores[issue.number]['scores'].append(score)
                    for label in issue.labels:
                        issues_by_label.setdefault(label.lower(), []).append(issue.number)
            
            # Populate average_sentiment_scores map
            if count != 0:
                average_sentiment_scores[issue.number] = total_score / count
            else:
                logging.debug(f"Issue {issue.number} has no comments. Not adding to average sentiment scores map.")

    def get_liner_regression(self, days_since_epoch, scores):
        slope, intercept, r_value, _, _ = linregress(days_since_epoch, scores)
        return slope, intercept, r_value

    def _plot_linear_regression_line(self, keys, values):
        logging.debug("Attempting to plot linear regression line")
        # Linear regression cannot be done with fewer than two data points
        if len(keys) < 2:
            logging.warning(f"Unable to create linear regression line. Fewer than two data points.")
            return False

        # Perform linear regression
        slope, intercept, r_value = self.get_liner_regression(keys, values)
        regression_line = slope * keys + intercept
        plt.plot(keys, regression_line, color='red', label=f'Linear Regression (r={r_value:.2f})')
        return True

    def _plot_sentiment_scores(self, issue_number, plot_lin_reg=True):
        # Lists of dates and sentiment scores
        dates = list(sentiment_scores[issue_number]['dates'])
        scores = list(sentiment_scores[issue_number]['scores'])

        # Create plot
        plt.figure(figsize=(8, 6))
        plt.plot(dates, scores, marker='o', linestyle='-', color='b')

        # Plot liner regression
        if plot_lin_reg:
            # Convert datetime to time since epoch
            days_since_epoch = mdates.date2num(dates)
            lin_reg_success = self._plot_linear_regression_line(days_since_epoch, scores)

        # Format the graph
        plt.xticks(rotation=45)
        plt.xlabel('Date')
        plt.ylabel('Sentiment Score')
        plt.title(f"{sentiment_scores[issue_number]['title']}...")
        # Only show the legend if the linear regression line was added to the figure
        if lin_reg_success:
            plt.legend()
        plt.tight_layout()
        plt.show()

    def run(self):
        while(True):
            print("\n---------------------------")
            # Iterate over user data.
            message = ("Please enter one of the following to display sentiment scores:\n"
                       "- The first few words of an issue title\n"
                       "- An issue number (e.g. 7051, 4055, etc.) \n"
                       "\n"
                       "- or enter \'exit\' to quit analysis.\n\n"
                       "> ")
            user_input = input(message)
            if user_input.lower() == "exit":
                print("Goodbye!")
                return

            # Attempt to parse issue number
            issue_number = -1
            try:
                issue_number = int(user_input)
                if issue_number not in sentiment_scores:
                    logging.error(f"Could not find issue number: {issue_number}")
                    continue
            except ValueError:
                logging.debug(f"Trying to find issue with title: '{user_input}'...")
                found = False
                for issue in _issues:
                    if issue.title.startswith(user_input):
                        issue_number = issue.number
                        found = True
                if not found:
                    logging.error(f"Could not find issue title starting with \'{user_input}\'")
                    continue
            
            # Plot the sentiment scores
            self._plot_sentiment_scores(issue_number)
    
if __name__ == '__main__':
    # Run for testing
    log_level = config.get_parameter('LOG_LEVEL')
    logging.basicConfig(level=logging.getLevelName(log_level),
                        format='%(asctime)s [%(levelname)s] %(message)s',
                        handlers=[logging.StreamHandler()])
    SentimentScores().run()