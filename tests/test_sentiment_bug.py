import unittest
from unittest.mock import patch, MagicMock
from sentiment_bug import SentimentAnalysis
from data_loader import DataLoader
import pandas as pd

class TestSentimentBugs(unittest.TestCase):
    
    @patch.object(DataLoader, 'load_data')
    def setUp(self, mock_load_data):
        # Mock data representing a sample JSON data structure
        mock_load_data.return_value = [
            {'number': 1, 'created_date': '2022-01-01T00:00:00Z', 'labels': ['bug'], 'events': []},
            {'number': 2, 'created_date': '2022-02-01T00:00:00Z', 'labels': ['feature'], 'events': []},
            {'number': 3, 'created_date': '2022-03-01T00:00:00Z', 'labels': ['enhancement'], 'events': []},
            {'number': 4, 'created_date': None, 'labels': ['bug'], 'events': []},  # Test case with null date
            {'number': 5, 'created_date': 'InvalidDate', 'labels': ['bug'], 'events': []},  # Invalid date format
            {'number': 6, 'created_date': '2022-04-01T00:00:00Z', 'labels': [], 'events': []},  # No labels
            {'number': 7, 'created_date': '2022-05-01T00:00:00Z', 'labels': ['other'], 'events': []}  # Different label
        ]
        self.analysis = SentimentAnalysis('mock_json_file.json')
        self.analysis.data = mock_load_data()

    def test_process_issues(self):
        # Test process_issues to see if DataFrame is created as expected
        self.analysis.process_issues()
        self.assertIsNotNone(self.analysis.df)
        self.assertEqual(len(self.analysis.df), 5)  # Only "Bug" and "Feature" should be processed

    def test_prepare_data(self):
        # Test the prepare_data function
        self.analysis.process_issues()
        self.analysis.prepare_data()

        # Check that only valid dates are in the DataFrame and week/year are calculated correctly
        self.assertFalse(self.analysis.df['CreatedDate'].isna().any())  # No NaT values should remain
        self.assertIn('Week', self.analysis.df.columns)
        self.assertIn('Year', self.analysis.df.columns)

    @patch('builtins.print')
    def test_print_statistics_format(self, mock_print):
        # Test the statistics printing for both bugs and features
        self.analysis.process_issues()
        self.analysis.prepare_data()

        weekly_bugs = self.analysis.df[self.analysis.df['Category'] == 'Bug'].groupby('Week').agg(
            NumberOfBugs=('SentimentScore', 'count'),
            AvgSentimentScore=('SentimentScore', 'mean')
        ).reset_index()

        self.analysis._print_statistics(weekly_bugs)

        # Check if the print function was called, indicating that statistics were printed
        self.assertTrue(mock_print.call_count > 0)

    def test_categorize_labels(self):
        # Test categorize_labels to ensure correct categorization
        self.assertEqual(self.analysis.categorize_labels(['bug']), 'Bug')
        self.assertEqual(self.analysis.categorize_labels(['feature']), 'Feature')
        self.assertEqual(self.analysis.categorize_labels(['enhancement']), 'Feature')
        self.assertEqual(self.analysis.categorize_labels(['other']), 'Other')

    def test_empty_data(self):
        # Test with empty dataset
        self.analysis.data = []
        self.analysis.process_issues()
        self.assertTrue(self.analysis.df.empty)

    def test_invalid_dates(self):
        # Test behavior with invalid dates
        self.analysis.process_issues()
        self.analysis.prepare_data()

        # Check that rows with invalid dates are dropped
        invalid_dates_count = self.analysis.df[self.analysis.df['CreatedDate'].isna()].shape[0]
        self.assertEqual(invalid_dates_count, 0)

    def test_plot_combined(self):
        # Test the plot_combined function to ensure it runs without errors
        self.analysis.process_issues()
        self.analysis.prepare_data()

        # Mock plt.show to prevent the actual plot from rendering during the test
        with patch('matplotlib.pyplot.show'):
            self.analysis.plot_combined()

    @patch.object(SentimentAnalysis, '_print_statistics')
    def test_run(self, mock_print_statistics):
        # Test the full run flow to ensure all methods are called
        self.analysis.run()

        # Ensure that _print_statistics was called, meaning the full flow ran
        self.assertTrue(mock_print_statistics.called)


if __name__ == '__main__':
    unittest.main()

