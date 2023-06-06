from database_utils import DatabaseConnector as dc
import pandas as pd
from tabula.io import read_pdf
from sqlalchemy import text
import requests

# This Class extracts data from a data source and converts to a Pandas DataFrame
class DataExtractor():
    '''
    The initialiser method
    '''
    def __init__(self) -> None:
        pass

    '''
    The method connects to a specified data source and extracts the data from a given table into a Pandas DataFrame

    table_name: string - Name of the table
    
    returns: Pandas DataFrame - A DataFrame of table data
    '''
    @staticmethod
    def read_rds_table(table_name: str) -> pd.DataFrame:
        rds_table = pd.DataFrame
        engine = dc.init_db_engine()
        table_names = dc.list_db_tables(engine)
        if table_name in table_names:
            with engine.connect() as conn:
                rds_table = pd.read_sql(text(f"SELECT * FROM {table_name}"), con=conn)
        return rds_table
    
    '''
    The method connects to a specified PDF source and extracts the data from the document into a Pandas DataFrame

    file_link: string - PDF file location
    
    returns: Pandas DataFrame - A DataFrame of table data
    '''
    @staticmethod
    def retrieve_pdf_data(file_link: str) -> pd.DataFrame:
        df = pd.concat(read_pdf(file_link, pages='all', multiple_tables=True))
        return df
    
    '''
    The method calls an API to retrieve the number of stores available
    
    returns: int - number_stores value
    '''
    @staticmethod
    def list_number_of_stores(endpoint: str, header: str) -> int:
        request = requests.get(url=endpoint, headers=header)
        return request.json().get('number_stores')
    
    '''
    The method retrieves all the stores data
    
    returns: Pandas DataFrame - A DataFrame of table data
    '''
    @staticmethod
    def retrieve_stores_data(endpoint: str, header: str) -> pd.DataFrame:
        df = DataExtractor.retrieve_store_data(endpoint, header, 0)
        number_of_stores = DataExtractor.list_number_of_stores('https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores', header)
        for i in range(1, (number_of_stores - 1)):
            df = pd.concat([df, DataExtractor.retrieve_store_data(endpoint, header, i)], axis=0)
        return df

    '''
    The method calls an API to retrieve the store details specified

    store_number: str - The store number
    
    returns: Pandas DataFrame - A DataFrame of a single record
    '''
    @staticmethod
    def retrieve_store_data(endpoint: str, header: str, store_number: int) -> pd.DataFrame:
        request = requests.get(url=endpoint + str(store_number), headers=header)
        df = pd.DataFrame([request.json()])
        return df

if __name__ == "__main__":
    #Testing Methods
    print(DataExtractor.read_rds_table('legacy_users'))
    print(DataExtractor.retrieve_pdf_data('https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf'))
    print(DataExtractor.retrieve_stores_data('https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/', {'x-api-key': 'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}))
    

