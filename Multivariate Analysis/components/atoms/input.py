from dash import dcc, html

def titled_input(title="", id="", type="text", placeholder="", value=None, width="10vw", width_box="5vw", min=None, max=None, step=None):

    style={
        "display":"flex",
        "flex-direction":"row",
        "justify-content":"space-between",
        "align-items":"center",
        "width":width
    }

    input_style={
        "border": "solid rgba(0,0,0,0.1) 0.15vw",
        "border-radius": "0.2vw",
        "width":width_box,
        "text-align":'center'
    }

    input_title={
        "font-weight":"500",
        
    }

    return html.Div([
        html.Div(f"{title}", className="title", style=input_title ),
        dcc.Input(
            id=f"input-{id}",
            type=type,
            placeholder=f"Enter with {placeholder}",
            value=value,
            style=input_style,
            min=min,
            max=max,
            step=step 
        )
    ], className="titled_input", style=style,)



