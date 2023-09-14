import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ..data.loader import DataSchemaSentiment
from . import ids


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    all_days: list[str] = data[DataSchemaSentiment.DAY].tolist()
    unique_days = sorted(set(all_days))

    @app.callback(
        Output(ids.DAYS_DROPDOWN, "value"),
        [
            Input(ids.SELECT_ALL_DAYS_BUTTON, "n_clicks"),
        ],
    )
    def select_all_days(_: int) -> list[str]:
        return unique_days

    return html.Div(
        children=[
            html.H6("Days"),
            dcc.Dropdown(
                id=ids.DAYS_DROPDOWN,
                options=[{"label": days, "value": days} for days in unique_days],
                value=unique_days,
                multi=True,
            ),
            html.Button(
                className="dropdown-button",
                children=["Select All"],
                id=ids.SELECT_ALL_DAYS_BUTTON,
                n_clicks=0,
            ),
        ]
    )
