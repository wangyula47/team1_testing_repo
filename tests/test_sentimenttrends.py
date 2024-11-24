# testing for the sentiment_trends function 
import unittest
import sentiment_trends

import matplotlib.pyplot as plt
import datetime
import pandas as pd
import matplotlib.dates as mdates

from unittest.mock import MagicMock
from datetime import datetime, timedelta

from sentiment_trends import SentimentTrends



class TestSentimentTrends(unittest.TestCase):


    # setup before any tests run 
    def setUp(self):
       

        # create mock values that represent data used in the function 
        self.mock_sentiment_scores = MagicMock()
        self.mock_sentiment_scores.get_issues_by_label.return_value = {
            'kind/bug': [1],
            'status/duplicate': [2],
            'kind/feature': [],
            'kind/enhancement': [3],
            'kind/question': [4]
        }
        self.mock_sentiment_scores.get_sentiment_scores.return_value = {
            1: {'dates': [datetime(2024, 1, 15), datetime(2024, 1, 20)], 'scores': [0.5, -0.3]},
            2: {'dates': [datetime(2024, 2, 10)], 'scores': [0.8]},
            3: {'dates': [datetime(2024, 3, 5), datetime(2024, 3, 25)], 'scores': [0.4, 0.6]},
            4: {'dates': [datetime(2024, 4, 10)], 'scores': [0.2]},
        }

       
        sentiment_trends.SentimentScores = MagicMock(return_value=self.mock_sentiment_scores)
        self.sentiment_trends = SentimentTrends()


    # test that the trends functions properly gets issues and scores from the sentiment scores class 
    def test_initialization(self):
        self.assertEqual(self.sentiment_trends.issues_by_label, self.mock_sentiment_scores.get_issues_by_label())
        self.assertEqual(self.sentiment_trends.sentiment_scores, self.mock_sentiment_scores.get_sentiment_scores())

    def test_run(self):

        # mock the plot issues overtime method 
        self.sentiment_trends.plot_issues_overtime = MagicMock()

        # run the function 
        self.sentiment_trends.run()

        # test the function is called 
        self.sentiment_trends.plot_issues_overtime.assert_any_call(
            [datetime(2024, 1, 15), datetime(2024, 1, 20)], [0.5, -0.3], 'kind/bug'
        )
        
    def test_plot_issues_overtime(self):
        # mock plot 
        sentiment_trends.plt.show = MagicMock()
        # create test data to test against mock 
        dates = [datetime(2024, 1, 15), datetime(2024, 1, 20)]
        scores = [0.5, -0.3]
        label = 'kind/bug'

        # run plot_issues_overtime with the test input 
        avr = self.sentiment_trends.plot_issues_overtime(dates, scores, label)

        # recreate expected data frame with the test data 
        df = pd.DataFrame({'date': dates, 'score': scores})
        df['date'] = df['date'].dt.tz_localize(None)
        df['month'] = df['date'].dt.to_period('M')
        monthly_avg = df.groupby('month')['score'].mean()

        expected_avg = pd.Series([0.1], index=[pd.Period('2024-01')])
    
        self.assertTrue(monthly_avg.equals(expected_avg))



if __name__ == "__main__":
    unittest.main()
