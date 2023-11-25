import dash
from dash import dcc, html, Input, Output, State,  callback, dash_table
from collections import OrderedDict

import pandas as pd

import json
from scripts.dataset import Dataset, DataDict

DATA_DIR = './datasets'
EXTERNAL_STYLESHEETS = ['/assets/home.css']

DELIMITER_OPTIONS={
    ';':';',
    ',':',',
    "' '":""
}

DECIMAL_OPTIONS={
    ',':',',
    '.':'.'
}

ENCODING_OPTIONS={
    'Latin 1':'latin-1',
    'UTF-8':'utf-8'
}

dash.register_page(__name__,external_stylesheets=EXTERNAL_STYLESHEETS, path='/')

with open(DATA_DIR+"/datasets.json",  encoding='utf-8') as file:
    datasetList = json.load(file)['datasets_list']

layout = html.Div(
    [   
        html.Div([
            dcc.Dropdown(
                options=[{"label": meta["name"] , "value": meta["file_name"]} for meta in datasetList],
                searchable=False,
                placeholder="Select a dataset",
                id="data-list-dropdown"
            ),
            dcc.Dropdown(
                options=[{"label": option, "value": DELIMITER_OPTIONS[option]} for option in DELIMITER_OPTIONS.keys()],
                searchable=False,
                placeholder="Select a delimiter",
                id="delimiter-list"
            ),    
            dcc.Dropdown(
                options=[{"label": option, "value": DECIMAL_OPTIONS[option]} for option in DECIMAL_OPTIONS.keys()],
                searchable=False,
                placeholder="Select a decimal",
                id="decimal-list"
            ),    
            dcc.Dropdown(
                options=[{"label": option, "value": ENCODING_OPTIONS[option]} for option in ENCODING_OPTIONS.keys()],
                searchable=False,
                placeholder="Select a encoding",
                id="encoding-list"
            ),    
        ]),
        html.Div([
            
        ], className="data-options"),
        html.Div([

        ], id="dataset-show"),
        
        html.Div(id='output-data-upload')
    ]
)

@callback(
    Output("dataset-show", "children"),
    Input("data-list-dropdown", "value"), 
    Input("delimiter-list", 'value'),
    Input("decimal-list", 'value'),
    Input("encoding-list", 'value'),
    prevent_initial_call=True
)
def update_dataset(selected_data_path, sep:str=None, decimal:str=None, encoding:str=None):

    if decimal == None:
        decimal = ','

    data_dict = DataDict()
    data_dict.add_dataset('df', pd.read_csv(DATA_DIR+selected_data_path, sep=sep, decimal=decimal, encoding=encoding))
    
    df = data_dict.get_dataset('df')

    return html.Div([
        dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], page_size=10)
    ])