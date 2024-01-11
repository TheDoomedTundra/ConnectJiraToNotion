#!/usr/bin/env python3

import json
import logging
import os
import requests
import sys

import JiraApi

if __name__ == '__main__':
    token_file = '.local/share/jira_tokens/pull_scripts.json'
    story_query = 'issuetype = Story AND resolution = Unresolved AND assignee in (currentUser()) ' \
            'AND NOT (status in ("10000", "10406", "10001", "3", "10401", "10400") ' \
            'AND issuetype != "10000" AND status not in ("10001") AND (cf[10004] is EMPTY ' \
            'OR cf[10004] not in futureSprints() AND cf[10004] not in openSprints())) ORDER BY key ASC'

    queryObj = JiraApi.JiraIssues(token_file)
    
    issues = queryObj.get_open_issues(story_query)
    data = queryObj.build_issue_key_map(issues)
    
    # Specify the file name
    file_name = 'subtask_data.json'

    # Open the file for writing
    with open(file_name, 'w') as json_file:
        # Write the JSON data to the file
        json.dump(data, json_file, indent=4)

    # process_json(data)




