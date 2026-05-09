# BSE BhavCopy ETL Pipeline

## Project Overview

The BSE BhavCopy ETL Pipeline is a Data Engineering project built to automate the ingestion, transformation, and analytical processing of stock market data from the Bombay Stock Exchange (BSE).

This project simulates a real-world ETL workflow used in financial analytics systems where daily stock market files are processed into structured analytical datasets.

The pipeline was developed using:

- Apache Airflow for orchestration
- PostgreSQL for data warehousing
- Python and Pandas for data processing
- Docker for containerization
- SQL for transformations and analytics
- WSL Ubuntu environment for development

The project processes BhavCopy CSV files, loads them into a staging table, performs SQL-based transformations, and generates analytical datasets using window functions and SQL views.

---

# Business Problem

Financial market datasets are generated daily and contain thousands of stock records.

Manually processing this data becomes difficult because:

- Files are generated daily
- Data needs cleaning and standardization
- Analysts require transformed analytical datasets
- Historical comparisons and rolling metrics are needed
- Monitoring ETL execution manually is inefficient

This project solves these problems by creating an automated ETL pipeline that:

- Loads daily stock market data
- Cleans and standardizes records
- Performs analytical SQL transformations
- Stores transformed datasets in PostgreSQL
- Maintains ETL audit logs
- Automates execution through Airflow

---

# Objectives of the Project

The primary objectives of this project were:

- Build an end-to-end ETL pipeline
- Learn Airflow DAG orchestration
- Use Docker for containerized deployment
- Implement SQL window functions
- Design staging and fact tables
- Create analytical SQL views
- Build a portfolio-ready Data Engineering project

---

# Initial Project Planning

Initially, the project was planned to:

1. Automatically fetch BhavCopy ZIP files from the BSE website
2. Extract the CSV files
3. Process one year of historical stock market data
4. Load the processed data into PostgreSQL
5. Automate the complete workflow using Airflow

However, during implementation, multiple challenges were faced with dynamic BSE download links and ZIP extraction.

To ensure stable and reliable execution:

- CSV files were manually downloaded
- The ETL pipeline was redesigned to process local CSV files from the `/data` folder
- The automation architecture remained intact

This redesign improved stability and simplified debugging.

---

# Project Architecture

```text
BhavCopy CSV Files
        ↓
Python ETL Loader
        ↓
PostgreSQL Staging Table
        ↓
SQL Transformations
        ↓
Fact Table
        ↓
Analytics Views
        ↓
Audit Logging
        ↓
Airflow DAG Orchestration
```

---

# Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data ingestion and processing |
| Pandas | CSV transformation and cleaning |
| PostgreSQL | Data warehouse |
| Apache Airflow | Workflow orchestration |
| Docker | Containerization |
| SQL | Data transformation and analytics |
| WSL Ubuntu | Development environment |
| GitHub | Version control and project hosting |

---

# Folder Structure

```text
BSE_ETL_PROJECT/
│
├── dags/
│   └── bse_etl_dag.py
│
├── scripts/
│   └── load_bhavcopy.py
│
├── sql/
│   ├── create_tables.sql
│   ├── transformations.sql
│   └── analytics_views.sql
│
├── data/
│   └── Sample BhavCopy CSV Files
│
├── results/
│   └── SQL analytics screenshots
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── README.md
└── .gitignore
```

---

# ETL Pipeline Workflow

## Step 1 — Data Ingestion

BhavCopy CSV files are placed inside the `/data` folder.

The Python ETL script:

- Reads each CSV file
- Extracts required columns
- Cleans and standardizes data
- Converts dates and numeric values
- Loads records into PostgreSQL staging tables

### Selected Columns

The following fields were extracted:

- symbol
- open_price
- high_price
- low_price
- close_price
- volume
- trade_date
- source_file

---

## Step 2 — Staging Layer

Raw cleaned records are loaded into:

```sql
stg_bhavcopy
```

The staging layer acts as an intermediate landing zone before transformation.

### Benefits

- Easier debugging
- Better data validation
- Prevents direct corruption of analytical tables

---

## Step 3 — SQL Transformation Layer

Data is transformed into the final analytical fact table:

```sql
fact_stock_prices
```

Transformations include:

- Rolling averages
- Daily volatility calculations
- Price movement analysis
- Trend signal generation
- Ranking-based analytics

---

# SQL Transformations

## Rolling 3-Day Moving Average

A rolling average was calculated using SQL window functions.

### SQL Query

```sql
AVG(close_price) OVER (
    PARTITION BY symbol
    ORDER BY trade_date
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
)
```

### Purpose

This transformation helps analyze short-term stock price trends.

### Example Output

| symbol | trade_date | close_price | avg_close_last_3_days |
|---|---|---|---|
| ABB | 2026-04-02 | 6058.65 | 6058.65 |
| ABB | 2026-04-06 | 6120.50 | 6089.57 |
| ABB | 2026-04-07 | 6200.10 | 6126.42 |

