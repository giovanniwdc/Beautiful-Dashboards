from dash import Dash, html, dcc, page_container


EXTERNAL_STYLESHEETS = ['/assets/app.css', '/assets/home.css']

app = Dash(__name__, external_stylesheets=EXTERNAL_STYLESHEETS, use_pages=True)

PATHS={
    'Home': '/',
    'Transform':'transform',
    'Analysis':'analysis',
    'Cluster':'cluster',
    'Factors':'factors'
}

buttons = [dcc.Link(title, href=path) for title, path in zip(PATHS.keys(), PATHS.values())]

app.layout = html.Div(
    [
        html.Div([
            html.P('Multivariate Analysis'),
            html.Div(buttons, id='menuBar')
        ], className='header'),
        html.Div([
            page_container
        ], className='main', id='page_content'),
        html.Footer([])
    ],
    className='content'
)

if __name__ == '__main__':
    app.run(debug=True)


