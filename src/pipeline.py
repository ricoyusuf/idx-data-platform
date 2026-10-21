from src.extract.download_stock import download_stock
from src.validation.validate_stock import validate_stock
from src.transform.transform_stock import transform_stock
from src.load.load_stock import load_stock
from src.load.db_setup import setup_database
from pathlib import Path
import logging

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)

def run_pipeline(ticker):
    try:
        logger.info("Starting pipeline for %s", ticker)

        # First attempt: normal download
        stock_data = download_stock(ticker, repair=False)
        logger.info("Initial download completed for %s", ticker)

        is_valid = (
            not stock_data.empty
            and validate_stock(stock_data)
        )

        # Retry with yfinance repair if initial data is invalid
        if not is_valid:
            logger.warning(
                "Initial validation failed for %s. Retrying with repair=True.",
                ticker,
            )

            stock_data = download_stock(ticker, repair=True)

            is_valid = (
                not stock_data.empty
                and validate_stock(stock_data)
            )

            if not is_valid:
                logger.error(
                    "Validation failed after repair for %s. "
                    "No raw data saved.",
                    ticker,
                )
                return False

            logger.info(
                "Validation passed after repair for %s",
                ticker,
            )

            if "Repaired?" in stock_data.columns:
                repaired_count = int(
                    stock_data["Repaired?"]
                    .fillna(False)
                    .sum()
                )

                logger.info(
                    "yfinance marked %d repaired rows for %s",
                    repaired_count,
                    ticker,
                )
        else:
            logger.info(
                "Initial validation passed for %s",
                ticker,
            )

        # Save only the data that passed validation
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        raw_path = RAW_DIR / f"{ticker}.csv"
        stock_data.to_csv(raw_path, index=False)

        logger.info("Accepted extract saved to %s", raw_path)

        df = transform_stock(stock_data)
        logger.info("Transform completed for %s", ticker)

        load_stock(df, ticker)
        logger.info("Load completed for %s", ticker)

        return True

    except Exception:
        logger.exception("Pipeline failed for %s", ticker)
        return False

    
def run_all_stocks(tickers):
    log = {}
    for ticker in tickers:
        log[ticker] = run_pipeline(ticker)
    return log

TICKERS = ["BBCA", "BBRI", "BMRI", "TLKM","ANTM","AUTO","LSIP","ESSA"]    

if __name__ == "__main__":
    setup_database()

    result = run_all_stocks(TICKERS)
    failed_tickers = []

    for ticker, status in result.items():
        if status:
            print(ticker, ": SUCCESS")
        else:
            print(ticker, ": FAILED")
            failed_tickers.append(ticker)

    if failed_tickers:
        logger.error(
            "Pipeline failed for tickers: %s",
            ", ".join(failed_tickers)
        )
        raise SystemExit(1)

    logger.info(
        "All %d tickers processed successfully",
        len(result)
    )