---

# SQL Analytical Views

Several analytical views were created for market analysis.

---

## SQL Analytics Sample Outputs

The project generated multiple analytical outputs using SQL transformations and window functions.

### 1. Rolling 3-Day Moving Average

This output demonstrates the rolling average calculation using SQL window functions.

Screenshot:

```text
result/rolling_average.png
```

---

### 2. Daily Price Change Analysis

This analytical output calculates daily percentage movement between opening and closing prices.

Screenshot:

```text
result/price_change_analysis.png
```

---

### 3. Volatility Analysis

This output measures daily stock volatility using high and low price differences.

Screenshot:

```text
result/volatility.png
```

---

### 4. Trend Signal & Top Gainers Analysis

This output identifies bullish/bearish signals and ranks top-performing stocks using SQL ranking functions.

Screenshot:

```text
results/top_gainers.png
```

---

## SQL Features Implemented

The project implemented several advanced SQL concepts:

- Window Functions
- Rolling Aggregations
- Analytical Views
- CASE Statements
- Ranking Functions
- Aggregate Functions
- Partitioning
- Moving Average Calculations

---

# Airflow DAG Orchestration

Apache Airflow was used to orchestrate the ETL pipeline.

The DAG performs the following tasks sequentially:

1. Load CSV files into staging table
2. Perform SQL transformations
3. Generate analytics tables/views
4. Insert ETL audit logs

---

# Airflow DAG Structure

```text
load_data
    ↓
transform_data
    ↓
audit_logging
```

---

# ETL Audit Logging

An audit table was created:

```sql
etl_audit_log
```

This table tracks:

- job_name
- source_file
- records_loaded
- status
- start_time
- end_time
- error_message

### Example Output

| job_name | records_loaded | status |
|---|---|---|
| bhavcopy_etl_load | 83585 | SUCCESS |

---

# Challenges Faced During Development

## 1. BSE Dynamic Download Links

Initially, the project attempted automatic BhavCopy downloads from the BSE website.

### Challenges Faced

- Dynamic file URLs
- Invalid ZIP responses
- Broken download links
- ZIP extraction failures

### Solution

The pipeline was redesigned to process manually downloaded CSV files from the local data folder.

---

## 2. Airflow XCom Serialization Error

### Error

```text
Object of type CompletedProcess is not JSON serializable
```

### Cause

PythonOperator was returning a non-serializable subprocess object.

### Solution

Modified the DAG so tasks returned serializable values only.

---

## 3. PostgreSQL Authentication Failure

### Error

```text
password authentication failed for user "postgres"
```

### Cause

Incorrect Airflow PostgreSQL connection configuration.

### Solution

Updated Airflow connection credentials and restarted containers.

---

## 4. Docker Container Debugging

### Challenges Included

- Container startup failures
- Airflow service synchronization
- Volume mounting issues
- DAG refresh delays

### Solution

Used Docker Compose lifecycle commands:

```bash
docker compose up -d
```

```bash
docker compose down
```

and rebuilt containers during debugging.

---

# Key SQL Concepts Used

This project implemented advanced SQL concepts including:

- Window Functions
- Aggregate Functions
- Analytical Views
- CASE Statements
- Ranking Functions
- Partitioning
- Rolling Aggregations

---

# Key Learning Outcomes

Through this project, the following skills were developed:

- ETL pipeline design
- Apache Airflow orchestration
- Docker containerization
- PostgreSQL database management
- SQL analytical transformations
- Debugging distributed systems
- Data pipeline monitoring
- Workflow automation

---

# Sample Commands Used

## Start Containers

```bash
docker compose up -d
```

## Stop Containers

```bash
docker compose down
```

## Open PostgreSQL

```bash
docker exec -it bse_etl_project-postgres-1 psql -U airflow -d airflow
```

## Trigger Airflow DAG

Open:

```text
http://localhost:8080
```

---

# Future Enhancements

The project can be extended further with:

## 1. Power BI Dashboard Integration

Connect PostgreSQL to Power BI for:

- stock trend dashboards
- gainers/losers visualization
- volatility charts
- trading volume analysis

---

## 2. Real-Time API Integration

Replace CSV ingestion with:

- real-time stock APIs
- scheduled API ingestion
- streaming pipelines

---

## 3. Incremental Data Loading

Load only new daily records instead of full reloads.

---


# Conclusion

This project successfully demonstrates an end-to-end Data Engineering workflow using modern industry tools.

The pipeline automates stock market data ingestion, performs analytical transformations, orchestrates execution using Airflow, and stores processed datasets inside PostgreSQL.

The project showcases practical implementation of:

- ETL engineering
- workflow orchestration
- SQL analytics
- Dockerized deployment
- data warehouse concepts

This project helped strengthen practical skills in Data Engineering and workflow automation while simulating a real-world financial data processing pipeline.
