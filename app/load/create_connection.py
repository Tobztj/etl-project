import pyodbc as odbc
from configparser import ConfigParser
from app.logging.load_logger import load_logger

def database_connection(DRIVER, SERVER, DATABASE):

    try:
        connection_string = f"""
            DRIVER={DRIVER};
            SERVER={SERVER};
            DATABASE={DATABASE};
            Trust_Connection=yes;
            """
        conn = odbc.connect(connection_string, autocommit=True)
        load_logger.info("Database connection established successfully.")

    except ValueError as err:
        load_logger.error(f"Connection failed: {err}")

    return conn
