-- Show table schema 
\d+ retail;

-- Show first 10 rows
SELECT * FROM retail limit 10;

-- Check # of records
SELECT count(*) FROM retail;

-- number of clients (e.g. unique client ID)
SELECT count(distinct customer_id) FROM retail;

-- invoice date range (e.g. max/min dates)
SELECT min(invoice_date), max(invoice_date) FROM retail;

-- number of SKU/merchants (e.g. unique stock code)
SELECT count(distinct stock_code) FROM retail;

-- Calculate average invoice amount excluding invoices with a negative amount (e.g. canceled orders have negative amount)
SELECT AVG(invoice_amount) 
FROM (
    SELECT 
        invoice_no,
        SUM(quantity * unit_price) AS invoice_amount
    FROM retail
    GROUP BY invoice_no
    HAVING SUM(quantity * unit_price) > 0
) AS valid_invoices;

-- Calculate total revenue (e.g. sum of unit_price * quantity)
SELECT SUM(quantity * unit_price) AS total_revenue
FROM retail

-- Calculate total revenue by YYYYMM 
SELECT 
    TO_CHAR(invoice_date, 'YYYYMM') AS year_month,
    SUM(quantity * unit_price) AS total_revenue
FROM retail
GROUP BY year_month
ORDER BY year_month;
