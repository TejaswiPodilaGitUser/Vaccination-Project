import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

def create_connection():
    host = os.getenv("DB_HOST")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")

    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        if connection.is_connected():
            print("Database connected.")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def close_connection(connection):
    """
    Closes the database connection.

    Args:
        connection (mysql.connector.connection): MySQL connection object.
    """
    if connection and connection.is_connected():
        connection.close()
        print("Database connection closed.")

# Example usage
if __name__ == "__main__":
    # Create a connection to the database
    conn = create_connection()

    # Perform your database operations here...

    # Close the connection
    close_connection(conn)
