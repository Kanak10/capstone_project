import pyodbc
import pandas as pd
import json
import os

from logger import logging

def main(config_path="config.json"):
    """
    Fetches data from a SQL Server table and returns it as a DataFrame.

    Args:
        config_path (str): Path to the configuration JSON file.

    Returns:
        pd.DataFrame: DataFrame containing the table data.
    """
    
    # Get tge directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logging.info((f"Script path: {script_dir}"))
    config_file = os.path.join(script_dir, config_path)
    logging.info(f"Config path: {config_file}")

    # Load configuration from JSON
    with open(config_file, 'r') as file:
        config = json.load(file)

    # Read SQL Server connection details
    server = config["sql_server"]["server"]
    database = config["sql_server"]["databases"]
    table = config["sql_server"]["table"]

    logging.info(f"Server: {server}, database: {database}, table: {table}")

    # Define connection string for Windows Authentication
    connection_string = (
        f"DRIVER={{SQL Server}};"
        f"SERVER={server};"
        f"DATABASE={database};"
        f"Trusted_Connection=yes"
    )
    logging.info(f"{connection_string}")\
    
    try:
        # Establsih connection
        conn = pyodbc.connect(connection_string)
        if conn:
            logging.info("Connection to SQL Server successful!")
        else:
            logging.info("Could not connect to SSMS")
        
        # Fetch data from the specified table
        query = f"SELECT * FROM {table}"
        df = pd.read_sql(query, conn)
        conn.cloase()
        logging.info(f"Data fetched successfully from table '{table}'.")
        return df
    except Exception as e:
        logging.error(f"Error connecting to SQL or fetching data: {e}")
        return None
