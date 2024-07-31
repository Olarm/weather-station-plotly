from datetime import date, datetime, timedelta

from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd


from data import get_data

df2 = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')
df = get_data()

app = Dash()

app.layout = [
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    #dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
    dcc.Dropdown(df.keys()[2:], 'T_out', id='dropdown-selection'),
    dcc.Graph(id='graph-content'),
    dcc.DatePickerSingle(
        month_format='Do, MMM YY',
        placeholder='Do, MMM YY',
        min_date_allowed=date(2022, 1, 1),
        max_date_allowed=date.today(),
        date=date.today() - timedelta(days=1),
        id='date-from'
    ),
    dcc.DatePickerSingle(
        month_format='Do, MMM YY',
        placeholder='Do, MMM YY',
        min_date_allowed=date(2022, 1, 1),
        max_date_allowed=date.today(),
        date=date.today() - timedelta(days=1),
        id='date-to'
    ),
]

@callback(
    Output('graph-content', 'figure'),# Output('output-container-date-picker-single', 'children')],
    [Input('dropdown-selection', 'value'), Input('date-from', 'date'), Input('date-to', 'date')]
)
def update_graph(value, date_from, date_to):
    date_from = datetime.strptime(date_from, "%Y-%m-%d").date()
    date_to = datetime.strptime(date_to, "%Y-%m-%d").date()
    df = get_data(date_from)
    #dff = df[df.country==value]
    #return px.line(dff, x='year', y='pop')
    return px.line(df, x='timestamp', y=value)

#@callback(
#    Output('output-container-date-picker-single', 'children'),
#    Input('date-from', 'date')
#)
#def update_output(selected_date):
#    return f'Selected date: {selected_date}'

if __name__ == '__main__':
    app.run(debug=True)
