-- =========================================
-- STAGING TABLE
-- =========================================

CREATE TABLE IF NOT EXISTS stg_bhavcopy (
    symbol TEXT,
    open_price NUMERIC,
    high_price NUMERIC,
    low_price NUMERIC,
    close_price NUMERIC,
    volume BIGINT,
    trade_date DATE,
    source_file TEXT
);



-- =========================================
-- FACT TABLE
-- =========================================

CREATE TABLE IF NOT EXISTS fact_stock_prices (
    symbol TEXT,
    trade_date DATE,
    open_price NUMERIC,
    high_price NUMERIC,
    low_price NUMERIC,
    close_price NUMERIC,
    volume BIGINT,
    avg_close_last_3_days NUMERIC,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



-- =========================================
-- AUDIT TABLE
-- =========================================

CREATE TABLE IF NOT EXISTS etl_audit_log (
    id SERIAL PRIMARY KEY,
    job_name TEXT,
    source_file TEXT,
    records_loaded INTEGER,
    status TEXT,
    error_message TEXT,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
