from datetime import datetime

import plotly.express as px
from dash import Dash, Input, Output, State, callback_context, dcc, html
from dash.exceptions import PreventUpdate
from dash_extendable_graph import ExtendableGraph

from gui.utils import ApiSchema, api_response, get_prices_dataframe

app = Dash(__name__)

raw_tickers = api_response(ApiSchema.tickers, {}, 'tickers')
tickers = {t['ticker']: t for t in raw_tickers}

app.layout = html.Div(children=[
    html.H1(children='Hello Skanestas!'),
    html.H3(children='The pulse of fake tickers for your pleasure and relaxation'),
    dcc.Dropdown(list(tickers), id='ticker-dropdown'),
    dcc.Input(id='amount-input', type='range',  min=100, max=3600, step=100, value=400),
    html.Div(id='amount-info'),
    ExtendableGraph(id='prices-graph'),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,
        n_intervals=0
    ),
])


@app.callback(
    Output('amount-info', 'children'),
    Input('amount-input', 'value'),
)
def update_amount(amount):
    return f'Fetch {amount} latest values when new ticker chosen'


@app.callback(
    Output('prices-graph', 'figure'),
    Input('ticker-dropdown', 'value'),
    State('amount-input', 'value')
)
def load_chart(ticker, amount):
    if not callback_context.triggered:
        raise PreventUpdate  # no actions on initial page load

    raw_prices = api_response(ApiSchema.latest, container='result', ticker=ticker, amount=amount)
    prices = get_prices_dataframe(raw_prices)

    fig = px.line(prices, x='ts', y='price', title=ticker)
    fig.update_layout(transition_duration=500)
    return fig


@app.callback(
    Output('prices-graph', 'extendData'),
    Input('interval-component', 'n_intervals'),
    State('ticker-dropdown', 'value'),
    State('prices-graph', 'figure'),
)
def extend_chart(intervals, ticker, figure):
    if ticker is None or figure is None:
        raise PreventUpdate
    if len(figure['data'][0]['x']):
        latest_ts = datetime.fromisoformat(figure['data'][0]['x'][-1]).timestamp()
    else:
        latest_ts = 0
    raw_prices = api_response(ApiSchema.since, container='result', ticker=ticker, latest_ts=latest_ts)
    prices = get_prices_dataframe(raw_prices)
    return [dict(x=prices['ts'], y=prices['price'])], [0]


if __name__ == '__main__':
    # TODO: disable debug in product environment
    app.run_server(debug=True)
