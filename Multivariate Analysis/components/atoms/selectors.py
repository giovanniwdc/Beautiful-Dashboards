from dash import dcc, html, Input, Output, State,  callback, dash_table, no_update

def dropdown_item(title, options, placeholder, id, size="18vw", value=None, clearable=False, maxHeight=150):

    style={
        "display":"flex",
        "flexDirection":"row",

        "width":"100%",
        
        "justify-content":"space-between"
    }

    container_style={
        "width": size,
    }

    input_title={
        "font-weight":"500"
    }

    return html.Div([
        html.Span(title, className="title", style=input_title),
        dcc.Dropdown(
            options=options,
            searchable=False,
            placeholder=placeholder,
            id=id,
            value=value,
            maxHeight=maxHeight,
            className="dropdown",
            clearable=clearable,
            style=container_style)
    ], className="dropdown-item", style=style)