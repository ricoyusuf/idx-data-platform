from pathlib import Path

from src.load.db_connection import get_connection

BASE_DIR = Path(__file__).resolve().parents[2]
SQL_DIR = BASE_DIR / "sql"


def run_query(sql, params=None):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        if params is None:
            cursor.execute(sql)
        else:
            cursor.execute(sql, params)

        columns = [column.name for column in cursor.description]
        rows = cursor.fetchall()

        return columns, rows


    finally:
        cursor.close()
        connection.close()

def get_stock_by_ticker(ticker):
    sql = (SQL_DIR / "stock_by_ticker.sql").read_text(
            encoding="utf-8"
        )
    columns, rows = run_query(sql, (ticker,))
    return columns, rows

def get_latest_stocks():
    sql = (SQL_DIR / "latest_stocks.sql").read_text(
        encoding="utf-8"
    )

    columns, rows = run_query(sql)

    return columns, rows

if __name__ == "__main__":
    columns, rows = get_latest_stocks()

    print(columns)

    for row in rows:
        print(row)