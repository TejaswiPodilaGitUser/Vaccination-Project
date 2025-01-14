import pandas as pd
import os
import sys

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db_operations.db_connections import create_connection, close_connection

def create_table(file_path, table_name):
    connection = create_connection()
    if connection is None:
        return

    try:
        cursor = connection.cursor()

        # Check if the file exists
        if not os.path.exists(file_path):
            print(f"File {file_path} not found. Skipping...")
            return

        # Load Excel data
        data = pd.read_excel(file_path)

        # Replace 0, empty strings, and NaN with None
        data = data.replace({0: None, '': None})  # Replace 0 and empty string with None
        data = data.where(pd.notna(data), None)  # Replace NaN with None

        # Drop rows where all values are None
        data = data.dropna(how='all')

        # Get column names from the dataframe
        columns = data.columns.tolist()

        # Generate table creation query dynamically
        create_query = f"CREATE TABLE IF NOT EXISTS {table_name} ("
        for column in columns:
            if column.lower() == 'sourcecomment':
                create_query += f"`{column}` LONGTEXT, "
            else:
                create_query += f"`{column}` VARCHAR(255), "
        create_query = create_query.rstrip(", ") + ")"

        # Drop the table if it exists
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

        # Create the table
        cursor.execute(create_query)
        print(f"Table {table_name} created successfully.")

        connection.commit()
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        close_connection(connection)

def load_data(file_path, table_name):
    connection = create_connection()
    if connection is None:
        return

    try:
        cursor = connection.cursor()

        # Check if the file exists
        if not os.path.exists(file_path):
            print(f"File {file_path} not found. Skipping...")
            return

        # Load Excel data
        data = pd.read_excel(file_path)
        data = data.replace({0: None, '': None})  # Replace 0 and empty string with None
        data = data.where(pd.notna(data), None)  # Replace NaN with None
        data = data.dropna(how='all')

        # Prepare column names and data for insertion
        columns = ", ".join(f"`{col}`" for col in data.columns)
        placeholders = ", ".join(["%s"] * len(data.columns))
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        for row in data.itertuples(index=False):
            row_data = tuple(None if pd.isna(val) else val for val in row)
            try:
                cursor.execute(insert_query, row_data)
            except Exception as e:
                print(f"Error inserting row {row} into {table_name}: {e}")

        connection.commit()
        print(f"Data loaded successfully into {table_name}.")
    except Exception as e:
        print(f"Error loading data into table {table_name}: {e}")
    finally:
        close_connection(connection)
