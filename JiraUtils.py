from JiraApi import *
from JiraIssues import *


def pull_active_stories(token_file):
    # TODO: Don't do by issuetype, just query to get sub-tasks AND stories
    story_query = 'resolution = Unresolved AND assignee in (currentUser()) ' \
            'AND NOT (status in ("10000", "10406", "10001", "3", "10401", "10400") ' \
            'AND issuetype != "10000" AND status not in ("10001") AND (cf[10004] is EMPTY ' \
            'OR cf[10004] not in futureSprints() AND cf[10004] not in openSprints())) ORDER BY key ASC'
    # data = map_subtasks_to_stories(token_file, story_query)
    issues = JiraPull(token_file).get_open_issues(story_query)
    return issues

def pull_issue_backlog(token_file):
    backlog_query = ''
    data = map_subtasks_to_stories(token_file, backlog_query)

def map_subtasks_to_stories(token_file, query):
    issues = JiraPull(token_file).get_open_issues(query)
    data = JiraIssues.build_issue_key_map(issues)

# Heirarchy for issues in the Jira results for open story, returned as a list:
# list[0]["key"] = key OR ["id"]
# list[0]["fields"] = fields
# fields["summary"] = title of issue
# fields["issuetype"]["name"] = type of issue
# fields["parent"]["id"] or ["key"] - use to map to other issue
# fields["worklog"]["worklogs"]
# fields["subtasks"] = list of subtasks
# for subtask in fields["subtasks"]:
#       subtask["key"]
#       fields["assignee"]["name"] - ensure belongs to me
#       fields["status"]["name"] - status name
#       fields["worklog"]["worklogs"]
#       fields["issuetype"]["name"] 
#       fields["issuetype"]["subtask"] - boolean on whether or not it is
#       fields["project"]["name"]
        # fields["summary"]
        # fields["upadeted"] - last update
# fields["status"]["name"]
# Don't need to iterate through subtasks with this method
