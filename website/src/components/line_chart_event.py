import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ..data.loader import DataSchemaEvent
from . import ids


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    @app.callback(
        Output(ids.LINE_CHART_EVENT, "children"),
        [
            Input(ids.EVENTS_DROPDOWN, "value"),
            Input(ids.EVENT_DATE_PICKER, "date"),
            Input(ids.CHART_DROPDOWN, "value")
        ],
    )
    def update_line_chart_event(
        symbols: list[str], date: str, chart: str,
    ) -> html.Div:
        if chart == 'Line':     
            filtered_data = data.query(
                "symbol in @symbols"
            )

            if filtered_data.shape[0] == 0:
                return html.Div("No data selected.", id=ids.LINE_CHART_EVENT)
            
            def create_traces(symbols: list[str]):
                traces = []
                # Create a trace for each symbol
                for symbol in symbols:
                    symbol_data = filtered_data[filtered_data[DataSchemaEvent.SYMBOL] == symbol]
                    trace = go.Scatter(
                        x=symbol_data[DataSchemaEvent.DATE],
                        y=symbol_data[DataSchemaEvent.PRICE],
                        mode='lines',
                        name=f'{symbol}'  # Use the symbol as the trace name
                    )
                    traces.append(trace)
                return traces


            # Create a layout
            layout = go.Layout(
                title='Public Sentiment Analysis with Nvidia Stock',
                xaxis=dict(title='Date'),
                yaxis=dict(title='Normalized Values')
            )

            traces = create_traces(symbols)

            fig = go.Figure(data=traces, layout=layout)
            fig.update_layout(margin={"t": 40, "b": 0, "l": 0, "r": 0})
            
            # Add a vertical dotted line at '2020-01-01'
            event_date = date
            fig.add_shape(
                go.layout.Shape(
                    type="line",
                    x0=event_date,
                    x1=event_date,
                    y0=0,
                    y1=1,
                    xref="x",
                    yref="paper",  # Sets the y-coordinate in relative coordinates
                    line=dict(
                        color="red",  # Color of the line
                        width=1,  # Line width
                        dash="dot",  # Line style (dotted)
                    ),
                )
            )

            return html.Div(dcc.Graph(figure=fig), id=ids.LINE_CHART_EVENT)
        else:
            return 

    return html.Div(id=ids.LINE_CHART_EVENT)