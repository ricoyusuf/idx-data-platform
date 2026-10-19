from src.analysis.query import (
    get_stock_by_ticker,
    get_latest_stocks,
)


def test_get_stock_by_ticker():
    columns, rows = get_stock_by_ticker("BBCA")
    ticker_index = columns.index("ticker")
    assert all(row[ticker_index] == "BBCA" for row in rows)

def test_get_latest_stocks():
    columns, rows = get_latest_stocks()
    ticker_index = columns.index("ticker")
    tickers = [row[ticker_index] for row in rows]
    assert len(tickers) == len(set(tickers))