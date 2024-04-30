from dash import Dash, dcc, html, Input, Output, callback

app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    html.H1('This is an example'),
    dcc.Dropdown(['first', 'last', 'all'], 'choice', id='dropdown'),
    html.Div(id='display-value')
    ])

@callback(Output('display-value', 'children'), Input('dropdown', 'value'))
def display_value(value):
    return f'You have selected {value}'

if __name__ == '__main__':
    app.run(debug=True)
