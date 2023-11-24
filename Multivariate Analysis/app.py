import dash
from dash import Dash, html, dcc, callback, Output, Input,  State
from dash.exceptions import PreventUpdate

import plotly.express as px

import pandas as pd

EXTERNAL_STYLESHEETS = ['/assets/app.css']

app = Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS, use_pages=True)

PATHS={
    'Home': '/',
    'Transform':'transform',
    'Analysis':'analysis',
    'Cluster':'cluster',
    'Factors':'factors'
}

buttons = [dcc.Link(title, href=path) for title, path in zip(PATHS.keys(), PATHS.values())]

app.layout = html.Div(
    [
        html.Div([
            html.P('Multivariate Analysis'),
            html.Div(buttons, id='menuBar')
        ], className='header'),
        html.Div([
            dash.page_container
        ], className='main', id='page_content'),
        html.Footer([])
    ],
    className='content'
)

if __name__ == '__main__':
    app.run(debug=True)


