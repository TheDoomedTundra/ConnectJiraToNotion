#!/usr/bin/env python3

from RestApiBase import *

class JiraApi(ApiBase):
    def __init__(self, file_path):
        # Make sure URL does not end with /
        super().__init__(file_path)

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
    
# Have JiraPull and JiraPush inherit, have JiraIssues process with composition
class JiraPull(JiraApi):
    story_query = 'issuetype = Story AND resolution = Unresolved AND assignee in (currentUser()) ' \
            'AND NOT (status in ("10000", "10406", "10001", "3", "10401", "10400") ' \
            'AND issuetype != "10000" AND status not in ("10001") AND (cf[10004] is EMPTY ' \
            'OR cf[10004] not in futureSprints() AND cf[10004] not in openSprints())) ORDER BY key ASC'

    def __init__(self, file_path):
        super().__init__(file_path)
        self.issue_fields = ["issuetype", "summary", "status", "subtasks", "worklog"]
        self.expand = ["changelog"]

    def get_open_issues(self, query=story_query):
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
        
    
class JiraIssues():
    def __init__(self) -> None:
        pass

    @staticmethod
    def process_issue(issue):
        fields = issue["fields"]
        issue_type = fields["issuetype"]["name"]

        issue_data = {
            "type": issue_type,
            "summary": fields["summary"],
            "status": fields["status"]["name"],
            "id": issue["id"],
            "worklogs": JiraIssues.process_worklog(fields["worklog"]),
            "lastupdated": None,
            "subtasks": {}
        }

        if issue_type == "Story":
            last_update = issue["changelog"]["histories"][-1]["created"]
            for subtask in fields["subtasks"]:
                subtask_data = JiraIssues.process_issue(subtask)
                issue_data["subtasks"][subtask["key"]] = subtask_data
        else:
            last_update = fields["updated"]

        issue_data["lastupdated"] = last_update

        return issue_data

    @staticmethod
    def build_issue_key_map(issues):
        issue_map = {}
        for issue in issues:
            # Map issue keys to issue objects
            issue_key = issue["key"]
            issue_data = JiraIssues.process_issue(issue)
            issue_map[issue_key] = issue_data
        
        return issue_map
    
    @staticmethod
    def process_worklog(worklog):
        time_spent = 0
        for log in worklog["worklogs"]:
            time_spent += log["timeSpentSeconds"]

        return time_spent