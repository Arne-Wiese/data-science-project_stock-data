import pandas as pd
from dash import Dash, html, dcc
from src.components import (
    bar_chart_event,
    bar_chart_sector,
    chart_dropdown_event,
    chart_dropdown_sector,
    days_dropdown,
    event_date_picker,
    event_dropdown,
    line_chart_event,
    line_chart_sentiment,
    sector_dropdown,
    sector_heatmap,
)


def create_layout(app: Dash, sentiment_data: pd.DataFrame, sector_data: pd.DataFrame,
                  event_data: pd.DataFrame, sector_wide_data: pd.DataFrame) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            dcc.Tabs(
                id="tabs",
                value="home-tab",  # Default tab to display
                children=[
                    dcc.Tab(
                        label="Home",
                        value="home-tab",
                        children=[
                            html.P("Hello")
                        ],
                    ),
                    dcc.Tab(
                        label="Prediction Model",
                        value="prediction-tab",
                        children=[
                            html.P("Hello")
                        ],
                    ),
                    dcc.Tab(
                        label="Economic Indicators and Country Performance",
                        value="economic-tab",
                        children=[
                            html.P("Hello")
                        ],
                    ),
                    dcc.Tab(
                        label="Sentiment Analysis",
                        value="sentiment-tab",
                        children=[
                            html.Div(
                                className="dropdown-container",
                                children=[
                                    days_dropdown.render(app, sentiment_data),
                                ],
                            ),
                            line_chart_sentiment.render(app, sentiment_data),
                        ],
                    ),
                    dcc.Tab(
                        label="Sector Correlation",
                        value="sector-tab",
                        children=[
                            html.Div(
                                className="dropdown-container",
                                children=[
                                    sector_dropdown.render(app, sector_data),
                                    chart_dropdown_sector.render(),
                                ],
                            ),
                            bar_chart_sector.render(app, sector_data),
                            sector_heatmap.render(app, sector_wide_data)
                        ],
                    ),
                    dcc.Tab(
                        label="Event Analysis",
                        value="event-tab",
                        children=[
                            html.Div(
                                className="dropdown-container",
                                children=[
                                    event_dropdown.render(app, event_data),
                                    event_date_picker.render(),
                                    chart_dropdown_event.render(),
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
