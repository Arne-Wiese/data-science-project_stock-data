import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ..data.loader import DataSchemaSector, sectors_dict
from . import ids

def render(app: Dash, data: pd.DataFrame) -> html.Div:
    all_sectors: list[str] = data[DataSchemaSector.SECTOR].tolist()
    unique_sectors = sorted(set(all_sectors))

    @app.callback(
        Output(ids.SECTORS_DROPDOWN, "value"),
        [
            Input(ids.SELECT_ALL_SECTORS_BUTTON, "n_clicks"),
        ],
    )
    def select_all_sectors(_: int) -> list[str]:
        return unique_sectors

    return html.Div(
        children=[
            html.H6("Sectors"),
            dcc.Dropdown(
                id=ids.SECTORS_DROPDOWN,
                options=[{"label": sectors, "value": sectors} for sectors in unique_sectors],
                value=unique_sectors,
                multi=True,
            ),
            html.Button(
                className="dropdown-button",
                children=["Select All"],
                id=ids.SELECT_ALL_SECTORS_BUTTON,
                n_clicks=0,
            ),
        ]
    )