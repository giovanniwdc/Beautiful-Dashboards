from dash import Dash, html, dcc, callback, Output, Input,  State
from dash.exceptions import PreventUpdate

import plotly.express as px

#from pages import home

import pandas as pd

EXTERNAL_STYLESHEETS = ["/app.css"]

app = Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS)

PATHS={
    'Home': '/',
    'Transformações':'/transformations',
    'Redução de Dimensionalidade':'/dimentional_reduction',
    'Análise Fatorail':'factor_analysis ',
    'Análise de Correlações Canônicas':'canonical_correlation',
    'Agrupamentos':'clustering'
}

buttons = [dcc.Link(title, href=path) for title, path in zip(PATHS.keys(), PATHS.values())]

app.layout = html.Div(
    [
        html.Div([
            html.P('Multivariate Analysis'),
            html.Div(buttons, id='menuBar')
        ], className='header'),
        html.Div([], className='main', id='page_content'),
        html.Footer([]),
        dcc.Location(id='url', refresh=False)
    ],
    className='content'
)

@callback(
    Output('page_content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathanme):

    if pathanme == '/': 
        return 'home.layout'
    else:
        return '404'

if __name__ == '__main__':
    app.run(debug=True)
