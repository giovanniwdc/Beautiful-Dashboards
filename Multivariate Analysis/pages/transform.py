import dash
from dash import dcc, html, Input, Output, State,  callback, dash_table

import pandas as pd

dash.register_page(__name__)

layout = html.Div(
    [   

        html.P('Inicio'),
        
    ]
)

