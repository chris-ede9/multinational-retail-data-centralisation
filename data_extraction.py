import boto3
import pandas as pd
import requests
from database_utils import DatabaseConnector
from io import StringIO
from sqlalchemy import text
from tabula.io import read_pdf


# This Class extracts data from a data source and converts to a Pandas DataFrame
class DataExtractor():
    def __init__(self) -> None:
        '''
        The initialiser method
        '''
        pass

    @staticmethod
    def read_rds_table(table_name: str) -> pd.DataFrame:
        '''
        The method connects to a specified data source and extracts the data from a given table into a Pandas DataFrame

        table_name: string - Name of the table
        
        returns: Pandas DataFrame - A DataFrame of table data
        '''
        
        dc = DatabaseConnector()
        rds_table = pd.DataFrame
        engine = dc.init_db_engine()
        table_names = dc.list_db_tables(engine)
        if table_name in table_names:
            with engine.connect() as conn:
                rds_table = pd.read_sql(text(f"SELECT * FROM {table_name}"), con=conn)
        return rds_table
    
    @staticmethod
    def retrieve_pdf_data(file_link: str) -> pd.DataFrame:
        '''
        The method connects to a specified PDF source and extracts the data from the document into a Pandas DataFrame

        file_link: string - PDF file location
        
        returns: Pandas DataFrame - A DataFrame of table data
        '''

        df = pd.concat(read_pdf(file_link, pages='all', multiple_tables=True))
        return df
    
    @staticmethod
    def list_number_of_stores(endpoint: str, header: str) -> int:
        '''
        The method calls an API to retrieve the number of stores available
        
        returns: int - number_stores value
        '''
        
        request = requests.get(url=endpoint, headers=header)
        return request.json().get('number_stores')
    
    @staticmethod
    def retrieve_stores_data(endpoint: str, header: str) -> pd.DataFrame:
        '''
        The method retrieves all the stores data
        
        returns: Pandas DataFrame - A DataFrame of table data
        '''
        df = DataExtractor.retrieve_store_data(endpoint, header, 0)
        number_of_stores = DataExtractor.list_number_of_stores('https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores', header)
        for i in range(1, number_of_stores):
            df = pd.concat([df, DataExtractor.retrieve_store_data(endpoint, header, i)], axis=0)
        return df

    @staticmethod
    def retrieve_store_data(endpoint: str, header: str, store_number: int) -> pd.DataFrame:
        '''
        The method calls an API to retrieve the store details specified

        store_number: str - The store number
        
        returns: Pandas DataFrame - A DataFrame of a single record
        '''
        request = requests.get(url=endpoint + str(store_number), headers=header)
        df = pd.DataFrame([request.json()])
        return df
    
    @staticmethod
    def extract_from_s3(s3_file_path: str) -> pd.DataFrame:
        '''
        The method connects to an S3 bucket and retrieves a specified file

        s3_file_path: str - The CSV file location of the S3 bucket
        
        returns: Pandas DataFrame - A DataFrame of table data
        '''

        # Check if valid s3 address
        if s3_file_path.startswith('s3://'):
            # Remove the additional / in the URL
            s3_file_path = s3_file_path.replace(":/", "")

            # Split out the file path client, bucket name and file name from the file link
            client = boto3.client(s3_file_path.split('/')[0])
            bucket_name = s3_file_path.split('/')[1]
            file_name = s3_file_path.split('/')[2]

            # Extract the CSV data
            csv_obj = client.get_object(Bucket=bucket_name, Key=file_name)
            body = csv_obj['Body']
            csv_string = body.read().decode('utf-8')

            # Convert to a Pandas DataFrame
            df = pd.read_csv(StringIO(csv_string))
            return df
        else:
            print("Invalid S3 Bucket location entered")
            return None

    @staticmethod
    def retrieve_event_data(s3_url_path: str) -> pd.DataFrame:
        '''
        The method retrieves a JSON file stored on S3

        s3_url_path: str - The JSON file location of the S3 bucket
        
        returns: Pandas DataFrame - A DataFrame of the json file
        '''
        request = requests.get(url=s3_url_path)
        df = pd.DataFrame(request.json())
        return df

if __name__ == "__main__":
    #Testing Methods
    print(DataExtractor.read_rds_table('legacy_users'))
    print(DataExtractor.retrieve_pdf_data('https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf'))
    print(DataExtractor.retrieve_stores_data('https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/', {'x-api-key': 'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}))
    print(DataExtractor.extract_from_s3('s3://data-handling-public/products.csv'))
    print(DataExtractor.read_rds_table('orders_table'))
    print(DataExtractor.retrieve_event_data('https://data-handling-public.s3.eu-west-1.amazonaws.com/date_details.json'))