#!/usr/bin/env python3
import JiraApi

if __name__ == '__main__':
    token_file = '.local/share/jira_tokens/pull_scripts.json'
    
    queryObj = JiraApi.JiraPull(token_file)
    
    issues = queryObj.get_open_issues()
    data = JiraApi.JiraIssues.build_issue_key_map(issues)
    
    queryObj.dump_to_file(data)




