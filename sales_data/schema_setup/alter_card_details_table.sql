SELECT MAX(LENGTH(card_number)) FROM dim_card_details; /* 19 */
SELECT MAX(LENGTH(expiry_date)) FROM dim_card_details; /* 5 */

ALTER TABLE dim_card_details
	ALTER COLUMN card_number TYPE VARCHAR(19),
	ALTER COLUMN expiry_date TYPE VARCHAR(5);