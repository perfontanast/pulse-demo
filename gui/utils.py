import json
from enum import Enum

import pandas as pd
import requests
from dash.exceptions import PreventUpdate


class ApiSchema(Enum):
    tickers: str = 'http://127.0.0.1:8000/api/v1/tickers'
    latest: str = 'http://127.0.0.1:8000/api/v1/ticker/{ticker}/latest/{amount}'
    since: str = 'http://127.0.0.1:8000/api/v1/ticker/{ticker}/since/{latest_ts}'


def api_response(endpoint: ApiSchema | str, default=None, container: str = None, **kwargs):
    url = endpoint.value
    if kwargs:
        url = url.format(**kwargs)
    response = requests.get(url)  # TODO: should validate API response in real world
    if not response.ok:
        if default is not None:
            return default
        raise PreventUpdate
    raw_result = json.loads(response.text)
    if container is not None:
        return raw_result[container]
    return raw_result


def get_prices_dataframe(raw_prices):
    prices = pd.DataFrame(raw_prices)
    if prices.empty:
        raise PreventUpdate
    prices['ts'] = pd.to_datetime(prices['ts'], unit='s', utc=True).dt.ceil(freq='us')
    return prices
