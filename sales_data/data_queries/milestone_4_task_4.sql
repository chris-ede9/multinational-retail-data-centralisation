SELECT DISTINCT COUNT(o.date_uuid) AS number_of_sales, SUM(o.product_quantity) AS product_quantity_count, (
CASE
	WHEN sd.store_type = 'Web Portal' THEN 'Web'
	ELSE 'Offline'
END) AS "location"
FROM orders_table AS o
INNER JOIN dim_store_details sd ON o.store_code = sd.store_code
GROUP BY "location"