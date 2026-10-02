from src.load.db_connection import get_connection

def insert_stock_data(df, ticker):
    connection = get_connection()
    cursor = connection.cursor()

    query = """
            INSERT INTO stock_prices (ticker, date, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (ticker, date)
            DO UPDATE SET
                open = EXCLUDED.open,
                high = EXCLUDED.high,
                low = EXCLUDED.low,
                close = EXCLUDED.close,
                volume = EXCLUDED.volume
    """

    for _, row in df.iterrows():
        values = (
            ticker,
            row["Date"],
            row["Open"],
            row["High"],
            row["Low"],
            row["Close"],
            row["Volume"],

        )
        cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()

    print(f"{ticker} data inserted successfuly")

