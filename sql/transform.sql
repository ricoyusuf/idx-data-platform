CREATE OR REPLACE VIEW stock_analysis AS

WITH calculated_data AS (
    SELECT
        ticker,
        date,
        open,
        high,
        low,
        close,
        volume,

        LAG(close) OVER (
            PARTITION BY ticker
            ORDER BY date
        ) AS previous_close,

        close - LAG(close) OVER (
            PARTITION BY ticker
            ORDER BY date
        ) AS daily_gain,

        ROUND(
            (
                close - LAG(close) OVER (
                    PARTITION BY ticker
                    ORDER BY date
                )
            )
            / LAG(close) OVER (
                PARTITION BY ticker
                ORDER BY date
            ) * 100,
            4
        ) AS daily_return,

        CASE
            WHEN COUNT(close) OVER (
                PARTITION BY ticker
                ORDER BY date
                ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
            ) = 5
            THEN AVG(close) OVER (
                PARTITION BY ticker
                ORDER BY date
                ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
            )
        END AS ma_5,

        CASE
            WHEN COUNT(close) OVER (
                PARTITION BY ticker
                ORDER BY date
                ROWS BETWEEN 19 PRECEDING AND CURRENT ROW
            ) = 20
            THEN AVG(close) OVER (
                PARTITION BY ticker
                ORDER BY date
                ROWS BETWEEN 19 PRECEDING AND CURRENT ROW
            )
        END AS ma_20

    FROM stock_prices
),

calculated_metrics AS (
    SELECT
        *,
        (close - ma_20) / ma_20 * 100 AS distance_ma20
    FROM calculated_data
)

SELECT
    ticker,
    date,
    open,
    high,
    low,
    close,
    volume,
    previous_close,
    daily_gain,
    daily_return,
    ma_5,
    ma_20,

    CASE
        WHEN ma_20 IS NULL THEN 'No Signal'
        WHEN close > ma_20 THEN 'Above MA20'
        ELSE 'Below MA20'
    END AS trend,

    distance_ma20,

    CASE
        WHEN distance_ma20 IS NULL THEN 'No Signal'
        WHEN distance_ma20 < -2 THEN 'Far Below MA20'
        WHEN distance_ma20 <= 2 THEN 'Near MA20'
        ELSE 'Far Above MA20'
    END AS ma20_category

FROM calculated_metrics;