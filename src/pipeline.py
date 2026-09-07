from src.extract.download_stock import download_stock
from src.validation.validate_stock import validate_stock
from src.transform.transform_stock import transform_stock
from src.load.load_stock import load_stock
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"

def run_pipeline(ticker):
    try:
        print(f"Starting pipeline for {ticker}")

        stock_data = download_stock(ticker)
        
        print("Extract completed")

        if validate_stock(stock_data):
            print("Validation passed")
            RAW_DIR.mkdir(parents=True, exist_ok=True)
            stock_data.to_csv(RAW_DIR / f"{ticker}.csv",index=False)
            print(f"Raw data saved: {RAW_DIR}")
            df = transform_stock(stock_data)
            print("Transform completed")

            load_stock(df, ticker)
            print("Load completed")
            return True
        else:
            print("Validation failed. Pipeline stopped.")
            return False
    except Exception as e:
        print(f"{ticker} failed: {e}")
        return False

    
def run_all_stocks(tickers):
    log = {}
    for ticker in tickers:
        log[ticker] = run_pipeline(ticker)
    return log

TICKERS = ["BBCA", "BBRI", "BMRI", "TLKM"]    
if __name__ == "__main__":
    result = run_all_stocks(TICKERS)
    for ticker, status in result.items():
        if status:
            print(ticker, ": SUCCESS")
        else:
            print(ticker, ": FAILED")