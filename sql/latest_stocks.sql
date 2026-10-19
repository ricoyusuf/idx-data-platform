WITH ranked_data AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY ticker
            ORDER BY date DESC
        ) AS row_num
    FROM stock_analysis
)

SELECT
    ticker,
    date,
    close,
    ma_20,
    distance_ma20,
    daily_return,
    trend,
    ma20_category
FROM ranked_data
WHERE row_num = 1
ORDER BY ticker;