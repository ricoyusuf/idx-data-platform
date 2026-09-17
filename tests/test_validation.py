import pandas as pd
import pytest
from src.validation.validate_stock import validate_stock

@pytest.fixture
def valid_df():
    return pd.DataFrame({
    "Date": ["2025-01-01","2026-01-01"],
    "Close": [100,101],
    "High": [105,103],
    "Low": [95,99],
    "Open": [98,100],
    "Volume": [1000,3000]
})

def test_valid_data(valid_df):
    assert validate_stock(valid_df) 

def test_missing_value(valid_df):
    test_df = valid_df.copy()
    test_df.loc[0, "Close"] = None
    assert not validate_stock(test_df) 

def test_missing_column(valid_df):
    test_df = valid_df.drop(columns=["Volume"])
    assert not validate_stock(test_df) 

def test_unsorted_date(valid_df):
    test_df = valid_df.copy()
    test_df.loc[0,"Date"] = "2027-01-01"
    assert not validate_stock(test_df)