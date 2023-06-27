import pandas as pd
import yaml
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import text

# This class connects to both a remote DB server and a local DB server based on the db credentials in db_creds.yaml
class DatabaseConnector():
    def __init__(self) -> None:
        db_creds = self.read_db_creds()
        self.database_type = db_creds['LOCAL_DATABASE_TYPE']
        self.dbapi = db_creds['LOCAL_DBAPI']
        self.host = db_creds['LOCAL_HOST']
        self.user = db_creds['LOCAL_USER']
        self.password = db_creds['LOCAL_PASSWORD']
        self.database = db_creds['LOCAL_DATABASE']
        self.port = db_creds['LOCAL_PORT']

    def read_db_creds(self) -> dict:
        '''
        Reads the db credentials of the yaml file db_creds

        returns: dict - A dictionary of the db credentials
        '''
        with open('db_creds.yaml', 'r') as file:
            db_creds = yaml.safe_load(file)

            return db_creds
    
    def init_db_engine(self) -> create_engine:
        '''
        Creates an SQLAlchemy engine based on the credentials passed in from read_db_creds

        returns: create_engine - SQLAlchemy engine
        '''
        db_creds = self.read_db_creds()
        engine = create_engine(f"postgresql+psycopg2://{db_creds['RDS_USER']}:{db_creds['RDS_PASSWORD']}@{db_creds['RDS_HOST']}:{db_creds['RDS_PORT']}/{db_creds['RDS_DATABASE']}")
        return engine

    def list_db_tables(self, engine: create_engine) -> list:
        '''
        Lists the base table names in an SQLAlchemy object

        returns: list - List of table names
        '''
        table_names = []
        with engine.connect() as conn:
            result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';"))
            for row in result:
                table_names.append(row.table_name)
        return table_names
    
    def upload_to_db(self, df: pd.DataFrame, table_name: str) -> None:
        '''
        Uploads a Panda DataFrame to a specified table name in the database

        df: Pandas DataFrame - The Dataframe to upload to the local database
        table_name: str - The name of the table in the database to store the data

        returns: Nothing
    '''
        
        # Connect to the database and upload the data to the specified table
        engine = create_engine(f"{self.database_type}+{self.dbapi}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}")
        with engine.connect() as conn:
            df.to_sql(table_name, engine, if_exists='replace')

if __name__ == "__main__":
    # Testing Methods
    
    dc = DatabaseConnector()
    print(dc.read_db_creds())
    engine = dc.init_db_engine()
    print(engine)
    print(dc.list_db_tables(engine))

