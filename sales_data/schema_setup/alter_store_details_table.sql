SELECT MAX(LENGTH(store_code)) FROM dim_store_details; /* 12 */
SELECT MAX(LENGTH(country_code)) FROM dim_store_details; /* 2 */

ALTER TABLE dim_store_details
	ALTER COLUMN longitude TYPE FLOAT USING longitude::float,
	ALTER COLUMN locality TYPE VARCHAR(255),
	ALTER COLUMN store_code TYPE VARCHAR(12),
	ALTER COLUMN staff_numbers TYPE SMALLINT USING staff_numbers::smallint,
	ALTER COLUMN store_type TYPE VARCHAR(255),
	ALTER COLUMN store_type SET NOT NULL,
	ALTER COLUMN latitude TYPE FLOAT USING longitude::float,
	ALTER COLUMN country_code TYPE VARCHAR(2),
	ALTER COLUMN continent TYPE VARCHAR(255);

