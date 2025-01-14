import os
import sys
from common_load_utils import create_table, load_data

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Define a dictionary mapping cleaned file paths to table names
FILE_TABLE_MAPPING = {
    "cleaned_xlsx/cleaned_coverage_data.xlsx": "cleaned_coverage_data",
    "cleaned_xlsx/cleaned_incidence_rate.xlsx": "cleaned_incidence_rate",
    "cleaned_xlsx/cleaned_reported_cases.xlsx": "cleaned_reported_cases",
    "cleaned_xlsx/cleaned_vaccine_introduction.xlsx": "cleaned_vaccine_introduction",
    "cleaned_xlsx/cleaned_vaccine_schedule_data.xlsx": "cleaned_vaccine_schedule_data"
}

def process_file(file_path, table_name):
    """
    Process a single file by creating a table and loading data into it.

    Parameters:
        file_path (str): Path to the Excel file.
        table_name (str): Name of the table to create and load data into.
    """
    print(f"\nProcessing file: {file_path} -> Table: {table_name}")
    try:
        create_table(file_path, table_name)
        load_data(file_path, table_name)
        print(f"Successfully processed file: {file_path}")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def main():
    """
    Main function to process all files in the FILE_TABLE_MAPPING.
    """
    print("\n--- Starting Data Load Process ---")
    for file_path, table_name in FILE_TABLE_MAPPING.items():
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}. Skipping...")
            continue
        process_file(file_path, table_name)
    print("\n--- Data Load Process Completed ---")

if __name__ == "__main__":
    main()
