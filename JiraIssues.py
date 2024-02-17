# File and/or class for processing Jira Issues

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