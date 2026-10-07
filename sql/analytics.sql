-- 1. Latest data for each ticker
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

-- 2. Latest return ranking
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
    daily_return,
    trend
FROM ranked_data
WHERE row_num = 1
ORDER BY daily_return DESC NULLS LAST;

-- 3. Latest distance from MA20
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
    trend
FROM ranked_data
WHERE row_num = 1
ORDER BY ABS(distance_ma20) ASC NULLS LAST;

-- 4. Latest trend distribution
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
    trend,
    COUNT(*) AS total_stocks
FROM ranked_data
WHERE row_num = 1
GROUP BY trend
ORDER BY total_stocks DESC;

-- 5. Near MA20 bullish screen
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
    trend
FROM ranked_data
WHERE row_num = 1
  AND close > ma_20
  AND daily_return > 0
  AND ABS(distance_ma20) <= 2
ORDER BY ABS(distance_ma20);