import pandas as pd
from dash import Dash, dcc, html
from . import ids


def render() -> html.Div:
    return html.Div(
        children=[
            html.H6("Chart Style"),
            dcc.Dropdown(
                id=ids.CHART_DROPDOWN,
                options=['Line', 'Bar'],
                value='Line',
                multi=False,
            ),
        ]
    )