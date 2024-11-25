# Sentiment Analysis for Python Poetry Issues

This application template implements some of the basic functions:

- `sentiment_scores.py`: Analysis of sentiment scores on a per issue basis
- `sentiment_trends.py`: Analysis of sentiment trends over issue labels
- `sentiment_bug.py`: Analysis of sentiment distribution
<hr>

- `data_loader.py`: Utility to load the issues from the provided data file and returns the issues in a runtime data structure (e.g., objects)
- `model.py`: Implements the data model into which the data file is loaded. The data can then be accessed by accessing the fields of objects.
- `config.py`: Supports configuring the application via the `config.json` file. You can add other configuration parameters to the `config.json` file.
- `run.py`: This is the module that will be invoked to run your application. Based on the `--feature` command line parameter, one of the three analyses you implemented will be run. You need to extend this module to call other analyses.

With the utility functions provided, you should focus on implementing creative analyses that generate interesting and insightful insights.

In addition to the utility functions, an example analysis has also been implemented in `example_analysis.py`. It illustrates how to use the provided utility functions and how to produce output.

## Analysis Descriptions
### Sentiment Scores Analysis
Given an issue title or number, the sentiment score for each of the comments is calculated and displayed. Additionally, a linear regression line is displayed to show the overall sentiment across all comments within an issue. Note: linear regression can't be calculated if an issue has less than two comments.

### Sentiment Trends Analysis
The sentiment trends analysis dives into issues labeled: bug, duplicate, feature, enhancement and question. We plot the sentiment of comments for these issues (averaged by month) over time. This allows us to see how the sentiment of different labels evolves over time, providing insight into community involvement across different issue types.

### Sentiment Distribution Analysis
The sentiment distribution analysis examines the relationship between number of bugs per week and the sentiment score for that week. This is divided into subcategories for features and bugs. This analysis shows as the number of bugs increases the overall sentiment remains neutral. Given the large number of comments, it's unsurprising that the sentiment follows a normal distribution.

## Setup

### Install dependencies

In the root directory of the application, create a virtual environment, activate that environment, and install the dependencies like so:

```
pip install -r requirements.txt
```

### Download and configure the data file

Download the data file (in `json` format) from the project assignment in Canvas and update the `config.json` with the path to the file. Note, you can also specify an environment variable by the same name as the config setting (`ENPM611_PROJECT_DATA_PATH`) to avoid committing your personal path to the repository.


### Run an analysis

With everything set up, you should be able to run the existing example analysis:

```
python run.py --feature 0
```
Sentiment scores analysis:
```
python run.py --feature 1
```
Sentiment trends analysis:
```
python run.py --feature 2
```
Sentiment distribution analysis:
```
python run.py --feature 3
```


That will output basic information about the issues to the command line.

## Install dependencies
pip install coverage
## Running unit test case
To run the unit tests for this project:
python -m coverage run -m unittest discover -s tests

## Generating Test Coverage Report
After running the tests, you can generate a coverage report using the following command:
python -m coverage report --omit="test_*"

## Note:
While running the tests, if any graphical windows open (e.g., for plotting or visualizing results), make sure to close the graph after reviewing it. This allows the next test case to execute without interruptions.


## VSCode run configuration

To make the application easier to debug, runtime configurations are provided to run each of the analyses you are implementing. When you click on the run button in the left-hand side toolbar, you can select to run one of the three analyses or run the file you are currently viewing. That makes debugging a little easier. This run configuration is specified in the `.vscode/launch.json` if you want to modify it.

The `.vscode/settings.json` also customizes the VSCode user interface slightly to make navigation and debugging easier. But that is a matter of preference and can be turned off by removing the appropriate settings.
