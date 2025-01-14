import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db_operations.query_executor import execute_query

def low_coverage_regions():
    """Identify regions with low vaccination coverage."""
    query = """
    SELECT region, vaccination_rate
    FROM coverage_data
    WHERE vaccination_rate < 50
    """
    data = execute_query(query)
    # Visualization or reporting logic here
    return data
