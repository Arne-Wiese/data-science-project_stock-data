from dash import dcc, html
from . import ids


def render() -> html.Div:
    return html.Div(
        children=[
            html.H6("Chart Style"),
            dcc.Dropdown(
                id=ids.CHART_DROPDOWN_EVENT,
                options=['Line', 'Bar'],
                value='Line',
                multi=False,
            ),
        ]
    )