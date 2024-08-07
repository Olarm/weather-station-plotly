from datetime import date, datetime, timedelta
import os

from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

from data import get_data


PRODUCTION = False
if os.getenv('FLASK_ENV') == 'development':
    print("Running in development mode")
elif os.getenv('FLASK_ENV') == 'production':
    print("Running in production mode with Gunicorn")
    PRODUCTION = True

df = get_data()

app = Dash()
server = app.server
app.title = "Rennodden"


app.layout = [
    html.H1(children='Rennodden værstasjon ved Dalskilen', style={'textAlign':'center'}),
    html.H4(children='(Under utbygging)', style={'textAlign':'center'}),
    dcc.Dropdown(df.keys()[2:], 'Temperatur ute', id='dropdown-selection'),
    html.Div(['Fra: ',
        dcc.DatePickerSingle(
            display_format='D/M/Y',
            month_format='Do, MMM YY',
            placeholder='Do, MMM YY',
            min_date_allowed=date(2022, 1, 1),
            max_date_allowed=date.today(),
            date=date.today() - timedelta(days=1),
            id='date-from'
        ),
        "Til: ",
        dcc.DatePickerSingle(
            display_format='D/M/Y',
            month_format='Do, MMM YY',
            placeholder='Do, MMM YY',
            min_date_allowed=date(2022, 1, 1),
            max_date_allowed=date.today(),
            date=date.today(),
            id='date-to'
        )],
        style={'fontSize': 20},
    ),
    dcc.Graph(id='graph-content'),
]

@callback(
    Output('graph-content', 'figure'),
    [Input('dropdown-selection', 'value'), Input('date-from', 'date'), Input('date-to', 'date')]
)
def update_graph(value, date_from, date_to):
    date_from = datetime.strptime(date_from, "%Y-%m-%d").date()
    date_to = datetime.strptime(date_to, "%Y-%m-%d").date()
    df = get_data(date_from, date_to)
    return px.line(df, x='timestamp', y=value)

if __name__ == '__main__':
    app.run(debug=PRODUCTION)
