INSERT INTO fact_stock_prices (
    symbol,
    trade_date,
    open_price,
    high_price,
    low_price,
    close_price,
    volume,
    avg_close_last_3_days
)

SELECT
    symbol,
    trade_date,
    open_price,
    high_price,
    low_price,
    close_price,
    volume,

    AVG(close_price) OVER (
        PARTITION BY symbol
        ORDER BY trade_date
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS avg_close_last_3_days

FROM stg_bhavcopy;
