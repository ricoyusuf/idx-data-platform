from pathlib import Path
from src.load.db_loader import insert_stock_data

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"


def load_stock(df, ticker):
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df[["Date","Close","Previous Close","Daily Gain","Daily Return","MA_5","MA_20","Trend","Distance_MA20","MA20_Category"]].to_csv(PROCESSED_DIR / f"{ticker}_processed.csv" ,index=False)
    
    insert_stock_data(df, ticker)

    print(f"{ticker} loaded successfully.")