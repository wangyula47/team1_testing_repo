
import json
from typing import List

import config
from model import Issue

from datetime import datetime
import re

# Store issues as singleton to avoid reloads
_ISSUES:List[Issue] = None

class DataLoader:
    """
    Loads the issue data into a runtime object.
    """
    
    def __init__(self):
        """
        Constructor
        """
        self.data_path:str = config.get_parameter('ENPM611_PROJECT_DATA_PATH')
        self.debug_mode:bool = config.get_parameter('DEBUG_MODE')
        self.debug_print_path:str = config.get_parameter('DEBUG_COMMENTS_PRINT_PATH')
        
    def get_issues(self):
        """
        This should be invoked by other parts of the application to get access
        to the issues in the data file.
        """
        global _ISSUES # to access it within the function
        if _ISSUES is None:
            _ISSUES = self._load()
            print(f'Loaded {len(_ISSUES)} issues from {self.data_path}.')
            self._preprocess_data()
        return _ISSUES
    
    def _debug_print(self, file, text):
        if self.debug_mode:
            file.write(text)
    def load_data(self):
        # Load the JSON data
        with  open(self.data_path,'r') as fin:
          return   json.load(fin)

    def _preprocess_data(self):
        """
        Removes problematic data from issues ahead of sentiment analysis
        """
        # Remove null events
        with open(self.debug_print_path, 'w') as file: 
            for issue in _ISSUES:
                # 2 issues have null text
                if issue.text is None:
                    issue.text = ""
                
                # 188 issues have null authors and event_dates, also perform general cleanup
                for event in list(issue.events):
                    if event.comment is not None:
                        # Replace all embedded hyperlinks with just the words. [<word>](<url>) -> <word>
                        event.comment = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', event.comment)

                        # Remove any replies, "> [<text>]\r" or "> [<text>]\n", as they can affect sentiment scores
                        event.comment = re.sub(r'>.+?[\r\n]', '', event.comment)

                        # Replace any additional \r or \n characters with whitespace
                        event.comment = re.sub(r'[\r\n]+', ' ', event.comment)
                    
                    if event.author is None:
                        event.author = ""
                    if event.event_date is None:
                        event.event_date = datetime(1970, 1, 1)
                    
                    if event.comment != None:
                        self._debug_print(file, f"{event.comment}\n")
                    
                self._debug_print(file, f"\n\n\n")
            file.close()

    def _load(self):
        """
        Loads the issues into memory.
        """
        with open(self.data_path,'r') as fin:
            return [Issue(i) for i in json.load(fin)]
    

if __name__ == '__main__':
    # Run the loader for testing
    DataLoader().get_issues()