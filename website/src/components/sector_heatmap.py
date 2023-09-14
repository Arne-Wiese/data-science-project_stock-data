import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ..data.loader import DataSchemaSectorAnalyis, sectors_dict
from . import ids

def render(app: Dash, data: pd.DataFrame) -> html.Div:
    @app.callback(
        Output(ids.HEATPMAP_CHART_SECTOR, "children"),
        [
            Input(ids.SECTORS_DROPDOWN, "value"),
            Input(ids.CHART_DROPDOWN_SECTOR, "value")
        ],
    )
    def update_line_chart_event(
        sectors: list[str], chart: str,
    ) -> html.Div:
        if chart == 'Heatmap':
            # Create the correlation heatmap
            filtered_data = data.query("symbol in @sectors")

            if filtered_data.shape[0] == 0:
                return html.Div("No data selected.", id=ids.HEATPMAP_CHART_SECTOR)
            
            pivoted_df = filtered_data.pivot(index=DataSchemaSectorAnalyis.DATE,
                                              columns=DataSchemaSectorAnalyis.SYMBOL,
                                                values=DataSchemaSectorAnalyis.PRICE)
            correlation_matrix = pivoted_df.corr()
            
            # Rename the columns in the correlation_matrix DataFrame
            correlation_matrix.rename(columns=sectors_dict, inplace=True)

            # Create a heatmap using Plotly Express
            fig = px.imshow(
                correlation_matrix,
                x=correlation_matrix.columns,
                y=correlation_matrix.columns,
                color_continuous_scale='Jet',
            )

            fig.update_layout(
                title='Correlation Heatmap between Symbols',
                xaxis_title='Symbols',
                yaxis_title='Symbols',
                width=800,  # Adjust the width as needed
                height=600,  # Adjust the height as needed
            )  

            return html.Div(dcc.Graph(figure=fig), id=ids.HEATPMAP_CHART_SECTOR,
                            style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'})
        else:
            return html.Div(id=ids.HEATPMAP_CHART_SECTOR)
    
    return html.Div(id=ids.HEATPMAP_CHART_SECTOR)