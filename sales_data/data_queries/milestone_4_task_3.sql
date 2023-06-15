SELECT DISTINCT CAST(SUM(pr.product_price * o.product_quantity) AS DECIMAL(18, 2)) AS total_sales, dt.month FROM orders_table AS o
INNER JOIN dim_date_times AS dt ON o.date_uuid = dt.date_uuid
INNER JOIN dim_products AS pr ON o.product_code = pr.product_code
GROUP BY dt.month
ORDER BY total_sales DESC
