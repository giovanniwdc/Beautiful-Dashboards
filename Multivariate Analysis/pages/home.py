import dash
from dash import dcc, html, Input, Output, State,  callback, dash_table, no_update

import dash_daq as daq

import dash_bootstrap_components as dbc

import plotly.express as px

import pandas as pd
import numpy as np
import json

from scripts.dataset import DataDict

from components.atoms.selectors import dropdown_item
from components.atoms.output import output_value, dataTable
from components.atoms.input import titled_input

from constants.home import *

from sklearn.model_selection import train_test_split

dash.register_page(__name__,external_stylesheets=EXTERNAL_STYLESHEETS, path='/')

with open(DATA_DIR+"/datasets.json",  encoding='utf-8') as file:
    datasetList = json.load(file)['datasets_list']

dataset_options=[{"label": meta["name"] , "value": i} for i, meta in enumerate(datasetList)]

def info(dataset=pd.DataFrame()):

    columns = dataset.columns
    nrows, ncolums = dataset.shape
    nones = dataset.isnull()
    nnones = np.sum(nones.values)
    max_nones_column = ""
    max_column_name = ""
    duplicated_rows = np.sum(dataset.duplicated())

    if nrows > 0:
        max_nones_column = np.argmax(nnones)
        max_column_name = columns[max_nones_column]

    return[
        html.Div([
            output_value(nrows, 'Rows: '),
            output_value(ncolums, 'Columns: '),
            output_value(nnones, 'None rows: '),
            output_value(max_column_name, 'Highest none: '),
            output_value(duplicated_rows, 'Duplicated rows: '),
            
        ], style={'display':'flex', 'flex':'1','flex-direction':'column', 'justify-content':'space-between', 'border-right':'solid rgba(0,0,0,0.1) 0.15vw', 'padding':'1vw'}),
        html.Div([

        ],style={'flex':'1'})
        
    ]

drop_down_menus = [dropdown_item(*menu.values()) for menu in DATASET_MENU_DROPDOWN]
dataset_selector=[
    dropdown_item("Dataset", dataset_options, "Select a dataset", "data-list-dropdown"),
    *drop_down_menus
]

dataset_info=info()

def dataset_menu_split(cat_columns:[str]=[], columns:[str]=[]):
    
    stratify_options = [{'label': 'Nothing', 'value':'Nothing'}] + [{'label':column, 'value':column} for column in cat_columns]
    order_options = [{'label': 'Nothing', 'value':'Nothing'}] + [{'label':column, 'value':column} for column in columns]

    return [
        html.Div([
            html.Div("Percentage of training, test and validation", className="title", style={"margin-bottom":"0.5vw"}),
            dcc.RangeSlider(
                50, 
                100, 
                value=[50, 75], 
                allowCross=False, 
                pushable=10, 
                tooltip={"placement": "bottom", "always_visible": True},
                marks={i: f"{i}%" for i in range(50, 105, 5)},
                id='split-range-slider'
            )
        ], className="sliders"),
        dropdown_item("Stratify by: ", stratify_options, "column", "column-dropdown-stratify", value='Nothing', maxHeight=100, clearable=True),
        dropdown_item("Order by: ", order_options, "column", "column-dropdown-order", value='Nothing', maxHeight=100, clearable=True),
        html.Div([
            titled_input("Seed", "split-seed", "number", "a seed", 42, min=0, step=1),
            html.Button('Create', id='submit-create-dataset'),
            dcc.Download(id="download-dataframe-train-csv"),
            dcc.Download(id="download-dataframe-test-csv"),
            dcc.Download(id="download-dataframe-outofsample-csv"),
            html.Button('Save', id='submit-save-dataset', disabled=True)
        ], style={'flex':'row', 'display':'flex', 'justify-content':'space-between'}),



        
    ]

dataset_split=dataset_menu_split()

modal_error=dbc.Modal([
    dbc.ModalHeader("More information about selected row"),
    dbc.ModalBody(id="modal-content"),
    dbc.ModalFooter(dbc.Button("Close", id="close", className="ml-auto")),
],id="modal-error")


def get_categories(df:pd.DataFrame, limit:int=10):

    return [column for column in df.columns if df[column].unique().shape[0] <= limit]



def distribution_menu(columns=[None], categories=[None]):

    column_options=[{'label': column, 'value': column} for column in columns if column != None]
    categorical_options=[{'label': column, 'value': column} for column in categories if column != None]

    return [
        dropdown_item("", column_options, "Column", "home-graph-x-dropdown", size="100%",value=columns[0]),
        dropdown_item("", categorical_options, "Column", "home-graph-y-dropdown", size="100%",value=categories[0], clearable=True),
        dropdown_item("", categorical_options, "Column", "home-graph-color-dropdown", size="100%",value=categories[0], clearable=True),
        html.Div([
            daq.BooleanSwitch(on=False, label="LogX", labelPosition="top", id="distribution-menu-logx"),
            daq.BooleanSwitch(on=False, label="Flip", labelPosition="top", id="distribution-menu-flip")
        ], style={'display':'flex', 'flex-direction':'row', 'justify-content':'space-between', 'font-weight':'500'})
        
    ]


