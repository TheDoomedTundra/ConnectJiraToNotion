#!/usr/bin/env python3

from RestApiBase import *

class QueryJira(ApiBase):
    def __init__(self, file_path):
        # Make sure URL does not end with /
        api_url = "https://api.notion.com"
        super().__init__(file_path, api_url)