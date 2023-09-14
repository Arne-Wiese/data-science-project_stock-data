import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ..data.loader import DataSchemaEvent
from . import ids


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    @app.callback(
        Output(ids.BAR_CHART_EVENT, "children"),
        [
            Input(ids.EVENTS_DROPDOWN, "value"),
            Input(ids.EVENT_DATE_PICKER, "date"),
        ],
    )
    def update_bar_chart_event(
        symbols: list[str], date: str
    ) -> html.Div:
        filtered_data = data.query(
            "symbol in @symbols"
        )

        filtered_data['Date'] = pd.to_datetime(filtered_data['date'])

        def calculate_metrics(data, event):
            avg_price_before_event = data[data['Date'] < pd.to_datetime(
                event)][DataSchemaEvent.PRICE].mean()
            std_dev_before_event = data[data['Date'] < pd.to_datetime(
                event)][DataSchemaEvent.PRICE].std()

            avg_price_after_event = data[data['Date'] >= pd.to_datetime(
                event)][DataSchemaEvent.PRICE].mean()
            std_dev_after_event = data[data['Date'] >= pd.to_datetime(
                event)][DataSchemaEvent.PRICE].std()

            return {
                'avg_price_before_event': avg_price_before_event,
                'std_dev_before_event': std_dev_before_event,
                'avg_price_after_event': avg_price_after_event,
                'std_dev_after_event': std_dev_after_event
            }

        if filtered_data.shape[0] == 0:
            return html.Div("No data selected.", id=ids.BAR_CHART_EVENT)

        date_one_year_before = pd.to_datetime(date) - pd.DateOffset(years=1)
        date_one_year_after = pd.to_datetime(date) + pd.DateOffset(years=1)

        x_values = []
        before_values = []
        after_values = []

        for stock_symbol in symbols:
            new_filtered_data = filtered_data[DataSchemaEvent.SYMBOL == stock_symbol][(filtered_data['Date'] >= date_one_year_before)
                                                                                      & (filtered_data['Date'] <= date_one_year_after)]
            metrics = calculate_metrics(new_filtered_data, date)
            avg_price_before = metrics['avg_price_before_event']
            avg_price_after = metrics['avg_price_after_event']

            x_values.append(stock_symbol)
            before_values.append(avg_price_before)
            after_values.append(avg_price_after)

        # Create a DataFrame from your data
        data = pd.DataFrame(
            {'Company': x_values, 'Before Event': before_values, 'After Event': after_values})

        # Create a Plotly Express bar chart figure
        fig = px.bar(
            data,
            x='Company',
            # Multiple bars for each company
            y=['Before Event', 'After Event'],
            labels={'Company': 'Company',
                    'value': 'Average Adjusted Closing Price ($)'},
            title='Average Adjusted Closing Price Before and After Event',
            color_discrete_sequence=['blue', 'orange'],  # Bar colors
        )

        # bar_chart_text = "The Bar Chart displays the average adjusted closing prices of selected stocks one year before and after a specified event date. It provides a visual comparison of how stock prices changed around the event."
        return html.Div(dcc.Graph(figure=fig), id=ids.BAR_CHART_EVENT)

    return html.Div(id=ids.BAR_CHART_EVENT)
