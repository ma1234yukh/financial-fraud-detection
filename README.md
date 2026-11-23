# Financial Fraud Detection & Transaction Monitoring

A portfolio-ready SQL + PostgreSQL + Python project that generates synthetic banking transactions, loads them into PostgreSQL, detects suspicious patterns, and exports a risk-based review report.

## Features
- Synthetic transaction dataset generation (no real customer data)
- PostgreSQL schema with useful indexes
- Rolling transaction monitoring using window functions
- Risk scoring for high-value, rapid, and unusual transactions
- Recursive CTE example to trace connected transaction chains
- Python ETL and report export to CSV

## Project structure
```text
financial_fraud_detection_project/
├── data/
├── sql/
│   ├── schema.sql
│   └── monitoring_queries.sql
├── generate_data.py
├── run_pipeline.py
├── requirements.txt
└── README.md
```

## 1. Requirements
- Python 3.9+
- PostgreSQL 13+
- A PostgreSQL database, for example `fraud_monitoring`

Install Python packages:
```bash
pip install -r requirements.txt
```

## 2. Create the database
Create a database named `fraud_monitoring` in PostgreSQL, then set environment variables.

macOS/Linux:
```bash
export PGHOST=localhost
export PGPORT=5432
export PGDATABASE=fraud_monitoring
export PGUSER=postgres
export PGPASSWORD=your_password
```

Windows PowerShell:
```powershell
$env:PGHOST="localhost"
$env:PGPORT="5432"
$env:PGDATABASE="fraud_monitoring"
$env:PGUSER="postgres"
$env:PGPASSWORD="your_password"
```

## 3. Generate sample data
```bash
python generate_data.py
```
This creates `data/transactions.csv` containing synthetic customers and transactions.

## 4. Create tables and run monitoring
```bash
python run_pipeline.py
```
The pipeline creates the table, loads the CSV, runs monitoring SQL, and saves:
- `data/risk_based_transaction_report.csv`

## Detection logic (demonstration rules)
A transaction receives risk points for:
- Amount at or above 100,000
- At least 3 transactions by the same customer within a rolling 10-minute window
- At least 5 transactions by the same customer within a rolling 24-hour window
- Transaction from a country different from the customer's registered country

The score is a rule-based indicator, not proof of fraud. Tune thresholds against labelled data before real-world use.

## Resume description
**Financial Fraud Detection & Transaction Monitoring | SQL, PostgreSQL, Python**
- Built a transaction-monitoring pipeline to analyse synthetic banking transactions and flag potentially suspicious activity.
- Used PostgreSQL window functions to detect rapid transaction bursts and rolling 24-hour activity.
- Implemented risk scoring and a recursive CTE example to explore connected transaction chains.
- Automated data generation, database loading, and CSV risk-report creation using Python.

## Important
This is an educational portfolio project using synthetic data. It is not a production fraud system and does not make accusations about real customers.
