from utils import *
from bs4 import BeautifulSoup
import time
from tqdm import tqdm

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
    if not file_exists('data/uni_websites.json'):
        uni_websites = dict()

        url = 'http://www.shanghairanking.com/ARWU2018.html'

        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        sleep_time = 2
        for uni_link in tqdm(soup.select('#UniversityRanking a')):
            # print(uni_link)
            uni_name = uni_link.text

            if uni_name:
                uni_url = uni_link['href']
                # print(uni_url,uni_name)
                while sleep_time < 1000:
                    try:
                        time.sleep(sleep_time)
                        r = requests.get('http://www.shanghairanking.com/'+uni_url)
                        soup = BeautifulSoup(r.content, "html.parser")

                        link = soup.select('#tab1.tab_content a')
                        # print(link)
                        if len(link):
                            uni_websites[uni_name] = soup.select('#tab1.tab_content a')[0].text
                            print(uni_websites[uni_name])
                            break
                    except:
                        sleep_time *= 2
                        print('increasing sleep time')
                # request failed
                if not uni_name in uni_websites:
                    break

        write_dict_to_file(uni_websites, 'data/uni_websites.json')
    return load_json_file('data/uni_websites.json')
