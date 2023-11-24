import dash
from dash import dcc, html, Input, Output, State,  callback, dash_table

import json

import os

import pandas as pd
from scripts.dataset import Dataset

DATA_DIR = './datasets'
dataset = Dataset()

dash.register_page(__name__, path='/')

with open(DATA_DIR+"/datasets.json",  encoding='utf-8') as file:
    datasetList = json.load(file)['datasets_list']



layout = html.Div(
    [   
        html.H2('Inicio'),
        html.Div([

        ], className=""),
        dcc.Dropdown(
            options=[{"label": meta["name"] , "value": meta["file_name"]} for meta in datasetList],
            searchable=False,
            placeholder="Select a dataset",
            className="dataList"
        ),
        
        html.Div(id='output-data-upload')
    ]
)

