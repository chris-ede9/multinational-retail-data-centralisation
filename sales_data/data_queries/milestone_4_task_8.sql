SELECT DISTINCT CAST(SUM(pr.product_price * o.product_quantity) AS DECIMAL(18, 2)) AS total_sales, sd.store_type, sd.country_code
FROM orders_table AS o
INNER JOIN dim_store_details sd ON o.store_code = sd.store_code
INNER JOIN dim_products AS pr ON o.product_code = pr.product_code
WHERE sd.country_code = 'DE'
GROUP BY sd.store_type, sd.country_code
ORDER BY total_sales