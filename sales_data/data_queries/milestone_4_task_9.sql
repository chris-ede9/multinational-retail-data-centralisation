WITH sales_dates AS (
SELECT "year", CAST(CONCAT(make_date(CAST("year" AS INT), CAST("month" AS INT), CAST("day" AS INT)), ' ', "timestamp") AS TIMESTAMP) AS "timestamp" 
FROM public.dim_date_times
ORDER BY "year", "month", "day", "timestamp"),

sales_differences AS (
SELECT "year", "timestamp", LEAD("timestamp") OVER (PARTITION BY "year" ORDER BY "timestamp") AS next_timestamp 
FROM sales_dates),

sales_intervals AS (
SELECT "year", CAST(next_timestamp AS TIMESTAMP) - CAST("timestamp" AS TIMESTAMP) AS timestamp_diff
FROM sales_differences)

SELECT DISTINCT "year", AVG(timestamp_diff) AS actual_time_taken
FROM sales_intervals
GROUP BY "year"
ORDER BY actual_time_taken DESC