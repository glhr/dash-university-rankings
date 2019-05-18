import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from app import app
from dash.dependencies import Input, Output, State

import requests
import os
import json

app_name = 'dash-university_rankings'

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


plot_countries = {'France', 'Netherlands', 'Belgium', 'Denmark'}
plot_subjects = 'Electrical \u0026 Electronic Engineering'

df_currentyear=pd.DataFrame.from_dict(data['world_university_rankings_2019'])
df_currentyear.set_index('name',inplace=True)

df_lastyear=pd.DataFrame.from_dict(data['world_university_rankings_2019'])
df_lastyear.set_index('name',inplace=True)

df_merged = df_currentyear.combine_first(df_lastyear)

def compute_ratio(ratio_str):
    try:
        ratio_split = ratio_str.split(' : ')
        return int(ratio_split[0])/int(ratio_split[1])
    except:
        return None

df_merged['stats_female_male_ratio'] = df_merged['stats_female_male_ratio'].map(compute_ratio)

countries = df_merged.location.unique()

layout = html.Div([
    html.Div([html.H1("Times Higher Education - World University Rankings")], style={'textAlign': "center"}),
    html.Div([html.Div([dcc.Dropdown(id='value-selected', options=[{"label": i, 'value': i} for i in countries],
                                     value=["France"], multi=True)],
                       style={"display": "block", "margin-left": "auto", "margin-right": "auto", "width": "60%"})],
             className="row"),
    dcc.Graph(id="my-graph")], className="container")

plot_layout = go.Layout(
    autosize=False,
    width=1100,
    height=len(df_merged)*20,
    xaxis=dict(
        showgrid=False,
        showline=False,
        zeroline=False,
        side='top'
        # showticklabels = False,
        # domain=[0, 1]
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        zeroline=False,
        autorange='reversed'
        # showticklabels=False
    ),
    # paper_bgcolor='rgb(248, 248, 255)',
    # plot_bgcolor='rgb(248, 248, 255)',
    margin=dict(
        l=400,
        r=10,
        t=50,
        b=80
    ),
    showlegend=True,
)

@app.callback(Output("my-graph", "figure"), [Input("value-selected", "value")])
def update_graph(selected):
    dropdown = {i:i for i in countries}
    ctx = dash.callback_context
    trace = []
    df_updated = df_merged.loc[df_merged['location'].isin(selected)]
    # for value in selected:
    #     trace.append(go.Bar(x=df_merged[value], y=df_merged.index,
    #                             orientation='h',
    #                             # marker={"opacity": 0.7, 'size': 5, 'line': {'width': 0.5, 'color': 'white'}},
    #                             name=dropdown[value]),
    #                             )
    trace = [go.Bar(x=df_updated['stats_female_male_ratio'], y=df_updated.index,
                        orientation='h',
                        name='stats_female_male_ratio')]
    plot_layout['height'] = len(df_updated)*20
    figure = {"data": trace, "layout": plot_layout}
    return figure
