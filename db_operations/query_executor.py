import sys
import os
from sqlalchemy import text
from db_operations.db_connections import create_connection, close_connection

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def execute_query(query):
    """Execute SQL query and return results."""
    connection = create_connection()  # Reuse the existing connection from db_connection.py
    
    # Execute the query using SQLAlchemy connection
    with connection.connect() as conn:
        # Wrap the query string in text() to make it executable
        result = conn.execute(text(query)).fetchall()
    
    # No need to close connection manually as it's managed by SQLAlchemy's connection context
    return result
