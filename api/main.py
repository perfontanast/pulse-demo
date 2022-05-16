import os

from databases import Database
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

database = Database(f"sqlite:///{os.getenv('DB_FILE')}")

app = FastAPI()


@app.get('/api/v1/tickers')
async def tickers():
    query = (
        'SELECT ticker, COUNT(ticker) as total, min(ts) as min_ts, max(ts) as max_ts'
        ' FROM ohlc_data GROUP BY ticker ORDER BY ticker'
    )
    results = await database.fetch_all(query=query)
    return {'tickers': results}


@app.get('/api/v1/ticker/{ticker}/latest')
@app.get('/api/v1/ticker/{ticker}/latest/{count}')
async def latest(ticker: str, count: int = 1200):
    # TODO: pagination
    query = (
        'SELECT * FROM ohlc_data WHERE ticker = :ticker ORDER BY ts DESC LIMIT :count'
    )
    result = await database.fetch_all(query, {'ticker': ticker, 'count': count})
    return {'result': list(reversed(result))}


@app.get('/api/v1/ticker/{ticker}/since/{timestamp}')
async def since(ticker: str, timestamp: float):
    # TODO: pagination
    query = (
        'SELECT * FROM ohlc_data WHERE ticker = :ticker and ts > :timestamp ORDER BY ts'
    )
    result = await database.fetch_all(query, {'ticker': ticker, 'timestamp': timestamp})
    return {'result': result}
