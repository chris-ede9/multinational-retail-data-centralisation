from data_extraction import DataExtractor as de
from database_utils import DatabaseConnector as dc
import pandas as pd
import numpy as np

# This Class cleans up the data in a specified Pandas DataFrame
class DataCleaning():
    def __init__(self) -> None:
        pass
    
    '''
    This method cleans up the data from a Pandas dataFrame

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

        # print(df.loc[df['index'] == 14514])
        print(df.info())

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
        df[col_name] = df[col_name].str.replace(" ", "").str.replace("(", "").str.replace(")", "").str.replace(".", "").str.replace("-", "").str.replace("+", "")
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

if __name__ == "__main__":
    # Testing Methods
    df = DataCleaning.clean_user_data(de.read_rds_table('legacy_users'))
    dc.upload_to_db(df, 'dim_users')