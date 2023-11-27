from dash import dcc, html, Input, Output, State,  callback, dash_table, no_update

def dropdown_item(title, options, placeholder, id):

    style={
        "display":"flex",
        "flexDirection":"row",

        "width":"100%",
        
        "justify-content":"space-between"
    }

    container_style={
        "width": "18vw"
    }

    return html.Div([
        html.Span(title, className="title"),
        dcc.Dropdown(options=options,searchable=False,placeholder=placeholder, id=id, className="dropdown", clearable=False, style=container_style)
    ], className="dropdown_item", style=style)