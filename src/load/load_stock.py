from pathlib import Path
from src.transform.transform_stock import transform_stock
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"


def load_stock(ticker):
    df = transform_stock(ticker)
    df[["Date","Close","Previous Close","Daily Gain","Daily Return","MA_5","MA_20","Trend","Distance_MA20","MA20_Category"]].to_csv(PROCESSED_DIR / f"{ticker}_processed.csv" ,index=False)
    print(f"{ticker} loaded successfully.")
if __name__ == "__main__":
    load_stock("BBCA")