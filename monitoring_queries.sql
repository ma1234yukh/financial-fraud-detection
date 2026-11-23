-- Risk-based report: rolling transaction counts + rule-based risk points.
WITH rolling AS (
    SELECT
        t.*,
        COUNT(*) OVER (
            PARTITION BY customer_id
            ORDER BY transaction_time
            RANGE BETWEEN INTERVAL '10 minutes' PRECEDING AND CURRENT ROW
        ) AS tx_count_10m,
        COUNT(*) OVER (
            PARTITION BY customer_id
            ORDER BY transaction_time
            RANGE BETWEEN INTERVAL '24 hours' PRECEDING AND CURRENT ROW
        ) AS tx_count_24h,
        SUM(amount) OVER (
            PARTITION BY customer_id
            ORDER BY transaction_time
            RANGE BETWEEN INTERVAL '24 hours' PRECEDING AND CURRENT ROW
        ) AS amount_sum_24h
    FROM transactions t
),
scored AS (
    SELECT *,
        (CASE WHEN amount >= 100000 THEN 40 ELSE 0 END) +
        (CASE WHEN tx_count_10m >= 3 THEN 25 ELSE 0 END) +
        (CASE WHEN tx_count_24h >= 5 THEN 20 ELSE 0 END) +
        (CASE WHEN country_code <> customer_home_country THEN 15 ELSE 0 END)
        AS risk_score
    FROM rolling
)
SELECT
    transaction_id, customer_id, transaction_time, amount, channel,
    country_code, status, tx_count_10m, tx_count_24h,
    ROUND(amount_sum_24h, 2) AS amount_sum_24h,
    risk_score,
    CASE
        WHEN risk_score >= 60 THEN 'HIGH'
        WHEN risk_score >= 30 THEN 'MEDIUM'
        ELSE 'LOW'
    END AS risk_level
FROM scored
WHERE risk_score >= 30
ORDER BY risk_score DESC, transaction_time DESC;

-- Recursive CTE example: follow transactions between linked accounts.
-- In this demo, merchant IDs are used as a simple connection key.
-- Replace this relationship with a proper account-to-account transfer table
-- in a real implementation.
WITH RECURSIVE merchant_links AS (
    SELECT
        customer_id AS root_customer,
        customer_id AS current_customer,
        merchant_id,
        1 AS depth,
        ARRAY[customer_id] AS path
    FROM transactions
    WHERE status = 'SUCCESS'

    UNION ALL

    SELECT
        ml.root_customer,
        t.customer_id,
        t.merchant_id,
        ml.depth + 1,
        ml.path || t.customer_id
    FROM merchant_links ml
    JOIN transactions t
      ON t.merchant_id = ml.merchant_id
     AND t.customer_id <> ml.current_customer
    WHERE ml.depth < 3
      AND NOT t.customer_id = ANY(ml.path)
)
SELECT DISTINCT root_customer, current_customer, merchant_id, depth
FROM merchant_links
WHERE depth > 1
ORDER BY root_customer, depth;
