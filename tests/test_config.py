import unittest
from unittest.mock import patch, MagicMock
import json
import os
import config

class TestConfig(unittest.TestCase):

    def setUp(self):
        # Reset config before each test
        config._config = None
        # Clear environment variables
        for key in list(os.environ.keys()):
            if key not in ('PATH', 'SYSTEMROOT', 'USERNAME'):
                del os.environ[key]

    @patch('os.path.isfile')
    @patch('builtins.open')
    def test_init_config_with_file(self, mock_open, mock_isfile):
        # Mock file existence and content
        mock_isfile.return_value = True
        mock_file = MagicMock()
        mock_file.read.return_value = '{"test_param": "test_value"}'
        mock_open.return_value.__enter__.return_value = mock_file
        
        config._init_config()
        self.assertEqual(config._config['test_param'], 'test_value')

    @patch('os.path.isfile')
    def test_init_config_without_file(self, mock_isfile):
        mock_isfile.return_value = False
        config._init_config()
        self.assertEqual(config._config, {})

    def test_get_parameter_from_env(self):
        os.environ['TEST_PARAM'] = 'env_value'
        value = config.get_parameter('TEST_PARAM')
        self.assertEqual(value, 'env_value')

    def test_get_parameter_json_from_env(self):
        os.environ['TEST_PARAM'] = 'json:{"key": "value"}'
        value = config.get_parameter('TEST_PARAM')
        self.assertEqual(value, {"key": "value"})

    def test_get_parameter_with_default(self):
        value = config.get_parameter('MISSING_PARAM', default='default_value')
        self.assertEqual(value, 'default_value')

    def test_convert_to_typed_value(self):
        test_cases = [
            ('{"key": "value"}', {"key": "value"}),
            ('true', True),
            ('42', 42),
            ('string', 'string'),
            (None, None),
            ({"key": "value"}, {"key": "value"})
        ]
        
        for input_value, expected in test_cases:
            result = config.convert_to_typed_value(input_value)
            self.assertEqual(result, expected)

    def test_set_parameter_string(self):
        config.set_parameter('TEST_PARAM', 'test_value')
        self.assertEqual(os.environ['TEST_PARAM'], 'test_value')

    def test_set_parameter_json(self):
        config.set_parameter('TEST_PARAM', {"key": "value"})
        self.assertEqual(os.environ['TEST_PARAM'], 'json:{"key": "value"}')

    @patch('os.getcwd')
    @patch('os.path.isfile')
    def test_get_default_path(self, mock_isfile, mock_getcwd):
        mock_getcwd.return_value = '/test/path'
        mock_isfile.side_effect = [False, True]
        
        path = config._get_default_path()
        self.assertIsNotNone(path)

    def test_overwrite_from_args(self):
        class Args:
            def __init__(self):
                self.test_param = 'test_value'
                
        args = Args()
        config.overwrite_from_args(args)
        self.assertEqual(os.environ['test_param'], 'test_value')

if __name__ == '__main__':
    unittest.main()