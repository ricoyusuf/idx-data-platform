import pandas as pd
import pytest
from src.load.db_connection import get_connection
from src.load.db_loader import insert_stock_data

@pytest.fixture
def db_test_ticker():
    connection = get_connection()
    cursor = connection.cursor() 
    
    cursor.execute(
            "DELETE FROM stock_prices WHERE ticker = %s",
            ("TEST",)
        )
    connection.commit()
    cursor.close()
    connection.close()

    yield "TEST"

    connection = get_connection()
    cursor = connection.cursor() 
    
    cursor.execute(
            "DELETE FROM stock_prices WHERE ticker = %s",
            ("TEST",)
        )
    connection.commit()
    cursor.close()
    connection.close()

def test_insert_stock_data(db_test_ticker):

    test_df = pd.DataFrame({
        "Date": ["2099-01-01", "2099-01-02"],
        "Open": [100, 105],
        "High": [110, 115],
        "Low": [95, 100],
        "Close": [105,110],
        "Volume": [1000, 2000]
    })

    insert_stock_data(test_df, db_test_ticker)

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT ticker, date, open, high, low, close, volume FROM stock_prices WHERE ticker = %s ORDER BY date
    """, (db_test_ticker,)
    )

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    assert len(result) == 2
    assert result[0][0] == db_test_ticker
    assert result[0][1].isoformat() == "2099-01-01"
    assert result[0][5] == 105

def test_upsert_stock_data(db_test_ticker):
    test_df = pd.DataFrame({
        "Date": ["2099-01-01", "2099-01-02"],
        "Open": [100, 105],
        "High": [110, 115],
        "Low": [95, 100],
        "Close": [105,110],
        "Volume": [1000, 2000]
    })    

    insert_stock_data(test_df,db_test_ticker)
    updated_df = test_df.copy()
    updated_df.loc[0,"Close"] = 999
    insert_stock_data(updated_df,db_test_ticker)

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT ticker, date, open, high, low, close, volume FROM stock_prices WHERE ticker = %s ORDER BY date
    """, (db_test_ticker,)
    )

    result = cursor.fetchall()

    cursor.close()
    connection.close()

    assert len(result) == 2
    assert result[0][0] == db_test_ticker
    assert result[0][1].isoformat() == "2099-01-01"
    assert result[0][5] == 999