-- =========================================
-- PRICE CHANGE ANALYSIS
-- =========================================

CREATE OR REPLACE VIEW vw_price_change_analysis AS

SELECT
    symbol,
    trade_date,
    open_price,
    close_price,

    ROUND(
        ((close_price - open_price) / open_price * 100)::numeric,
        2
    ) AS price_change_pct,

    volume

FROM fact_stock_prices;



-- =========================================
-- VOLATILITY ANALYSIS
-- =========================================

CREATE OR REPLACE VIEW vw_volatility_analysis AS

SELECT
    symbol,
    trade_date,
    high_price,
    low_price,

    ROUND(
        (high_price - low_price)::numeric,
        2
    ) AS daily_volatility,

    volume

FROM fact_stock_prices;



-- =========================================
-- TREND SIGNAL
-- =========================================

CREATE OR REPLACE VIEW vw_trend_signal AS

SELECT
    symbol,
    trade_date,
    close_price,
    avg_close_last_3_days,

    CASE
        WHEN close_price > avg_close_last_3_days
        THEN 'Bullish'

        ELSE 'Bearish'
    END AS trend_signal

FROM fact_stock_prices;



-- =========================================
-- TOP DAILY GAINERS
-- =========================================

CREATE OR REPLACE VIEW vw_top_daily_gainers AS

SELECT
    symbol,
    trade_date,

    ROUND(
        ((close_price - open_price) / open_price * 100)::numeric,
        2
    ) AS gain_pct,

    RANK() OVER (
        PARTITION BY trade_date
        ORDER BY
            ((close_price - open_price) / open_price) DESC
    ) AS daily_rank

FROM fact_stock_prices;
