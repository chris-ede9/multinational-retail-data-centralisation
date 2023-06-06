import yaml
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import text
import pandas as pd

# This class connects to a remote DB server based on the db credentials in db_creds.yaml
class DatabaseConnector():
    def __init__(self) -> None:
        pass
    
    '''
    Reads the db credentials of the yaml file db_creds

    returns: dict - A dictionary of the db credentials
    '''
    @staticmethod
    def read_db_creds() -> dict:
        with open('db_creds.yaml', 'r') as file:
            db_creds = yaml.safe_load(file)

            return db_creds
    
    '''
    Creates an SQLAlchemy engine based on the credentials passed in from read_db_creds

    returns: create_engine - SQLAlchemy engine
    '''
    @staticmethod
    def init_db_engine() -> create_engine:
        db_creds = DatabaseConnector.read_db_creds()
        engine = create_engine(f"postgresql+psycopg2://{db_creds['RDS_USER']}:{db_creds['RDS_PASSWORD']}@{db_creds['RDS_HOST']}:{db_creds['RDS_PORT']}/{db_creds['RDS_DATABASE']}")
        return engine

    '''
    Lists the base table names in an SQLAlchemy object

    returns: list - List of table names
    '''
    @staticmethod
    def list_db_tables(engine: create_engine) -> list:
        table_names = []
        with engine.connect() as conn:
            result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';"))
            for row in result:
                table_names.append(row.table_name)
        return table_names
    
    '''
    Uploads a Panda DataFrame to a specified table name in the database

    df: Pandas DataFrame - The Dataframe to upload to the local database
    table_name: str - The name of the table in the database to store the data

    returns: Nothing
    '''
    @staticmethod
    def upload_to_db(df: pd.DataFrame, table_name: str) -> None:
        # Local db credentials
        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        HOST = 'localhost'
        USER = 'postgres'
        PASSWORD = 'aicore'
        DATABASE = 'sales_data'
        PORT = 5434
        
        # Connect to the database and upload the data to the specified table
        engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")
        with engine.connect() as conn:
            df.to_sql(table_name, engine, if_exists='replace')

if __name__ == "__main__":
    # Testing Methods
    print(DatabaseConnector.read_db_creds())
    engine = DatabaseConnector.init_db_engine()
    print(engine)
    print(DatabaseConnector.list_db_tables(engine))

