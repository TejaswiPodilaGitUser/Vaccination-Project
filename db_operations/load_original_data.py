import os
import sys

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common_load_utils import create_table, load_data

file_table_mapping = {
    "csv/coverage-data.xlsx": "coverage_data",
    "csv/incidence-rate-data.xlsx": "incidence_rate",
    "csv/reported-cases-data.xlsx": "reported_cases",
    "csv/vaccine-introduction-data.xlsx": "vaccine_introduction",
    "csv/vaccine-schedule-data.xlsx": "vaccine_schedule_data"
}

if __name__ == "__main__":
    for file_path, table_name in file_table_mapping.items():
        create_table(file_path, table_name)
        load_data(file_path, table_name)
