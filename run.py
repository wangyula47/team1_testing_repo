

"""
Starting point of the application. This module is invoked from
the command line to run the analyses.
"""

import logging
import argparse

import config
from example_analysis import ExampleAnalysis
from sentiment_scores import SentimentScores
from sentiment_trends import SentimentTrends
from sentiment_bug import SentimentAnalysis


def parse_args():
    """
    Parses the command line arguments that were provided along
    with the python command. The --feature flag must be provided as
    that determines what analysis to run. Optionally, you can pass in
    a user and/or a label to run analysis focusing on specific issues.
    
    You can also add more command line arguments following the pattern
    below.
    """
    ap = argparse.ArgumentParser("run.py")
    
    # Required parameter specifying what analysis to run
    ap.add_argument('--feature', '-f', type=int, required=True,
                    help='Which of the three features to run')
    
    # Optional parameter for analyses focusing on a specific user (i.e., contributor)
    ap.add_argument('--user', '-u', type=str, required=False,
                    help='Optional parameter for analyses focusing on a specific user')
    
    # Optional parameter for analyses focusing on a specific label
    ap.add_argument('--label', '-l', type=str, required=False,
                    help='Optional parameter for analyses focusing on a specific label')
    
    return ap.parse_args()

log_level = config.get_parameter('LOG_LEVEL')
logging.basicConfig(level=logging.getLevelName(log_level),
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    handlers=[logging.StreamHandler()])

# Parse feature to call from command line arguments
args = parse_args()
# Add arguments to config so that they can be accessed in other parts of the application
config.overwrite_from_args(args)
    
# Run the feature specified in the --feature flag
if args.feature == 0:
    ExampleAnalysis().run()
elif args.feature == 1:
    SentimentScores().run()
elif args.feature == 2:
    SentimentTrends().run()
elif args.feature == 3:
    data_path = config.get_parameter('ENPM611_PROJECT_DATA_PATH')
    SentimentAnalysis(data_path).run()
else:
    print('Need to specify which feature to run with --feature flag.')
