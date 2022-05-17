# Pulse

A simple application with live charts, API and datafeed generation. Specially for **Skanestas**. 

## Prerequisites

You need Docker to run this demo. If you have none - you can run it locally manually, see **Manual run** section below.

## How to run it

First, **make a local copy** of the repository, e.g. `git pull` it.

### Running Docker style

Copy `.env.example` file to `.env`, fill in settings required with values you like, or just leave defaults.

Build a docker image:
```shell
docker build -t pulse-demo .
```

Run a docker image:
```shell
docker run --rm -it -p 8050:8050 pulse-demo
```

Point your favorite browser to `http://127.0.0.1:8050/`. You should see a simple app. Pick a ticker - and enjoy watching the chart evolution.

That's it! Happy testing.

### Manual run

Run `RUN python pulse/db.py` once to creat DB and schema. It won't hurt if you run it twice, no worries.

Run `python pulse/pulse.py` to launch data generator.

Next, run `uvicorn api.main:app --host 0.0.0.0 --port 8000` to start API service.

Finally, run simple web server with `python gui/main.py` and go to `http://127.0.0.1:8050/` to see the result.


## Components

### Datafeed generator

Our stock exchange, which supplies data on assets and prices.

Located under `pulse` folder. Powered by stock python components.

Creates 100 sample tickers and updates their prices each second (configurable). Data is stored in **SQlite** database.
* `db.py` - DB initialization, DB query helper
* `pulse.py` - business logic

Data is held in single table with fields for ticker name, price and timestamp.

### API

Our broker, which provides users with stock exchange data. Powered by `fastapi` and `uvicorn`, with `databases` package for the convenience of work with DB.

Located under `api` folder. Supports endpoints:
* get ticker list with metadata (not used currently) - total amount of records, oldest and latest timestamps
* get recent tickers (400 by default, configurable)
* get tickers since some timestamp

There is no need to use API in this sample app, as we can access DB directly. Still, we'll need it in real world.

For endpoints, request and response format reference, please take a look at `http://127.0.0.1:8000/redoc` (do not forget to map port `8000` from a container beforehand).

### Front-end

User interface and data visualization. Powered by `plotly dash` with some additional components. `pandas` is used, but not necessary.

Located under `gui` folder. Implemented as single-page application. Provided functionality:
* ticker selection dropdown
* slider to select amount of last ticks to fetch (400 by default) - set it before selecting a ticker
* chart area with live update

When chart is updated, only fresh data is transferred to front-end. That makes chart updates nearly instant.

Feel free to use browser developer tools and check what's going on.

#### Caveat

When selecting another ticker, under certain conditions chart may seem to be frozen and not updating. **Double click chart area** to make it work again. This is related to area scaling of Plotly component used.

## Things not done
* sophisticated tests and 100% coverage
* docstrings and comments
* deployment and testing pipelines
* models for DB and API
* support for DB schema and data migrations
* standalone DBMS in separate container
* OHLCV data generator with realistic logic
* validations of requests and responses on API and GUI side
* pagination of API results
* flexible configuration
* async API requests
* multi-worker multi-thread production-ready deployment
* debug is still on - just to make it simple to check there are no errors
* more data on charts
* pretty looking UI styling and theming

## Who's done that?

https://www.linkedin.com/in/perfontana/