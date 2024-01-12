#!/usr/bin/env python3

import json
import os
import requests
import time

class ApiBase:
    file_name = 'for_debug.json'

    def __init__(self, file_path):
        home_path = os.path.expanduser('~')
        self.token_path = os.path.join(home_path, file_path)
        self.read_token_file()
        self.headers = {
            'Authorization' : 'Bearer ' + self.token,
            "Accept" : "application/json"
        }

    def build_url(self, resource):
        return f"{self.url}/{resource}"

    def read_token_file(self):
        with open(self.token_path) as f:
            data = json.load(f)

        self.url = data["url"]
        self.token = data['token']
    
    def send_query(self, method, url, params=None):
        response = requests.request(method,url,headers=self.headers,params=params)

        # Handle REST rate limit
        if response.status_code == 429:
            delay = int(response.headers['retry-after']) * 2
            print(f'Rate limit hit, sleeping {delay} seconds...')
            time.sleep(delay) 
            return self.send_query(method, url, params)
            
        if response.status_code == 200:
            return response
        else:
            raise Exception(f"Error: {response.status_code} - {response.reason}")
        
    def dump_to_file(self, data, file=file_name):
        # Open the file for writing
        with open(file, 'w') as json_file:
            # Write the JSON data to the file
            json.dump(data, json_file, indent=4)