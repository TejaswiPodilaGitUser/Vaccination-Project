import pandas as pd
import mysql.connector  # Ensure this is added
import os
import sys

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db_operations.db_connections import create_connection, close_connection
from eda.data_cleaning import handle_nulls, remove_duplicates, convert_dtypes  # Import the necessary functions


def fetch_data_from_db(query):
    """
    Fetch data from the database using the provided SQL query with a cursor.

    Parameters:
        query (str): SQL query to execute.

    Returns:
        pd.DataFrame: DataFrame containing the query results.
    """
    connection = create_connection()  # Establish a connection
    try:
        cursor = connection.cursor(dictionary=True)  # Create a cursor object
        cursor.execute(query)  # Execute the query
        rows = cursor.fetchall()  # Fetch all rows from the query result
        df = pd.DataFrame(rows)  # Convert the rows to a DataFrame
    except mysql.connector.Error as err:
        print(f"Error fetching data: {err}")
        df = pd.DataFrame()  # Return an empty DataFrame in case of an error
    finally:
        cursor.close()  # Close the cursor
        close_connection(connection)  # Close the connection
    return df

def load_table_data(table_name):
    """
    Load all data from a specific table.

    Parameters:
        table_name (str): Name of the table to load.

    Returns:
        pd.DataFrame: DataFrame containing table data.
    """
    query = f"SELECT * FROM {table_name}"
    return fetch_data_from_db(query)

# Example usage:
if __name__ == "__main__":
    tables = ["coverage_data", "incidence_rate", "reported_cases", "vaccine_introduction", "vaccine_schedule_data"]

    for table in tables:
        print(f"\n--- Extracting and Cleaning Data for {table} ---")
        df = load_table_data(table)
        if not df.empty:
            print(f"Data for {table} extracted successfully.")
        else:
            print(f"No data found for {table}.")
