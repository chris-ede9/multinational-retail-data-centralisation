UPDATE dim_products SET product_price = REPLACE(product_price, '£', '');

ALTER TABLE dim_products
	ADD COLUMN weight_class VARCHAR(14);
	
UPDATE dim_products
SET weight_class = CASE
	WHEN weight < 2 THEN 'Light'
	WHEN weight >= 2 AND weight < 40 THEN 'Mid_Sized'
	WHEN weight >= 40 AND weight < 140 THEN 'Heavy'
	WHEN weight >= 140 THEN 'Truck_Required'
END;

ALTER TABLE dim_products
	RENAME COLUMN removed TO still_available;
	
UPDATE dim_products
SET still_available = CASE
	WHEN still_available = 'Still_available' THEN 1
	WHEN still_available = 'Removed' THEN 0
END;

SELECT MAX(LENGTH("EAN")) FROM dim_products; /* 17 */
SELECT MAX(LENGTH(product_code)) FROM dim_products; /* 11 */

ALTER TABLE dim_products
	ALTER COLUMN product_price TYPE FLOAT USING product_price::float,
	ALTER COLUMN weight TYPE FLOAT USING weight::float,
	ALTER COLUMN "EAN" TYPE VARCHAR(17),
	ALTER COLUMN product_code TYPE VARCHAR(11),
	ALTER COLUMN "uuid" TYPE UUID USING "uuid"::uuid,
	ALTER COLUMN still_available TYPE BOOL USING still_available::BOOL;
