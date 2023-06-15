WITH store_total_sales AS
(SELECT DISTINCT sd.store_type, CAST(SUM(pr.product_price * o.product_quantity) AS DECIMAL(18, 2)) AS total_sales
FROM orders_table AS o
INNER JOIN dim_store_details sd ON o.store_code = sd.store_code
INNER JOIN dim_products AS pr ON o.product_code = pr.product_code
GROUP BY sd.store_type
ORDER BY total_sales DESC)

SELECT store_type, total_sales, CAST((total_sales * 100/ (SELECT SUM(total_sales) FROM store_total_sales)) AS DECIMAL(18, 2)) AS "percentage_total(%)"
FROM store_total_sales