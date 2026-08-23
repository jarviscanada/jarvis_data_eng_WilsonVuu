SELECT
  CASE WHEN is_post_fraud THEN '2 - After First Fraud'
       ELSE '1 - Before First Fraud' END                  AS period,

  -- volume / frequency behavior
  COUNT(*)                                                 AS num_transactions,
  COUNT(DISTINCT user_id)                                  AS active_users,
  ROUND(COUNT(*) * 1.0 / COUNT(DISTINCT user_id), 2)       AS avg_txns_per_user,

  -- spend behavior
  ROUND(AVG(amount), 2)                                    AS avg_amount,
  ROUND(percentile(amount, 0.5), 2)                        AS median_amount,
  ROUND(SUM(amount), 2)                                    AS total_amount,

  -- variety behavior
  COUNT(DISTINCT mcc_description)                          AS distinct_categories

FROM jrvs_databricks_fundamentals.gold.fact_transactions
WHERE first_fraud_date IS NOT NULL   -- users who were ever defrauded
  AND is_fraud = false               -- their legitimate behavior only
GROUP BY is_post_fraud
ORDER BY period;