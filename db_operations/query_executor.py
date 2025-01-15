import os
import sys
# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_operations.db_connections import create_connection, close_connection

def execute_query(query):
    """Execute SQL query and return results as a list of dictionaries."""
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)  # Use dictionary cursor for row-to-dict conversion
    
    try:
        cursor.execute(query)
        results = cursor.fetchall()
    except Exception as err:
        print(f"Error: {err}")
        results = []

    finally:
        cursor.close()
        close_connection(connection)  # Reuse the existing close_connection function

    return results
