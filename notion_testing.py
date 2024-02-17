from RestApiBase import dump_to_file
from NotionApi import *

if __name__ == '__main__':
    token_file = token_file = '.local/share/jira_tokens/notion.json'

    query_obj = QueryUsers(token_file)
    data = query_obj.get_users()
    # dump_to_file(data)

    data = query_obj.get_user("c57caec9-cbf2-4f92-99c9-525a33320eff")
    dump_to_file(data)

    search_obj = SearchNotion(token_file)
    data = search_obj.search()
    # dump_to_file(data)