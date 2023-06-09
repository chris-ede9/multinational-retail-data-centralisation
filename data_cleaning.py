import pandas as pd
import numpy as np
from data_extraction import DataExtractor
from database_utils import DatabaseConnector

# This Class cleans up the data in a specified Pandas DataFrame
class DataCleaning():
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def clean_user_data(df: pd.DataFrame) -> pd.DataFrame:
        '''
        This method cleans up the data from a Pandas dataFrame containing User data with a specific schema

        df: Pandas Dataframe - The Dataframe that is going to be cleaned

        returns: Pandas Dataframe - The cleaned DataFrame
        '''

        # Remove the rows with NULL values
        df = DataCleaning._clean_null_values(df, 'first_name')

        # Remove all rows with an invalid email address
        df = df[df['email_address'].str.contains('@')]

        # Update the Country data type to Category
        df['country'] = df['country'].astype('category')

        # Replace bad country code data
        df['country_code'] = np.where(df['country_code'] == 'GGB', 'GB', df['country_code'])
        df['country_code'] = df['country_code'].astype('category')

        # Format date of birth data to be consistent
        df = DataCleaning._clean_dates(df, 'date_of_birth')

        # Format join date data to be consistent
        df = DataCleaning._clean_dates(df, 'join_date')

        # Format phone number to be consistent
        df = DataCleaning._clean_phone_numbers(df, 'phone_number')

        # Set the index for the DataFrame
        df.set_index('index', inplace=True)
        return df
    
    @staticmethod
    def _clean_null_values(df: pd.DataFrame, col_name: str) -> pd.DataFrame:
        '''
        This method removes all rows in a DataFrame that contain 'NULL' in a specified column

        df: Pandas Dataframe - The Dataframe that is going to be cleaned
        col_name: str - The column to check for NULL values

        returns: Pandas Dataframe - DataFrame with cleaned date column
        '''

        # Remove the rows with NULL values
        df.replace('NULL', pd.NA, inplace=True)
        df = df[df[col_name].notna()]

        return df
    
    @staticmethod
    def _clean_dates(df: pd.DataFrame, col_name: str) -> pd.DataFrame:
        '''
        This method cleans up a specifed date column in a Pandas DataFrame

        df: Pandas Dataframe - The Dataframe that is going to be cleaned
        col_name: str - The date column name

        returns: Pandas Dataframe - DataFrame with cleaned date column
        '''

        # Get all the different date formats in the column
        date1 = pd.to_datetime(df[col_name], errors='coerce', format="%Y-%m-%d")
        date2 = pd.to_datetime(df[col_name], errors='coerce', format="%B %Y %d")
        date3 = pd.to_datetime(df[col_name], errors='coerce', format="%Y %B %d")
        date4 = pd.to_datetime(df[col_name], errors='coerce', format="%Y/%m/%d")

        # Merge the date formats back into the format for date1
        df[col_name] = date1.fillna(date2.fillna(date3.fillna(date4))).dt.date

        return df
    
    @staticmethod
    def _clean_phone_numbers(df: pd.DataFrame, col_name: str) -> pd.DataFrame:
        '''
        This method cleans up a specifed phone number column in a Pandas DataFrame

        df: Pandas Dataframe - The Dataframe that is going to be cleaned
        col_name: str - The phone number column name

        returns: Pandas Dataframe - DataFrame with cleaned phone number column
        '''

        # Remove all non-numeric characters
        df[col_name] = df[col_name].str.replace(" ", "", regex=True).str.replace("(", "", regex=True).str.replace(")", "", regex=True).str.replace(".", "", regex=True).str.replace("-", "", regex=True).str.replace("+", "", regex=True)
        # Remove all leading zeros in the phone number
        for i in range(1, 6):
            df[col_name] = np.where(df[col_name].str.startswith('0'), df[col_name].str[1:], df[col_name])
        
        # For each country, ensure the right country code is prefixed if not there already
        df[col_name] = np.where((df['country_code'] == 'US') & (df[col_name].str.startswith('1') == False), '+1' + df[col_name], df[col_name])
        df[col_name] = np.where((df['country_code'] == 'GB') & (df[col_name].str.startswith('44') == False), '+44' + df[col_name], df[col_name])
        # Germany can have area codes starting with 49, so need to ensure they are accounted for
        df[col_name] = np.where((df['country_code'] == 'DE') & (df[col_name].str.startswith('49') == True) & (df[col_name].str.len() < 10), '49' + df[col_name], df[col_name])
        df[col_name] = np.where((df['country_code'] == 'DE') & (df[col_name].str.startswith('49') == False), '+49' + df[col_name], df[col_name])
        # For any remaining phone numbers that don't have the + prefixed, then add to start
        df[col_name] = np.where(df[col_name].str.startswith('+'), df[col_name], '+' + df[col_name])

        return df
    
    @staticmethod
    def clean_card_data(df: pd.DataFrame) -> pd.DataFrame:
        '''
        This method cleans up the data from a Pandas dataFrame containing Card details data with a specific schema

        df: Pandas Dataframe - The Dataframe that is going to be cleaned

        returns: Pandas Dataframe - The cleaned DataFrame
        '''

        # Remove the rows with NULL values
        df = DataCleaning._clean_null_values(df, 'card_number')
        # Remove the invalid question marks in the card number column
        df['card_number'] = df['card_number'].replace('[?]', '', regex=True)

        # Remove all rows with an invalid card provider
        df = df.groupby('card_provider').filter(lambda x: len(x) > 1)
        # Update the Card Provider data type to Category
        df['card_provider'] = df['card_provider'].astype('category')

        # Format date payment confirmed data to be consistent
        df = DataCleaning._clean_dates(df, 'date_payment_confirmed')

        # Set the index for the DataFrame
        df.set_index('card_number', inplace=True)
        return df
    
    @staticmethod
    def clean_store_data(df: pd.DataFrame) -> pd.DataFrame:
        '''
        This method cleans up the data from a Pandas dataFrame containing Store data with a specific schema

        df: Pandas Dataframe - The Dataframe that is going to be cleaned

        returns: Pandas Dataframe - The cleaned DataFrame
        '''

        # Remove the rows with NULL values
        df = DataCleaning._clean_null_values(df, 'store_code')

        # Remove any N/A rows to NULL for location columns so they can be converted to float in future
        df['longitude'].replace('N/A', pd.NA, inplace=True)
        df['latitude'].replace('N/A', pd.NA, inplace=True)

        # Remove all rows with an invalid country code
        df = df.groupby('country_code').filter(lambda x: len(x) > 1)
        # Update the country code data type to Category
        df['country_code'] = df['country_code'].astype('category')

        # Replace bad continent data
        df['continent'] = np.where(df['continent'] == 'eeAmerica', 'America', df['continent'])
        df['continent'] = np.where(df['continent'] == 'eeEurope', 'Europe', df['continent'])
        df['continent'] = df['continent'].astype('category')

        # Remove the lat column as not required as NULL data and latitude column is correct
        df = df.drop(columns=['lat'])

        # Remove invalid characters in staff numbers field
        df['staff_numbers'] = df['staff_numbers'].str.replace('[^0-9]', '', regex=True)

        # Format opening date data to be consistent
        df = DataCleaning._clean_dates(df, 'opening_date')

        # Set the index for the DataFrame
        df.set_index('index', inplace=True)
        return df
    
    @staticmethod
    def clean_products_data(df: pd.DataFrame) -> pd.DataFrame:
        '''
        This method cleans up the data from a Pandas dataFrame containing products data with a specific schema

        df: Pandas Dataframe - The Dataframe that is going to be cleaned

        returns: Pandas Dataframe - The cleaned DataFrame
        '''

        # Rename the unnamed index column
        df = df.rename(columns={'Unnamed: 0': 'index'})

        # Remove the rows with NULL values
        df = DataCleaning._clean_null_values(df, 'product_name')

        # Remove all rows with an invalid category
        df = df.groupby('category').filter(lambda x: len(x) > 1)
        # Update the category data type to Category
        df['category'] = df['category'].astype('category')

        # Convert the weights to kg
        df = DataCleaning.convert_product_weights(df)

        # Format opening date data to be consistent
        df = DataCleaning._clean_dates(df, 'date_added')

        # Replace bad removed data
        df['removed'] = np.where(df['removed'] == 'Still_avaliable', 'Still_available', df['removed'])
        # Update the category data type to Category
        df['removed'] = df['removed'].astype('category')

        # Set the index for the DataFrame
        df.set_index('index', inplace=True)
        return df
    
    @staticmethod
    def convert_product_weights(df: pd.DataFrame) -> pd.DataFrame:
        '''
        This method converts all the weights to kg in the weight column

        df: Pandas Dataframe - The Dataframe that is going to have the weight column converted to kg

        returns: Pandas Dataframe - DataFrame with weight column all containing kg values
        '''

        # Replace all ml values to g as 1:1 ratio
        df['weight'] = df['weight'].replace('ml', 'g', regex=True)

        # Create a new column to store the weight type
        df['weight_type'] = np.where(df['weight'].str.contains('kg') == True, 'kg', np.where(df['weight'].str.contains('oz') == True, 'oz', 'g'))

        # Handle the values which contain multiples of the weights by storing the multipler to use later
        df['weight_mult'] = np.where(df['weight'].str.contains('x') == True, df['weight'].str.split(' x ').str[0], 1)
        df['weight'] = np.where(df['weight'].str.contains('x') == True, df['weight'].str.split(' x ').str[1], df['weight'] )

        # Remove the excess characters in the weight column
        df['weight'] = df['weight'].str.replace('[^\\d.]', '', regex=True)
        
        # Update the weight data types to float
        df['weight_mult'] = df['weight_mult'].astype('int')
        df['weight'] = df['weight'].astype('float')

        # Convert all weights that are in grams or ounces to kg
        df['weight'] = np.where(df['weight_type'] == 'g', df['weight'] / 1000, df['weight'])
        df['weight'] = np.where(df['weight_type'] == 'oz', round(df['weight'] / 35.274, 3), df['weight'])

        # Multipy the weights by the multiplier field
        df['weight'] = round(df['weight'] * df['weight_mult'], 3)

        # Remove the temp columns
        df = df.drop(columns=['weight_type'])
        df = df.drop(columns=['weight_mult'])

        return df

    @staticmethod
    def clean_orders_data(df: pd.DataFrame) -> pd.DataFrame:
        '''
        This method cleans up the data from a Pandas dataFrame containing order data with a specific schema

        df: Pandas Dataframe - The Dataframe that is going to be cleaned

        returns: Pandas Dataframe - The cleaned DataFrame
        '''

        # Remove the redundant columns
        df = df.drop(columns=['index', 'level_0', 'first_name', 'last_name', '1'])

        # Update the data types for the columns
        df['card_number'] = df['card_number'].astype('string')

        # Set the index for the DataFrame
        df.set_index(['date_uuid', 'user_uuid'], inplace=True)
        return df
    
    @staticmethod
    def clean_events_data(df: pd.DataFrame) -> pd.DataFrame:
        '''
        This method cleans up the data from a Pandas dataFrame containing events data with a specific schema

        df: Pandas Dataframe - The Dataframe that is going to be cleaned

        returns: Pandas Dataframe - The cleaned DataFrame
        '''
        
        # Remove the rows with NULL values
        df = DataCleaning._clean_null_values(df, 'date_uuid')

        # Remove all rows with an invalid time period
        df = df.groupby('time_period').filter(lambda x: len(x) > 1)
        # Update the time period data type to Category
        df['time_period'] = df['time_period'].astype('category')

        # Set the index for the DataFrame
        df.set_index('date_uuid', inplace=True)
        return df
    
if __name__ == "__main__":
    # Testing Methods
    
    dc = DatabaseConnector()

    df = DataCleaning.clean_user_data(DataExtractor.read_rds_table('legacy_users'))
    dc.upload_to_db(df, 'dim_users')

    df = DataCleaning.clean_card_data(DataExtractor.retrieve_pdf_data('https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf'))
    dc.upload_to_db(df, 'dim_card_details')

    df = DataCleaning.clean_store_data(DataExtractor.retrieve_stores_data('https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/', {'x-api-key': 'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}))
    dc.upload_to_db(df, 'dim_store_details')

    df = DataCleaning.clean_products_data(DataExtractor.extract_from_s3('s3://data-handling-public/products.csv'))
    dc.upload_to_db(df, 'dim_products')

    df = DataCleaning.clean_orders_data(DataExtractor.read_rds_table('orders_table'))
    dc.upload_to_db(df, 'orders_table')
    
    df = DataCleaning.clean_events_data(DataExtractor.retrieve_event_data('https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json'))
    dc.upload_to_db(df, 'dim_date_times')