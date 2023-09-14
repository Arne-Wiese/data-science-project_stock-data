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
            Input(ids.CHART_DROPDOWN, "value"),
        ],
    )
    def update_bar_chart_event(
        symbols: list[str], date: str, chart: str,
    ) -> html.Div:
        if chart == 'Bar':
            filtered_data = data.query(
                "symbol in @symbols"
            )

            if filtered_data.shape[0] == 0:
                return html.Div("No data selected.", id=ids.BAR_CHART_EVENT)

            filtered_data['Date'] = pd.to_datetime(filtered_data['date'])
            # Define the event date
            event_date = pd.to_datetime(date)

            # Create a new column 'Before/After' to indicate whether the date is before or after the event
            filtered_data['Before/After'] = filtered_data['Date'].apply(
                lambda x: 'Before' if x < event_date else 'After')
            
            one_year_before_event = event_date - pd.DateOffset(years=1)
            one_year_after_event = event_date + pd.DateOffset(years=1)

            # Filter the DataFrame to include only data within one year before and after the event
            filtered_data = filtered_data[
                (filtered_data['Date'] >= one_year_before_event) & 
                (filtered_data['Date'] <= one_year_after_event)
            ]

            def create_pivot_table() -> pd.DataFrame:
                pt = filtered_data.pivot_table(
                    values=DataSchemaEvent.PRICE, index=[DataSchemaEvent.SYMBOL, 'Before/After'], aggfunc='sum')
                return pt.reset_index().sort_values(DataSchemaEvent.PRICE, ascending=False)
            
            fig = px.bar(
                create_pivot_table(),
                x=DataSchemaEvent.SYMBOL,
                y=DataSchemaEvent.PRICE,
                color='Before/After',
                labels={DataSchemaEvent.SYMBOL: 'Symbol', DataSchemaEvent.PRICE: 'Price'},
                color_discrete_sequence=['blue', 'orange'],
            )

            return html.Div(dcc.Graph(figure=fig), id=ids.BAR_CHART_EVENT)
        else:
            return html.Div(id=ids.BAR_CHART_EVENT)
        
    return html.Div(id=ids.BAR_CHART_EVENT)
