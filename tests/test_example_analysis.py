import unittest
from unittest.mock import patch, MagicMock
from example_analysis import ExampleAnalysis
from data_loader import DataLoader
import pandas as pd

class TestExampleAnalysis(unittest.TestCase):

    @patch.object(DataLoader, 'get_issues')
    @patch('config.get_parameter')
    def setUp(self, mock_config, mock_get_issues):
        # Mock config to return test user
        mock_config.return_value = 'test_user'
        
        # Create mock issues with controlled data
        self.mock_issues = [
            MagicMock(
                creator='user1',
                events=[
                    MagicMock(author='test_user', event_type='commented'),
                    MagicMock(author='test_user', event_type='commented')
                ]
            ),
            MagicMock(
                creator='user2',
                events=[
                    MagicMock(author='test_user', event_type='commented')
                ]
            ),
            MagicMock(
                creator='user1',
                events=[
                    MagicMock(author='other_user', event_type='commented')
                ]
            )
        ]
        # Ensure get_issues always returns our mock data
        mock_get_issues.return_value = self.mock_issues
        self.analysis = ExampleAnalysis()

    @patch('matplotlib.pyplot.show')
    @patch('pandas.DataFrame.plot')
    @patch('builtins.print')
    @patch.object(DataLoader, 'get_issues')
    def test_run_with_user(self, mock_get_issues, mock_print, mock_plot, mock_show):
        # Setup mocks
        mock_get_issues.return_value = self.mock_issues
        mock_plot.return_value = MagicMock()
        
        # Run analysis
        self.analysis.run()
        
        # Verify print output
        expected_output = '\n\nFound 3 events across 3 issues for test_user.\n\n'
        mock_print.assert_called_with(expected_output)
        mock_show.assert_called_once()

    @patch('matplotlib.pyplot.show')
    @patch('pandas.DataFrame.plot')
    @patch('builtins.print')
    @patch('config.get_parameter')
    @patch.object(DataLoader, 'get_issues')
    def test_run_without_user(self, mock_get_issues, mock_config, mock_print, mock_plot, mock_show):
        # Setup mocks
        mock_config.return_value = None
        mock_get_issues.return_value = self.mock_issues
        mock_plot.return_value = MagicMock()
        
        # Create new analysis instance with None user
        analysis = ExampleAnalysis()
        analysis.run()
        
        # Verify print output
        expected_output = '\n\nFound 4 events across 3 issues.\n\n'
        mock_print.assert_called_with(expected_output)
        mock_show.assert_called_once()



if __name__ == '__main__':
    unittest.main()
