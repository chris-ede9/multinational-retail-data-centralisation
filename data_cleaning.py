from data_extraction import DataExtractor as de
from database_utils import DatabaseConnector as dc
import pandas as pd
import numpy as np

# This Class cleans up the data in a specified Pandas DataFrame
class DataCleaning():
    def __init__(self) -> None:
        pass
    
    '''
    This method cleans up the data from a Pandas dataFrame containing User data with a specific schema

    df: Pandas Dataframe - The Dataframe that is going to be cleaned

    returns: Pandas Dataframe - The cleaned DataFrame
    '''
    @staticmethod
    def clean_user_data(df: pd.DataFrame) -> pd.DataFrame:
        # Remove the rows with NULL values
        df.replace('NULL', pd.NA, inplace=True)
        df = df[df['first_name'].notna()]

        # Remove all rows with an invalid email address
        df = df[df['email_address'].str.contains('@')]

        # Update the Country data type to Category
        df['country'] = df['country'].astype('category')

        # Replace bad country code data
        df['country_code'] = np.where(df['country_code'] == 'GGB', 'GB', df['country_code'])
        df['country_code'] = df['country_code'].astype('category')

        # Format date of birth data to be consistent
        df = DataCleaning.clean_dates(df, 'date_of_birth')

        # Format join date data to be consistent
        df = DataCleaning.clean_dates(df, 'join_date')

        # Format phone number to be consistent
        df = DataCleaning.clean_phone_numbers(df, 'phone_number')

        # Set the index for the DataFrame
        df.set_index('index', inplace=True)
        return df
    
    '''
    This method cleans up a specifed date column in a Pandas DataFrame

    df: Pandas Dataframe - The Dataframe that is going to be cleaned
    col_name: str - The date column name

    returns: Pandas Dataframe - DataFrame with cleaned date column
    '''
    @staticmethod
    def clean_dates(df: pd.DataFrame, col_name: str) -> pd.DataFrame:
        # Get all the different date formats in the column
        date1 = pd.to_datetime(df[col_name], errors='coerce', format="%Y-%m-%d")
        date2 = pd.to_datetime(df[col_name], errors='coerce', format="%B %Y %d")
        date3 = pd.to_datetime(df[col_name], errors='coerce', format="%Y %B %d")
        date4 = pd.to_datetime(df[col_name], errors='coerce', format="%Y/%m/%d")

        # Merge the date formats back into the format for date1
        df[col_name] = date1.fillna(date2.fillna(date3.fillna(date4))).dt.date

        return df
    
    '''
    This method cleans up a specifed phone number column in a Pandas DataFrame

    df: Pandas Dataframe - The Dataframe that is going to be cleaned
    col_name: str - The phone number column name

    returns: Pandas Dataframe - DataFrame with cleaned phone number column
    '''
    @staticmethod
    def clean_phone_numbers(df: pd.DataFrame, col_name: str) -> pd.DataFrame:
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
    
    '''
    This method cleans up the data from a Pandas dataFrame containing Card details data with a specific schema

    df: Pandas Dataframe - The Dataframe that is going to be cleaned

    returns: Pandas Dataframe - The cleaned DataFrame
    '''
    @staticmethod
    def clean_card_data(df: pd.DataFrame) -> pd.DataFrame:
        # Remove the rows with NULL values
        df.replace('NULL', pd.NA, inplace=True)
        df = df[df['card_number'].notna()]
        # Remove the invalid question marks in the card number column
        df['card_number'] = df['card_number'].replace('[?]', '', regex=True)
        # Update the Card Number to be a str data type
        df['card_number'] = df['card_number'].astype('str')

        # Remove all rows with an invalid card provider
        df = df.groupby('card_provider').filter(lambda x: len(x) > 1)
        # Update the Card Provider data type to Category
        df['card_provider'] = df['card_provider'].astype('category')
        
        # Add a column to calculate the length of the card number to check if they are valid
        df['card_number_length'] = df['card_number'].str.len()
        # remove all invalid card numbers where card numbers don't match the majority of cases per card provider
        df = df.groupby(['card_provider', 'card_number_length']).filter(lambda x: len(x) > 3)
        # Remove the length column
        df = df.drop(columns=['card_number_length'])

        # Format date payment confirmed data to be consistent
        df = DataCleaning.clean_dates(df, 'date_payment_confirmed')

        # Set the index for the DataFrame
        df.set_index('card_number', inplace=True)
        return df

if __name__ == "__main__":
    # Testing Methods
    df = DataCleaning.clean_user_data(de.read_rds_table('legacy_users'))
    dc.upload_to_db(df, 'dim_users')

    df = DataCleaning.clean_card_data(de.retrieve_pdf_data('https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf'))
    dc.upload_to_db(df, 'dim_card_details')