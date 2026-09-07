import pandas as pd
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"

def validate_stock(df):

    print("Shape:", df.shape)

    print("\nMissing Values:")
    print(df.isna().sum())

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

    print("\nData Types:")
    print(df.dtypes)

    print("\nDate Range:")
    print("Start Date:", df["Date"].iloc[0])
    print("End Date:", df["Date"].iloc[-1])

    return df.isna().sum().sum() == 0 and df.duplicated().sum() == 0
    
if __name__ == "__main__":
    result = validate_stock("BBCA")
    print("Validation result: ", result)