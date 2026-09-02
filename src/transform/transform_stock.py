from pathlib import Path
import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"

def transform_stock(ticker):

    df = pd.read_csv(DATA_DIR / f"{ticker}.csv", parse_dates=["Date"])
    df["Previous Close"] = df["Close"].shift(1)
    df["Daily Gain"] = df["Close"] - df["Previous Close"]
    df["Daily Return"] = ((df["Close"] - df["Previous Close"])/ df["Previous Close"]) * 100

    df["MA_5"] = df["Close"].rolling(window=5).mean()
    df["MA_20"] = df["Close"].rolling(window=20).mean()


    df["Trend"] = np.where(
        df["MA_20"].isna(),
        "No Signal",
        np.where(df["Close"] > df["MA_20"],
        "Above MA20",
        "Below MA20"
        )
    )

    df["Distance_MA20"] = ((df["Close"] - df["MA_20"]) / df["MA_20"]) * 100

    conditions = [
        df["Distance_MA20"] < -2,
        (df["Distance_MA20"] >= -2) & (df["Distance_MA20"] <= 2),
        df["Distance_MA20"] > 2
    ]

    categories = ["Far Below MA20", "Near MA20", "Far Above MA20"]
    df["MA20_Category"] = np.select(conditions,categories,default="No Signal")

    return df


if __name__ == "__main__":
    df = transform_stock("BBCA")
    print(df.tail())