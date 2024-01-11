#!/usr/bin/env python3

from RestApiBase import *

class JiraApi(ApiBase):
    def __init__(self, file_path):
        # Make sure URL does not end with /
        api_url = "https://jira.mathworks.com/rest/api/2"
        super().__init__(file_path, api_url)

    def query_issue(self, method, id_or_key, resource='', fields=[], expand=[]):
        url = self.build_url(f"issue/{id_or_key}/{resource}")

        query = {
            'fields' : fields,
            'expand' : expand
        }
        response = self.send_query(method, url)
        return response.json()

    def send_jql_query(self, query='', fields=[], expand=[]):
        # Pass a JQL query to Jira and return the result
        url = self.build_url("search")

        query = {
            'jql' : query,
            'fields' : fields,
            'expand' : expand
        }

        response = self.send_query("GET", url, params=query)
        return response.json()
    
# Use Composition for JiraIssues since it has a Jira API, but it's purpose is processing. 
# Have subtasks inherit from issues
class JiraIssues():
    def __init__(self, file_path):
        self.api = JiraApi(file_path)
        self.issue_fields = ["issuetype", "summary", "status", "subtasks", "worklog"]
        self.expand = ["changelog"]

    def get_open_issues(self, query):
        data = self.api.send_jql_query(query, self.issue_fields, self.expand)
        issues = data['issues']

        return issues

    def get_worklog(self, issue_id):
        worklogs = self.api.query_issue("GET", issue_id, "worklog")

        time_spent = 0
        for log in worklogs["worklogs"]:
            time_spent += log["timeSpentSeconds"]

        return time_spent
    
    def process_worklog(self, worklogs):
        time_spent = 0
        for log in worklogs["worklogs"]:
            time_spent += log["timeSpentSeconds"]

        return time_spent
    
    def process_issue(self, issue):
        issue_type = issue["fields"]["issuetype"]["name"]

        issue_data = {
            "type": issue_type,
            "summary": issue["fields"]["summary"],
            "status": issue["fields"]["status"]["name"],
            "id": issue["id"],
            "worklogs": self.process_worklog(issue["fields"]["worklog"]), # TODO: Doesn't work for sub-tasks
            "lastupdated": issue["changelog"]["histories"][-1]["created"],
            "subtasks": {}
        }

        if (issue_type != "Sub-task" and "subtasks" in issue["fields"]):
            num_subtasks = len(issue["fields"]["subtasks"])
            j = 1
            for subtask in issue["fields"]["subtasks"]:
                print(f"Processing subtask {j} of {num_subtasks}")
                issue = self.api.query_issue("GET", subtask["id"])
                subtask_data = self.process_issue(issue)
                j += 1
                issue_data["subtasks"][subtask["key"]] = subtask_data

        return issue_data

    def build_issue_key_map(self, issues):
        issue_map = {}
        num_issues = len(issues)
        i = 1
        for issue in issues:
            # Map issue keys to issue objects
            issue_key = issue["key"]
            print(f"Processing issue {i} of {num_issues}")
            i += 1
            issue_data = self.process_issue(issue)
            
            issue_map[issue_key] = issue_data
        
        return issue_map