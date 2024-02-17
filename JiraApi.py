#!/usr/bin/env python3

from RestApiBase import *

class JiraApi(ApiBase):
    def __init__(self, file_path):
        # Make sure URL does not end with /
        super().__init__(file_path)

    @ApiBase.headers.setter
    def headers(self, token):
        self._headers = {
            'Authorization' : f'Bearer {token}',
            "Accept" : "application/json"
        }
        
    def query_issue(self, method, id_or_key, resource='', fields=[], expand=[]):
        query = {
            'fields' : fields,
            'expand' : expand
        }
        return self.retrieve_json(method, f"issue/{id_or_key}/{resource}")
        

    def send_jql_query(self, query='', fields=[], expand=[]):
        # Pass a JQL query to Jira and return the result
        query = {
            'jql' : query,
            'fields' : fields,
            'expand' : expand
        }

        return self.get("search", payload=query)
    
# Have JiraPull and JiraPush inherit, have JiraIssues process with composition
class JiraPull(JiraApi):
    def __init__(self, file_path, issue_fields=None, expand=None):
        super().__init__(file_path)
        self.issue_fields = issue_fields
        self.expand = expand

    def get_open_issues(self, query=None):
        data = self.send_jql_query(query, self.issue_fields, self.expand)
        issues = data['issues']

        issues = self.get_subtasks_for_issues(issues)
        return issues
    
    def get_subtasks_for_issues(self, issues):
        for issue in issues:
            subtasks = issue["fields"]["subtasks"]
            for i, subtask in enumerate(subtasks):
                subtask_issue = self.query_issue("GET", subtask["id"])
                subtasks[i] = subtask_issue
        return issues