DROP TABLE IF EXISTS transactions;

CREATE TABLE transactions (
    transaction_id VARCHAR(20) PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    transaction_time TIMESTAMPTZ NOT NULL,
    amount NUMERIC(14,2) NOT NULL CHECK (amount >= 0),
    channel VARCHAR(30) NOT NULL,
    country_code CHAR(2) NOT NULL,
    status VARCHAR(20) NOT NULL,
    merchant_id VARCHAR(10) NOT NULL,
    customer_home_country CHAR(2) NOT NULL DEFAULT 'IN'
);

CREATE INDEX idx_transactions_customer_time
    ON transactions(customer_id, transaction_time);

CREATE INDEX idx_transactions_time
    ON transactions(transaction_time);

CREATE INDEX idx_transactions_amount
    ON transactions(amount DESC);
