import sqlite3
import pandas as pd

from config import TABLE_NAME

class SQLLoader:
    def __init__(self, db_path):
        self.db_path = db_path

    def create_connection(self):
        """Creates a connection to the SQLite database."""
        return sqlite3.connect(self.db_path)

    def load_data(self, df: pd.DataFrame, table_name: str = TABLE_NAME, if_exists: str = "replace"):
        """Loads a DataFrame into SQLite using pandas.to_sql and closes the connection."""
        conn = self.create_connection()
        try:
            df.to_sql(table_name, conn, if_exists=if_exists, index=False)
            conn.commit()
        finally:
            conn.close()

    def load_chunk(self, df: pd.DataFrame, table_name: str = TABLE_NAME, if_exists: str = "append"):
        self.load_data(df, table_name=table_name, if_exists=if_exists)