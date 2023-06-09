# Multinational Retail Data Centralisation

 This project is based on a scenario where you work for a multinational company that sells various goods across the globe. Currently, their sales data is spread across many different data sources making it not easily accessible or analysable by current members of the team. In an effort to become more data-driven, your organisation would like to make its sales data accessible from one centralised location. Your first goal will be to produce a system that stores the current company data in a database so that it's accessed from one centralised location and acts as a single source of truth for sales data. You will then query the database to get up-to-date metrics for the business.

## Application Setup:

> Database Setup:

- Ensure a local Postgresql instance has been initialised with the attributes in the db_creds_local.yaml file in the root directory.

> Running the Python application to populate the sales_data database:

- Execute the data_cleaning.py file. This will call the necessary functions to extract the data from the various sources, clean that data up and then uploaded into the local sales_data database.

> Setting up the database star-based schema:

- Once the data has all been added to the database, SQL queries will need to be run which can be found in the sales_data\schema_setup folder. Utilise a tool like pgAdmin 4 to achieve this.

> Querying the database to gather insights on the business performance:

- Data queries that have been written so far can be found in the sales_data\data_queries folder and can be run in a tool like pgAdmin 4.

## Project Milestones for the Project:

### Milestone 1

- Setup the environment in a GitHub Repo.

### Milestone 2

> Extract and clean the data from the data sources.

>> This is written in Python code in the following files - data_cleaning, data_extraction and database_utils.

- Task 1: Setup a new database to store the data. This is stored locally in the folder sales_data. The database is a postgresql db.

- Task 2: Initialise the three project classes - Data_Extraction.py, Database_Utils.py and Data_Cleaning.py.

- Task 3: The historical data of users is currently stored in an AWS database in the cloud. Create methods in your DataExtractor, DatabaseConnector and DataCleaning classes which help extract the information from an AWS RDS database. This should then be cleaned and uploaded to a local database, sales_data.

- Task 4: The users card details are stored in a PDF document in an AWS S3 bucket. Create methods in DataExtractor and DataCleaning to retrieve the data, clean it up and upload to the sales_data database.

- Task 5: The store data can be retrived through the use of an API. Create methods in DataExtractor and DataCleaning to retrieve the data, clean it up and upload to the sales_data database.

- Task 6: The products data can be retrived from an S3 bucket in AWS. Create methods in DataExtractor and DataCleaning to retrieve the data, clean it up, convert the weights into kgs and upload to the sales_data database.

- Task 7: The orders data is currently stored in an AWS database in the cloud. Create methods in your DatabaseConnector and DataCleaning classes which help extract the information from an AWS RDS database. This data will act as the single source of truth for all orders the company has made in the past.

- Task 8: The events data is stored in a JSON file in an AWS S3 bucket. Create methods in DataExtractor and DataCleaning to retrieve the data, clean it up and upload to the sales_data database.

### Milestone 3

> Develop the star-based schema of the database, ensuring that the columns are of the correct data types.

>> All SQL code for the tasks can be found in the sales_data\schema_setup folder.

- Task 1: Cast the columns of the orders_table to the correct data types.

- Task 2: Cast the columns of the dim_users table to the correct data types.

- Task 3: Cast the columns of the dim_store_details table to the correct data types.

- Task 4: In SQL create a weight_class column in the dim_products table and populate based on the weight column.

- Task 5: Cast the columns of the dim_products table to the correct data types.

- Task 6: Cast the columns of the dim_date_times table to the correct data types.

- Task 7: Cast the columns of the dim_card_details table to the correct data types.

- Task 8: Create the primary keys in the dimensions tables (Please note this was initialised directly in the pgAdmin 4 tool).

- Task 9: Finalising the star-based schema and adding the foreign keys to the orders table.

### Milestone 4

> Querying the data. Write business led queries that benefit the business in making informed data-led decisions.

>> All data queries for the tasks can be found in the sales_data\data_queries folder.

- Task 1: How many stores does the business have and in which countries?

- Task 2: Which locations currently have the most stores?

- Task 3: Which months produce the average highest cost of sales typically?

- Task 4: How many sales are coming from online?

- Task 5: What percentage of sales come through each type of store?

- Task 6: Which month in each year produced the highest cost of sales?

- Task 7: What is our staff headcount?

- Task 8: Which German store type is selling the most?

- Task 9: How quickly is the company making sales?