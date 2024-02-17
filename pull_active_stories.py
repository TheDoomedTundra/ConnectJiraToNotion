#!/usr/bin/env python3
from RestApiBase import dump_to_file
from JiraUtils import *

if __name__ == '__main__':
    token_file = '.local/share/jira_tokens/pull_scripts.json'
    
    data = pull_active_stories(token_file)
    dump_to_file(data)
