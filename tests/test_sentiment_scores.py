import unittest
from unittest.mock import patch, MagicMock
from sentiment_scores import SentimentScores
from data_loader import DataLoader
from model import Issue, State
from datetime import datetime

class TestSentimentScores(unittest.TestCase):

    @patch.object(DataLoader, 'get_issues')
    def setUp(self, mock_get_issues):
        # Mock data matching the provided JSON structure
        mock_issues = [
            Issue({
                'url': 'https://github.com/scikit-learn/scikit-learn/issues/29923',
                'creator': 'scikit-learn-bot',
                'labels': [],
                'state': 'open',
                'assignees': [],
                'title': 'invalid Issue 1',
                'text': 'Test description',
                'number': 29923,
                'created_date': '2024-09-24T02:36:01+00:00',
                'updated_date': '2024-09-25T02:51:05+00:00',
                'timeline_url': 'https://api.github.com/repos/test/test/issues/1/timeline',
                'events': [
                    {
                        'event_type': 'commented',
                        'author': 'user1',
                        'event_date': '2024-09-24T09:02:06+00:00',
                        'comment': 'Great feature!'
                    },
                    {
                        'event_type': 'commented',
                        'author': 'user2',
                        'event_date': '2024-09-24T09:02:10+00:00',
                        'comment': 'Needs improvement.'
                    }
                ]
            }),
            Issue({
                'url': 'https://github.com/scikit-learn/scikit-learn/issues/29924',
                'creator': 'user2',
                'labels': ['bug'],
                'state': 'closed',
                'assignees': [],
                'title': 'invalid Issue 2',
                'text': 'Another test description',
                'number': 29924,
                'created_date': '2024-09-24T02:36:01+00:00',
                'updated_date': '2024-09-25T02:51:05+00:00',
                'timeline_url': 'https://api.github.com/repos/test/test/issues/2/timeline',
                'events': [
                    {
                        'event_type': 'commented',
                        'author': 'user3',
                        'event_date': '2024-09-24T09:02:06+00:00',
                        'comment': 'Excellent work!'
                    }
                ]
            }),
            Issue({
                'number': 29925,
                'title': 'Test Issue',
                'state': 'open',
                'labels': ['bug'],
                'created_date': '2024-09-24T02:36:01+00:00',
                'events': [
                    {
                        'event_type': 'commented',
                        'author': 'user1',
                        'event_date': '2024-09-24T09:02:06+00:00',
                        'comment': 'Test comment'
                    }
                ]
            })
        
        ]
        mock_get_issues.return_value = mock_issues
        self.sentiment_scores = SentimentScores()
    # Test if the sentiment maps are populated correctly.
    def test_populate_maps(self):
        self.sentiment_scores._populate_maps()
        sentiment_scores = self.sentiment_scores.get_sentiment_scores()
        self.assertEqual(len(sentiment_scores), 3)
        self.assertIn(29923, sentiment_scores)
        self.assertIn(29924, sentiment_scores)

    # Test retrieving the sentiment score for a specific issue.
    def test_get_sentiment_score(self):
        self.sentiment_scores._populate_maps()
        score = self.sentiment_scores.get_sentiment_score(29923)
        self.assertIsInstance(score, float)

    # Test grouping issues by their labels.
    def test_get_issues_by_label(self):
        self.sentiment_scores._populate_maps()
        issues_by_label = self.sentiment_scores.get_issues_by_label()
        self.assertIn('bug', issues_by_label)

    #Test linear regression on sentiment score trends.
    def test_get_liner_regression(self):
        days = [1, 2, 3, 4, 5]
        scores = [0.1, 0.2, 0.3, 0.4, 0.5]
        slope, intercept, r_value = self.sentiment_scores.get_liner_regression(days, scores)
        self.assertIsInstance(slope, float)
        self.assertIsInstance(intercept, float)
        self.assertIsInstance(r_value, float)

    # Test plotting sentiment scores for a specific issue.
    @patch('matplotlib.pyplot.show')
    def test_plot_sentiment_scores(self, mock_show):
        self.sentiment_scores._populate_maps()
        self.sentiment_scores._plot_sentiment_scores(29923)
        mock_show.assert_called_once()

    @patch('builtins.input', side_effect=['29923', 'exit'])
    @patch('matplotlib.pyplot.show')
    def test_run(self, mock_show, mock_input):
        self.sentiment_scores.run()
        mock_show.assert_called_once()

    # Test sentiment score retrieval for valid and invalid issue numbers.
    def test_error_handling(self):
        # Test with valid issue number from setUp
        score = self.sentiment_scores.get_sentiment_score(29923)
        self.assertIsNotNone(score)
        
    def test_preprocessing(self):
        # Test comment processing through sentiment analysis
        self.sentiment_scores._populate_maps()
        scores = self.sentiment_scores.get_sentiment_scores()
        self.assertIn(29923, scores)
        


    @patch('builtins.input', side_effect=['invalid', 'exit'])
    def test_invalid_input(self, mock_input):
        with patch('matplotlib.pyplot.show'):
            self.sentiment_scores.run()

    def test_empty_comments(self):
        # Test issue with no comments
        score = self.sentiment_scores.get_sentiment_score(99999)  # Non-existent issue
        self.assertEqual(score, 0)

    # Test linear regression function with valid data.
    def test_linear_regression(self):
        days = [1, 2, 3]
        scores = [0.1, 0.2, 0.3]
        slope, intercept, r_value = self.sentiment_scores.get_liner_regression(days, scores)
        self.assertIsInstance(slope, float)
        self.assertIsInstance(intercept, float)
        self.assertIsInstance(r_value, float)

if __name__ == '__main__':
    unittest.main()