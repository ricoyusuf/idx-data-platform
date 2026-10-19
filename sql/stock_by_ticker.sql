SELECT
    ticker,
    date,
    close,
    previous_close,
    daily_return,
    ma_20,
    distance_ma20,
    trend,
    ma20_category
FROM stock_analysis
WHERE ticker = %s
ORDER BY date DESC;