from src.extract.download_stock import download_stock
from src.validation.validate_stock import validate_stock
from src.transform.transform_stock import transform_stock
from src.load.load_stock import load_stock

def run_pipeline(ticker):
    print(f"Starting pipeline for {ticker}")

    download_stock(ticker)
    print("Extract completed")

    if validate_stock(ticker):
        print("Validation passed")

        df = transform_stock(ticker)
        print("Transform completed")

        load_stock(df, ticker)
        print("Load completed")
    else:
        print("Validation failed. Pipeline stopped.")

if __name__ == "__main__":
    run_pipeline("BBCA")