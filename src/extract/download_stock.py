import yfinance as yf 
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"

def download_stock(ticker) :
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    stock_data = yf.download(f"{ticker}.JK")
    stock_data.columns = stock_data.columns.get_level_values(0)
    stock_data = stock_data.reset_index()
    
    return stock_data

if __name__ == "__main__":
    download_stock("BBCA")