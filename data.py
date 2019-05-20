import requests
import os
import json
import pandas as pd
from colour import RGB_color_picker

file_paths = {'world_university_rankings_2019.json':'https://www.timeshighereducation.com//sites//default//files//the_data_rankings//world_university_rankings_2019_limit0_7216a250f6ae72c71cd09563798a9f18.json',
              'world_university_rankings_2018.json':'https://www.timeshighereducation.com//sites//default//files//the_data_rankings//world_university_rankings_2018_limit0_369a9045a203e176392b9fb8f8c1cb2a.json'}
data = {}

for file_path, url in file_paths.items():
    if not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
        print('Downloading JSON file')
        response_ranking = requests.get(url)

        with open(file_path, 'wb') as unis_json:
            unis_json.write(response_ranking.content)

    with open(file_path,'r') as unis_json:
        data[file_path.split('.')[0]] = json.load(unis_json)['data']


pd.set_option('display.expand_frame_repr', False)
df_currentyear = pd.DataFrame.from_dict(data['world_university_rankings_2019'])
df_currentyear.set_index('name', inplace=True)

df_lastyear = pd.DataFrame.from_dict(data['world_university_rankings_2018'])
df_lastyear.set_index('name', inplace=True)

df_merged = df_currentyear.combine_first(df_lastyear)
df_merged.drop(columns=['aliases'], inplace=True)
df_merged[['rank','rank_order']] = df_merged[['rank','rank_order']].apply(pd.to_numeric, errors='ignore')
df_merged = df_merged.sort_values('rank_order')


def compute_ratio(ratio_str):
    """
    Parameter:
        a string of the following format (two whole numbers separated by a colon): '50 : 50'
    Returns:
        if the format is valid, the division between the two integers as a float
        otherwise, None
    """
    try:
        ratio_split = ratio_str.split(' : ')
        return int(ratio_split[0])/int(ratio_split[1])
    except:
        return None


# compute numerical ratios from string representation (eg. '50 : 50')
df_merged['stats_female_male_ratio'] = df_merged['stats_female_male_ratio'].map(compute_ratio)

countries = df_merged.location.unique()
countries.sort()

# assign a color to each country
color_list = list(map(lambda c: RGB_color_picker(c).hex, countries))
color_lookup = dict(zip(countries, color_list))

# label for each column
stats = {'stats_number_students': 'Number of students',
         'stats_female_male_ratio': 'Female/Male ratio',
         'stats_student_staff_ratio': 'Student/Staff ratio',
         'stats_pc_intl_students': 'International students (%)',
         'scores_overall': 'Score: overall',
         'scores_teaching': 'Score: teaching',
         'scores_research': 'Score: research',
         'scores_industry_income': 'Score: industry income',
         'scores_international_outlook': 'Score: international outlook',
         'scores_citations': 'Score: citations',
         # 'rank': 'Rank',
         # 'rank_order': 'Rank order'
         }

# a set of all subjects offered (ensures uniqueness)
subjects_offered = list(set(i for i in df_merged["subjects_offered"].str.cat(sep=',').replace(', ', ',').split(',') if i))
subjects_offered.sort()
