import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ..data.loader import DataSchemaSentiment
from . import ids


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    @app.callback(
        Output(ids.LINE_CHART_SENTIMENT, "children"),
        [
            Input(ids.DAYS_DROPDOWN, "value"),
        ],
    )
    def update_line_chart_sentiment(
        days: list[str]
    ) -> html.Div:
        filtered_data = data.query(
            "day in @days"
        )

        if filtered_data.shape[0] == 0:
            return html.Div("No data selected.", id=ids.PIE_CHART)

        trace1 = go.Scatter(
            x=filtered_data[DataSchemaSentiment.DATE],
            y=filtered_data[DataSchemaSentiment.STOCK],
            mode='lines',
            name='Nvidia Stock Price'
        )

        trace2 = go.Scatter(
            x=filtered_data[DataSchemaSentiment.DATE],
            y=filtered_data[DataSchemaSentiment.SENTIMENT],
            mode='lines',
            name='Sentiment'
        )

        trace3 = go.Scatter(
            x=filtered_data[DataSchemaSentiment.DATE],
            y=filtered_data[DataSchemaSentiment.SENTIMENT_SHIFTED],
            mode='lines',
            name='Sentiment Shifted'
        )

        # Create a layout
        layout = go.Layout(
            title='Public Sentiment Analysis with Nvidia Stock',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Normalized Values')
        )

        fig = go.Figure(data=[trace1, trace2, trace3], layout=layout)
        fig.update_layout(margin={"t": 40, "b": 0, "l": 0, "r": 0})

        return html.Div(dcc.Graph(figure=fig), id=ids.LINE_CHART_SENTIMENT)

    return html.Div(id=ids.LINE_CHART_SENTIMENT)
