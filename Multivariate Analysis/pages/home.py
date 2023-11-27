import dash
from dash import dcc, html, Input, Output, State,  callback, dash_table, no_update
import dash_bootstrap_components as dbc

import pandas as pd

import json

from scripts.dataset import DataDict

from components.atoms.selectors import dropdown_item
from components.atoms.output import output_value, output_text

from constants.home import *

dash.register_page(__name__,external_stylesheets=EXTERNAL_STYLESHEETS, path='/')

with open(DATA_DIR+"/datasets.json",  encoding='utf-8') as file:
    datasetList = json.load(file)['datasets_list']

dataset_options=[{"label": meta["name"] , "value": i} for i, meta in enumerate(datasetList)]

def info(dataset=pd.DataFrame()):

    return[
        output_value(dataset.shape[0], 'Nrows: '),
        output_value(dataset.shape[1], 'Ncolumns: '),
    ]

drop_down_menus = [dropdown_item(*menu.values()) for menu in DATASET_MENU_DROPDOWN]
dataset_selector=[
    dropdown_item("Dataset", dataset_options, "Select a dataset", "data-list-dropdown"),
    *drop_down_menus
]

dataset_info=info()

dataset_split=[
    html.Div([
        html.Span("Percentage of training", className="title"),
        dcc.Slider(
            50, 100, 5,
            value=60,
            id='train-slider',
        ),
    ], className="sliders"),
    html.Div([
        html.Span("Percentage of out of sample", className="title"),
        dcc.Slider(
            0, 50, 5,
            value=20,
            id='outofsample-slider',
        ),
    ], className="sliders")
]

modal_error=dbc.Modal([
    dbc.ModalHeader("More information about selected row"),
    dbc.ModalBody(id="modal-content"),
    dbc.ModalFooter(dbc.Button("Close", id="close", className="ml-auto")),
],id="modal-error")


# layout of the home page
layout = html.Div([
    
    #top menu
    html.Div([
        html.Div(dataset_selector, className="left-component"),
        html.Div([], className="right-component", id="dataset-show")
    ], className="top-menu row"),
    
    # bottom menu
    html.Div([
        html.Div(dataset_info, className="left-component", id="data-info"),
        html.Div(dataset_split, className="right-component")
    ], className="bottom-menu row"),

    # model error
    modal_error

], className="home")

@callback(
    Output("dataset-show", "children"),
    
    # modal output
    Output("modal-error", "is_open", allow_duplicate=True,),
    Output("modal-content", "children"),

    # info output
    Output("data-info", "children"),

    # dataset option inputs
    Input("data-list-dropdown", "value"), 
    Input("delimiter-list", 'value'),
    Input("decimal-list", 'value'),
    Input("encoding-list", 'value'),
    
    prevent_initial_call=True
)
def update_dataset(selected, sep:str=None, decimal:str=None, encoding:str=None, i=0):

    if decimal == None:
        decimal = ','

    data_dict = DataDict()

    try:
        data_dict.add_dataset('df', pd.read_csv(DATA_DIR+datasetList[selected]["file_name"], sep=sep, decimal=decimal, encoding=encoding, engine="python"))
        df = data_dict.get_dataset('df')
        
        return html.Div([
            dash_table.DataTable(
                df.to_dict('records'), [{"name": i, "id": i} for i in df.columns],
                page_size=5, 
                style_table={'overflowX': 'auto', 'width':'68vw', "height":"100%"}
            )
        ], className="dataframe"), no_update, no_update, info(df)
    
    except UnicodeDecodeError as error:
         
        return [], True, html.Div(['Oiii']), no_update

@callback(
    Output("modal-error", "is_open"),
    Input("close", "n_clicks"),
    prevent_initial_call=True
)
def close_modal(a):
    return False, no_update

