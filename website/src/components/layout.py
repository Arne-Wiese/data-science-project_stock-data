import pandas as pd
from dash import Dash, html, dcc
from src.components import (
    bar_chart_event,
    bar_chart_sector,
    chart_dropdown,
    days_dropdown,
    event_date_picker,
    event_dropdown,
    line_chart_event,
    sector_dropdown,
    line_chart,
)


def create_layout(app: Dash, sentiment_data: pd.DataFrame, sector_data: pd.DataFrame,
                  event_data: pd.DataFrame) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            dcc.Tabs(
                id="tabs",
                value="line-tab",  # Default tab to display
                children=[
                    dcc.Tab(
                        label="Line Chart",
                        value="line-tab",
                        children=[
                            html.Div(
                                className="dropdown-container",
                                children=[
                                    days_dropdown.render(app, sentiment_data),
                                ],
                            ),
                            line_chart.render(app, sentiment_data),
                        ],
                    ),
                    dcc.Tab(
                        label="Bar Chart",
                        value="bar-tab",
                        children=[
                            html.Div(
                                className="dropdown-container",
                                children=[
                                    sector_dropdown.render(app, sector_data),
                                ],
                            ),
                            bar_chart_sector.render(app, sector_data),
                        ],
                    ),
                    dcc.Tab(
                        label="Event Chart",
                        value="event-tab",
                        children=[
                            html.Div(
                                className="dropdown-container",
                                children=[
                                    event_dropdown.render(app, event_data),
                                    event_date_picker.render(),
                                    chart_dropdown.render(),
                                ],
                            ),
                            line_chart_event.render(app, event_data),
                            bar_chart_event.render(app, event_data),
                        ],
                    ),
                ],
            ),
        ],
    )
