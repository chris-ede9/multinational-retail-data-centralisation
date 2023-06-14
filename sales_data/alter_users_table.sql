SELECT MAX(LENGTH(country_code)) FROM dim_users; /* 2 */

ALTER TABLE dim_users
	ALTER COLUMN first_name TYPE VARCHAR(255),
	ALTER COLUMN last_name TYPE VARCHAR(255),
	ALTER COLUMN country_code TYPE VARCHAR(2),
	ALTER COLUMN user_uuid TYPE UUID USING user_uuid::uuid;