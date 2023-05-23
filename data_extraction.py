from database_utils import DatabaseConnector as dc
import pandas as pd

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
                rds_table = pd.read_sql(f"SELECT * FROM {table_name}", con=conn)
        return rds_table

if __name__ == "__main__":
    #Testing Methods
    print(DataExtractor.read_rds_table('legacy_users'))
