from dash import html

def output_value(value, title=""):

    style={
        "display":"flex",
        
        "flex-direcation":"row",
        "width":"100%",

        "justify-content":"space-between"
    }

    return html.Div([
        html.Span(title, className="title"),
        html.Span(f"{value}", className="value")
    ], className="output_value", style=style)

def output_text(text, title="", height="6vw"):

    style={
        "display":"flex",
        
        "flex-direction":"column",
        "width":"100%",

        "justify-content":"space-between",

    }

    return html.Div([
        html.Span(title, className="title", style={"border-bottom":"solid rgba(0,0,0,0.1) 0.1vw"}),
        html.Span(f"{text}", className="text", style={"overflow-y":"auto", "height":height})
    ], className="output_text", style=style)


