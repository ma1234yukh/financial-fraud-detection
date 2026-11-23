import os
import pandas as pd
import psycopg2
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "transactions.csv"
SCHEMA = ROOT / "sql" / "schema.sql"
QUERY = ROOT / "sql" / "monitoring_queries.sql"
OUTPUT = ROOT / "data" / "risk_based_transaction_report.csv"

def connect():
    return psycopg2.connect(
        host=os.getenv("PGHOST", "localhost"),
        port=os.getenv("PGPORT", "5432"),
        dbname=os.getenv("PGDATABASE", "fraud_monitoring"),
        user=os.getenv("PGUSER", "postgres"),
        password=os.getenv("PGPASSWORD", "")
    )

def main():
    if not DATA.exists():
        raise FileNotFoundError("Run `python generate_data.py` first.")

    conn = connect()
    try:
        with conn.cursor() as cur:
            cur.execute(SCHEMA.read_text(encoding="utf-8"))
            conn.commit()

        df = pd.read_csv(DATA)
        # Keep the demo's registered/home country as IN. A production system
        # would load this from a customer master table.
        df["customer_home_country"] = "IN"

        with conn.cursor() as cur:
            insert_sql = """
                INSERT INTO transactions
                (transaction_id, customer_id, transaction_time, amount, channel,
                 country_code, status, merchant_id, customer_home_country)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            values = [
                (r.transaction_id, int(r.customer_id), r.transaction_time,
                 float(r.amount), r.channel, r.country_code, r.status,
                 r.merchant_id, r.customer_home_country)
                for r in df.itertuples(index=False)
            ]
            cur.executemany(insert_sql, values)
            conn.commit()

        # Execute the first monitoring query (before the recursive CTE marker).
        sql = QUERY.read_text(encoding="utf-8")
        report_sql = sql.split("-- Recursive CTE example:")[0]
        report = pd.read_sql_query(report_sql, conn)
        report.to_csv(OUTPUT, index=False)
        print(f"Loaded {len(df)} transactions.")
        print(f"Exported {len(report)} flagged transactions to {OUTPUT}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
