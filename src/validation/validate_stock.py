import pandas as pd
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"

def validate_stock(df):
    required_columns = [
    "Date",
    "Close",
    "High",
    "Low",
    "Open",
    "Volume"
    ]

    return (df.isna().sum().sum() == 0 
            and df.duplicated().sum() == 0 
            and set(required_columns).issubset(df.columns))
    
if __name__ == "__main__":
    result = validate_stock("BBCA")
    print("Validation result: ", result)