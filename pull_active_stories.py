#!/usr/bin/env python3

import json
import logging
import os
import requests
import sys

import JiraApi

if __name__ == '__main__':
    token_file = '.local/share/jira_tokens/pull_scripts.json'
    
    queryObj = JiraApi.JiraPull(token_file)
    
    issues = queryObj.get_open_issues()
    data = JiraApi.JiraIssues.build_issue_key_map(issues)
    
    queryObj.dump_to_file(data)




