from dash import dcc, html

from . import ids

def render() -> html.Div:
    return html.Div([
        html.H6("Select Event Date"),
        dcc.DatePickerSingle(
            id=ids.EVENT_DATE_PICKER,
            date='2020-03-11',
            display_format='YYYY-MM-DD',
        ),
        html.P("One interesting event is the first COVID-19 lockdown. It happened on March 11, 2020.\
               In the United Kingdom it was announced on March 23, 2020."),
    ])