# layout of the home page
layout = html.Div([
    
    #top menu
    html.Div([
        html.Div(dataset_selector, className="left-component"),
        html.Div([], className="right-component", id="dataset-show")
    ], className="top-menu row"),
    
    # bottom menu
    html.Div([
        html.Div(dataset_info, className='left-component', id="data-info"),
        html.Div([
            html.Div([
                dcc.Graph(figure={}, id='home-distribution-graph', className="graph", style={'width': '74%', 'height': '100%','margin':'0'}),
                html.Div(distribution_menu(), className="menu", id="distribution-menu")
            ],className="distribution"),
            html.Div(dataset_split, id="data-split-menu")
        ], className="right-component")
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
    Output("distribution-menu", "children"),

    # stratify menu output
    Output("data-split-menu", "children"),

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
        
        return dataTable(df), no_update, no_update, info(df), distribution_menu(df.columns, get_categories(df)), dataset_menu_split(get_categories(df), df.columns)
    
    except UnicodeDecodeError as error:
         
        return [], True, html.Div(['Oiii']), no_update, no_update, no_update

@callback(
    Output("modal-error", "is_open"),
    Input("close", "n_clicks"),
    prevent_initial_call=True
)
def close_modal(a):
    return False, no_update

@callback(
    Output("home-distribution-graph", "figure"),
    Input("home-graph-x-dropdown", "value"),
    Input("home-graph-y-dropdown", "value"),
    Input("home-graph-color-dropdown", "value"),
    Input("distribution-menu-logx", "on"),
    Input("distribution-menu-flip", "on"),
    prevent_initial_call=True
)
def update_graph(col_x, col_y, color, logx, flip):
    data_dict = DataDict()
    df = data_dict.get_dataset('df')

    if flip:
        temp=col_x
        col_x=col_y
        col_y=temp

    fig = px.histogram(df, x=col_x, y=col_y, color=color, histnorm='percent')
    fig.update_traces(marker_line_width=1, marker_line_color="rgba(0,0,0,0.5)")
    
    if logx:
        if flip ^ bool(col_y != None):
            fig.update_xaxes(type="log", range=[0,5]) 
        else:
            fig.update_yaxes(type="log", range=[0,5])

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0, pad=0),
        hovermode='closest',
        plot_bgcolor='rgba(0,0,0,0)',
    )

    return fig

@callback(
    Output('input-split-seed', 'value'),
    Output("submit-save-dataset", 'disabled'),
    Input('submit-create-dataset', 'n_clicks'),
    State('input-split-seed',  'value'),
    State('split-range-slider', 'value'),
    State('column-dropdown-stratify', 'value'),
    State('column-dropdown-order', 'value'),

    prevent_initial_call=True
)
def split_dataset(_, seed, range, stratify, order):

    seed = np.round(np.abs(seed))
    np.random.seed(seed)

    data_dict = DataDict()
    df = data_dict.get_dataset('df').copy()

    nrows, _ = df.shape
    
    train_range, test_range =  range

    out_of_sample = 100 - (train_range + test_range)
    n_out_of_sample = int(out_of_sample/100*nrows)

    if order != 'Nothing':
        df = df.sort_values(by=[order])

    df_out_of_sample = df.iloc[-n_out_of_sample:].copy()

    if stratify != 'Nothing':
        X_train, X_test, = train_test_split( df, test_size=test_range/100, random_state=seed, stratify=df[stratify])
    else:
        X_train, X_test, = train_test_split( df, test_size=test_range/100, random_state=seed)

    data_dict.add_dataset('df_outofsample', df_out_of_sample)
    data_dict.add_dataset('df_train',X_train)
    data_dict.add_dataset('df_test',X_test)

    return 42, False

@callback(
    Output("download-dataframe-train-csv", "data"),
    Output("download-dataframe-test-csv", "data"),
    Output("download-dataframe-outofsample-csv", "data"),
    Input("submit-save-dataset", "n_clicks"),
    prevent_initial_call=True,
)
def download_train_test_csv(n_clicks):
    data_dict = DataDict()

    df_train = data_dict.get_dataset('df_train')
    df_test = data_dict.get_dataset('df_test')
    df_outofsample = data_dict.get_dataset('df_outofsample')

    return dcc.send_data_frame(df_train.to_csv, "train.csv"), dcc.send_data_frame(df_test.to_csv, "test.csv"), dcc.send_data_frame(df_outofsample.to_csv, "outofsample.csv")