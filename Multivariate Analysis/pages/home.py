import dash
from dash import dcc, html, Input, Output, State,  callback, dash_table, no_update
import dash_bootstrap_components as dbc

import pandas as pd

import json

from scripts.dataset import DataDict

from constants.home import *

dash.register_page(__name__,external_stylesheets=EXTERNAL_STYLESHEETS, path='/')

with open(DATA_DIR+"/datasets.json",  encoding='utf-8') as file:
    datasetList = json.load(file)['datasets_list']

layout = html.Div(
    [   
        html.Div([
            html.Div([
                html.Div([
                    html.Span("Dataset", className="list-title"),
                    dcc.Dropdown(
                        options=[{"label": meta["name"] , "value": meta["file_name"]} for meta in datasetList],
                        searchable=False,
                        placeholder="Select a dataset",
                        id="data-list-dropdown",
                        className="dropdown",
                        clearable=False,
                    )
                ], className="item")
                ,
                html.Div([
                    html.Span("Delimiter", className="list-title"),
                        dcc.Dropdown(
                        options=[{"label": option, "value": DELIMITER_OPTIONS[option]} for option in DELIMITER_OPTIONS.keys()],
                        searchable=False,
                        placeholder="Select a delimiter",
                        id="delimiter-list",
                        className="dropdown",
                        clearable=False
                    )
                ], className="item")
                ,
                html.Div([
                    html.Span("Decimal", className="list-title"),
                    dcc.Dropdown(
                        options=[{"label": option, "value": DECIMAL_OPTIONS[option]} for option in DECIMAL_OPTIONS.keys()],
                        searchable=False,
                        placeholder="Select a decimal",
                        id="decimal-list",
                        className="dropdown",
                        clearable=False
                    )
                ], className="item")
                ,
                html.Div([
                    html.Span("Encoding", className="list-title"),
                    dcc.Dropdown(
                        options=[{"label": option, "value": ENCODING_OPTIONS[option]} for option in ENCODING_OPTIONS.keys()],
                        searchable=False,
                        placeholder="Select a encoding",
                        id="encoding-list",
                        className="dropdown",
                        clearable=False
                    )
                ], className="item")   
            ],className="menu"),

            html.Div([

            ], id="dataset-show")
        ], className="dataset"),
        html.Div([
            
        ], className="data-options"),
        
        
        dbc.Modal(
            [
                dbc.ModalHeader("More information about selected row"),
                dbc.ModalBody(id="modal-content"),
                dbc.ModalFooter(dbc.Button("Close", id="close", className="ml-auto")),
            ],
            id="modal-error",
        ),
    ],
    className="home"
)

@callback(
    Output("dataset-show", "children"),
    Output("modal-error", "is_open", allow_duplicate=True,),
    Output("modal-content", "children"),
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
    
    try:
        data_dict.add_dataset('df', pd.read_csv(DATA_DIR+selected_data_path, sep=sep, decimal=decimal, encoding=encoding, engine="python"))
        df = data_dict.get_dataset('df')

        return html.Div([
            dash_table.DataTable(
                df.to_dict('records'), [{"name": i, "id": i} for i in df.columns],
                page_size=5, 
                style_table={'overflowX': 'auto', 'width':'68vw', "height":"100%"}
            )
        ], className="dataframe"), no_update, no_update
    
    except UnicodeDecodeError as error:
         
        return [], True, html.Div(['Oiii'])

    return [], no_update, no_update

@callback(
    Output("modal-error", "is_open"),
    Input("close", "n_clicks"),
    prevent_initial_call=True
)
def close_modal(a):
    return False, no_update

