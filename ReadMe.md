# Multinational Retail Data Centralisation

> This project is based on a scenario where you work for a multinational company that sells various goods across the globe. Currently, their sales data is spread across many different data sources making it not easily accessible or analysable by current members of the team. In an effort to become more data-driven, your organisation would like to make its sales data accessible from one centralised location. Your first goal will be to produce a system that stores the current company data in a database so that it's accessed from one centralised location and acts as a single source of truth for sales data. You will then query the database to get up-to-date metrics for the business.

## Milestone 1

- Setup the environment in a GitHub Repo.

## Milestone 2

> Extract amd clean the data from the data sources.

- Task 1: Setup a new database to store the data. This is stored locally in the folder sales_data. The database is a postgres db.

- Task 2: Initialise the three project classes - Data_Extraction.py, Database_Utils.py and Data_Cleaning.py.

- Task 3: The historical data of users is currently stored in an AWS database in the cloud. Create methods in your DataExtractor, DatabaseConnector and DataCleaning classes which help extract the information from an AWS RDS database. This should then be cleaned and uploaded to a local database, sales_data.

- Task 4: The users card details are stored in a PDF document in an AWS S3 bucket. Create methods in DataExtractor and DataCleaning to retrieve the data, clean it up and upload to the sales_data database.

- Task 5: The store data can be retrived through the use of an API. Create methods in DataExtractor and DataCleaning to retrieve the data, clean it up and upload to the sales_data database.

- Task 6: The products data can be retrived by retroeving from an S3 bucket in AWS. Create methods in DataExtractor and DataCleaning to retrieve the data, clean it up, convert the weights into kg and upload to the sales_data database.

- Task 7: The orders data is currently stored in an AWS database in the cloud. Create methods in your DatabaseConnector and DataCleaning classes which help extract the information from an AWS RDS database. This data will act as the single source of truth for all orders the company has made in the past.

- Task 8: The events data is stored in a JSON file in an AWS S3 bucket. Create methods in DataExtractor and DataCleaning to retrieve the data, clean it up and upload to the sales_data database.

## Milestone 3

> Develop the star-based schema of the database, ensuring that the columns are of the correct data types.

- Task 1: Cast the columns of the orders_table to the correct data types.

- Task 2: Cast the columns of the dim_users table to the correct data types.

- Task 3: Cast the columns of the dim_store_details table to the correct data types.

- Task 4: In SQL create a weigh_class column in the dim_products table and populate based on the weight column.

- Task 5: Cast the columns of the dim_products table to the correct data types.

- Task 6: Cast the columns of the dim_date_times table to the correct data types.

- Task 7: Cast the columns of the dim_card_details table to the correct data types.

- Task 8: Create the primary keys in the dimensions tables.

- Task 9: Finalising the star-based schema and adding the foreign keys to the orders table.