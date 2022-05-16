import random
import time

from db import query


class Ticker:
    def __init__(self, name, price=0):
        self.name: str = name
        self.price: int = price

    def update_price(self):
        """Generate next price."""
        self.price += random.choice((-1, 1))
        return self.price


class Pulse:
    def __init__(self, freq: int = 1, tickers: int = 100, prefix: str = 'ticker_'):
        self.tickers: list = [None] * tickers
        self._freq = freq  # update frequency, seconds
        width = len(f'{tickers-1}')  # calculate leading zeroes count, log(tickers) is slower :)
        for index in range(tickers):
            name = f'{prefix}{index:0{width}d}'
            self.tickers[index] = Ticker(name)

    def shine(self):
        while True:
            values = []
            for ticker in self.tickers:
                new_price = ticker.update_price()
                ts = time.time()
                values.append((ticker.name, ts, new_price))
            query(
                # use qmark style for unsafe values!
                'INSERT INTO ohlc_data VALUES (?, ?, ?)',
                param=values
            )
            time.sleep(self._freq)


if __name__ == '__main__':
    Pulse().shine()
