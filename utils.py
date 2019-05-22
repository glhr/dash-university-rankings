import os
import json
import requests


def load_json_file(path):
    with open(path,'r') as f_json:
        return json.load(f_json)


def file_exists(path):
    if not os.path.isfile(path) or os.path.getsize(path) == 0:
        return False
    return True


def write_to_json_file(path, data):
    with open(path, 'wb') as f_json:
        f_json.write(data)


def download_json_file(path,url):
    print('Downloading JSON file')
    response = requests.get(url)
    write_to_json_file(path, response.content)

