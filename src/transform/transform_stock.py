import pandas as pd
import numpy as np
df = pd.read_csv("./data/BBCA.csv", parse_dates=["Date"])
df["Previous Close"] = df["Close"].shift(1)
df["Daily Gain"] = df["Close"] - df["Previous Close"]
df["Daily Return"] = ((df["Close"] - df["Previous Close"])/ df["Previous Close"]) * 100


# returns = []
# for x in range(len(df["Close"])): 
#     result = (df["Close"].iloc[x] - df["Previous Close"].iloc[x] ) / df["Previous Close"].iloc[x] * 100
#     if pd.isna(result) :
#         result = 0
#     returns.append(result)
# df["Daily Return"] = returns

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
print(df[["Date", "Close", "MA_20", "Distance_MA20", "MA20_Category"]].tail(10))
# print (df[["Date","Close","Previous Close","Daily Gain","Daily Return","MA_5","MA_20","Trend","Distance_MA20"]].head())
# print (df[["Date","Close","Previous Close","Daily Gain","Daily Return","MA_5","MA_20","Trend","Distance_MA20"]].tail())
df[["Date","Close","Previous Close","Daily Gain","Daily Return","MA_5","MA_20","Trend","Distance_MA20","MA20_Category"]].to_csv("./data/processed/BBCA_processed.csv" ,index=False)