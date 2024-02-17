#!/usr/bin/env python3
from abc import ABC, abstractmethod
import json
import os
import requests
import time

file_name = 'for_debug.json'

class ApiBase(ABC):
    def __init__(self, file_path):
        home_path = os.path.expanduser('~')
        self.token_path = os.path.join(home_path, file_path)
        self.read_token_file()
        self.headers = self.token

    @property
    def headers(self):
        return self._headers

    @headers.setter
    @abstractmethod
    def headers(self, val):
        ...

    def build_url(self, resource=''):
        return f"{self.url}/{resource}"

    def read_token_file(self):
        with open(self.token_path) as f:
            data = json.load(f)

        self.url = data["url"]
        self.token = data['token']
    
    def send_query(self, method, url, payload=None):
        if method == "GET":
            response = requests.get(url,headers=self.headers,params=payload)
        elif method == "POST":
            response = requests.post(url,headers=self.headers,data=payload)

        # Handle REST rate limit
        if response.status_code == 429:
            delay = int(response.headers['retry-after']) * 2
            print(f'Rate limit hit, sleeping {delay} seconds...')
            time.sleep(delay) 
            return self.send_query(method, url, payload)
            
        if response.status_code == 200:
            return response
        else:
            raise Exception(f"Error: {response.status_code} - {response.text}")
    
    def retrieve_json(self, method, resource='', payload=None):
        url = self.build_url(resource)
        response = self.send_query(method, url, payload)
        return response.json()
    
    def get(self, resource='', payload=None):
        return self.retrieve_json("GET", resource, payload)
    
    def post(self, resource='', payload=None):
        return self.retrieve_json("POST", resource, payload)
        
def dump_to_file(data, file=file_name):
    # Open the file for writing
    with open(file, 'w') as json_file:
        # Write the JSON data to the file
        json.dump(data, json_file, indent=4)