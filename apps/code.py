import dash_core_components as dcc
import dash_html_components as html

app_name = 'dash-university_rankings'

layout = html.Div([
    dcc.SyntaxHighlighter(language='python',
                          children=open('apps/main.py', 'r').read()),
])
