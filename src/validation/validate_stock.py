import pandas as pd

df = pd.read_csv("./data/BBCA.csv", parse_dates=["Date"])

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