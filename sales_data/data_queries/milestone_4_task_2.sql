SELECT DISTINCT locality, COUNT(store_code) AS total_no_stores FROM dim_store_details
WHERE Store_Type <> 'Web Portal'
GROUP BY locality
ORDER BY COUNT(store_code) DESC