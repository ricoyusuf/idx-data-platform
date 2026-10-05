from src.load.db_connection import get_connection
from psycopg2.extras import execute_values

def insert_stock_data(df, ticker):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
            INSERT INTO stock_prices (ticker, date, open, high, low, close, volume)
            VALUES %s
            ON CONFLICT (ticker, date)
            DO UPDATE SET
                open = EXCLUDED.open,
                high = EXCLUDED.high,
                low = EXCLUDED.low,
                close = EXCLUDED.close,
                volume = EXCLUDED.volume
    """

    rows = [
        (
            ticker,
            row.Date,
            row.Open,
            row.High,
            row.Low,
            row.Close,
            row.Volume,

        )
        for row in df.itertuples(index=False)
    ]

    execute_values(cursor, query, rows)

    connection.commit()

    cursor.close()
    connection.close()

    print(f"{ticker} data inserted successfuly")

