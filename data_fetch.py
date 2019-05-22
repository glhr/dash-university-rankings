from utils import *


def fetch_THE_rankings():
    file_paths = {
                'THE_world_university_rankings_2019.json':'https://www.timeshighereducation.com//sites//default//files//the_data_rankings//world_university_rankings_2019_limit0_7216a250f6ae72c71cd09563798a9f18.json',
                'THE_world_university_rankings_2018.json':'https://www.timeshighereducation.com//sites//default//files//the_data_rankings//world_university_rankings_2018_limit0_369a9045a203e176392b9fb8f8c1cb2a.json'
    }

    data = {}
    for file_name, url in file_paths.items():
        file_path = 'data/'+file_name
        if not file_exists(file_path):
            download_json_file(file_path, url)

        data[file_name.split('.')[0]] = load_json_file(file_path)['data']

    return data


def fetch_uni_websites():
    return load_json_file('data/uni_websites.json')

