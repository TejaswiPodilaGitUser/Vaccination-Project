import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db_operations.query_executor import execute_query

def vaccine_intro_vs_disease_cases():
    """Analyze the trend in disease cases before and after vaccine introduction."""
    query = """
    SELECT vi.introduction_year, rc.disease_cases, rc.year
    FROM vaccine_introduction vi
    JOIN reported_cases rc
    ON vi.disease = rc.disease
    WHERE rc.year BETWEEN vi.introduction_year - 5 AND vi.introduction_year + 5
    """
    data = execute_query(query)
    # Further analysis and visualizations
    return data
