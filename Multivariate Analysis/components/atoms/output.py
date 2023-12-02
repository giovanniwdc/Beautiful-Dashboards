from dash import html, dash_table

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


def dataTable(df, npages=5): 

    style_table={
        'overflowX': 'auto', 
        'width':'100%', 
        "height":"100%",
        "border-radius": "1vw",
    }

    style_cell = {
        "border":"none",
        "border-bottom":"solid rgba(0,0,0,0.1) 0.1vw",
    }

    style_data={
        "background-color":"rgba(0,0,0,0)",
        "text-align":"center"

    }

    style_header={
        "border-bottom":"solid rgba(0,0,0,0.1) 0.1vw",
        'fontWeight': 'bold',
        "text-align":"center",
        "padding-left":"1vw",
        "padding-right":"1vw"
    }

    return dash_table.DataTable(
        df.to_dict('records'), 
        [{"name": i, "id": i} for i in df.columns],
        page_size=npages, 
        style_table=style_table,
        style_cell=style_cell,
        style_data=style_data,
        style_header=style_header,
        css=[
            { 'selector': '.previous-next-container', 'rule': 'position:absolute; right:0;' },
            {'selector':'.cell-table, .dash-table-container, .dt-table-container__row-1, .dash-fixed-content', 'rule':'height:100%;'}
        ],
    )