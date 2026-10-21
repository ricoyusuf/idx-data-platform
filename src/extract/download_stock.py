import yfinance as yf 
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"

def download_stock(ticker, repair=False):
    stock_data = yf.download(
        f"{ticker}.JK",
        repair=repair,
        progress=False,
    )

    if stock_data is None:
        return pd.DataFrame(
            columns=["Date", "Close", "High", "Low", "Open", "Volume"]
        )

    stock_data.columns = stock_data.columns.get_level_values(0)
    stock_data = stock_data.reset_index()

    return stock_data

if __name__ == "__main__":
    download_stock("BBCA")