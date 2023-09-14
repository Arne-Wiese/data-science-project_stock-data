import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ..data.loader import DataSchemaEvent
from . import ids


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    all_symbols: list[str] = data[DataSchemaEvent.SYMBOL].tolist()
    unique_symbols = sorted(set(all_symbols))

    @app.callback(
        Output(ids.EVENTS_DROPDOWN, "value"),
        [
            Input(ids.SELECT_ALL_EVENTS_BUTTON, "n_clicks"),
        ],
    )
    def select_all_events(_: int) -> list[str]:
        return unique_symbols

    return html.Div(
        children=[
            html.H6("Symbols"),
            dcc.Dropdown(
                id=ids.EVENTS_DROPDOWN,
                options=[{"label": symbols, "value": symbols} for symbols in unique_symbols],
                value=unique_symbols[:5],
                multi=True,
            ),
            html.Button(
                className="dropdown-button",
                children=["Select All"],
                id=ids.SELECT_ALL_EVENTS_BUTTON,
                n_clicks=0,
            ),
        ]
    )
