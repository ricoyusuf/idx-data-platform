import pandas as pd

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
print (df[["Date","Close","Previous Close","Daily Gain","Daily Return"]])
df[["Date","Close","Previous Close","Daily Gain","Daily Return"]].to_csv("./data/processed/BBCA_processed.csv")