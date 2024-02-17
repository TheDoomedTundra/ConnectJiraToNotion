#!/usr/bin/env python3

from RestApiBase import *

class NotionBase(ApiBase):
    def __init__(self, file_path, resource):
        super().__init__(file_path)
        self.base_resource = resource

    @ApiBase.headers.setter
    def headers(self, token):
        self._headers = {
            'Authorization' : f'Bearer {token}',
            'Notion-Version' : "2022-06-28",
            "Content-Type": "application/json"
        }

    @property
    def base_resource(self):
        return self._base_resource

    @base_resource.setter
    def base_resource(self, val):
        self.url = self.build_url(val)
        self._base_resource = val

    def get_by_id(self, id):
        return self.get(id)

class SearchNotion(NotionBase):
    def __init__(self, file_path):
        super().__init__(file_path, 'search')

    def search(self, query=''):
        if query != '':
            query = json.dumps(query)
        return self.post(query)  
    
    def search_by_title(self, title):
        query = {
            "query": title
        }
        return self.search(query)
    
    def search_all_databases(self):
        query = {
            "filter": {
            "value": "page",
            "property": "object"
         }}
        return self.search(query)
    
    def search_all_pages(self):
        query = {
            "filter": {
            "value": "page",
            "property": "object"
         }}
        return self.search(query)  
    
    
class QueryPages(NotionBase):
    def __init__(self, file_path):
        super().__init__(file_path, 'pages')

    def get_page(self, page_id):
        return self.get_by_id(page_id)

class QueryDatabases(NotionBase):
    def __init__(self, file_path):
        super().__init__(file_path, 'databases')

    def get_database(self, database_id):
        return self.get_by_id(database_id)

class QueryUsers(NotionBase):
    def __init__(self, file_path):
        super().__init__(file_path, 'users')
     
    def get_users(self):
        return self.get()
    
    def get_user(self, user_id):
        return self.get_by_id(user_id)