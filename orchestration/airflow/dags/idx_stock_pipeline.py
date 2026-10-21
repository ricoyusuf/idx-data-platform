import sys
from datetime import timedelta

import pendulum
from airflow.sdk import dag, task


PROJECT_DIR = "/opt/airflow/idx-data-platform"


@dag(
    dag_id="idx_stock_pipeline",
    schedule="30 17 * * 1-5",
    start_date=pendulum.datetime(
        2026, 1, 1, tz="Asia/Jakarta"
    ),
    catchup=False,
    tags=["idx-data-platform", "stocks", "etl"],
)
def idx_stock_pipeline():

    @task(
        retries=1,
        retry_delay=timedelta(minutes=5),
    )
    def setup_database_task():
        if PROJECT_DIR not in sys.path:
            sys.path.insert(0, PROJECT_DIR)

        from src.load.db_setup import setup_database

        setup_database()

    @task(
        retries=1,
        retry_delay=timedelta(minutes=5),
    )
    def ingest_stocks_task():
        if PROJECT_DIR not in sys.path:
            sys.path.insert(0, PROJECT_DIR)

        from src.pipeline import run_all_stocks, TICKERS

        results = run_all_stocks(TICKERS)

        failed_tickers = [
            ticker
            for ticker, status in results.items()
            if not status
        ]

        if failed_tickers:
            raise RuntimeError(
                "Pipeline failed for tickers: "
                + ", ".join(failed_tickers)
            )

        print(
            f"All {len(results)} tickers processed successfully."
        )

    setup_database_task() >> ingest_stocks_task()


idx_stock_pipeline()