import dash
from dash import dcc, html, Input, Output, State,  callback, dash_table
from collections import OrderedDict


import json
from scripts.dataset import Dataset

DATA_DIR = './datasets'
EXTERNAL_STYLESHEETS = ['/assets/home.css']


dataset = Dataset()

dash.register_page(__name__,external_stylesheets=EXTERNAL_STYLESHEETS, path='/')

with open(DATA_DIR+"/datasets.json",  encoding='utf-8') as file:
    datasetList = json.load(file)['datasets_list']

layout = html.Div(
    [   
        dcc.Dropdown(
            options=[{"label": meta["name"] , "value": meta["file_name"]} for meta in datasetList],
            searchable=False,
            placeholder="Select a dataset",
            id="data-list-dropdown"
        ),
        html.Div([

        ], id="dataset-show"),
        
        html.Div(id='output-data-upload')
    ]
)

@callback(
    Output("dataset-show", "children"),
    Input("data-list-dropdown", "value"), 
    prevent_initial_call=True
)
def update_dataset(selected_data_path):

    df = Dataset(DATA_DIR+selected_data_path).getData()

    return html.Div([
        dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns], page_size=10)
    ])