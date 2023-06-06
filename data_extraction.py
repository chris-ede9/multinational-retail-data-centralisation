from database_utils import DatabaseConnector as dc
import pandas as pd
from tabula.io import read_pdf
from sqlalchemy import text

# This Class extracts data from a data source and converts to a Pandas DataFrame
class DataExtractor():
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

if __name__ == "__main__":
    #Testing Methods
    print(DataExtractor.read_rds_table('legacy_users'))
    print(DataExtractor.retrieve_pdf_data('https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf'))
