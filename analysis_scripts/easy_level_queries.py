import pandas as pd
import os
import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use('TkAgg')

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import plot functions from your helpers
from analysis_scripts.plot_helpers import plot_bar, plot_line, plot_scatter

# Define the base directory and cleaned data directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEANED_XLSX_DIR = os.path.join(BASE_DIR, 'cleaned_xlsx')
VACCINATION_COVERAGE = "Vaccination Coverage"

# List of expected file names
EXCEL_FILES = [
    'cleaned_coverage_data.xlsx',
    'cleaned_incidence_rate.xlsx',
    'cleaned_reported_cases.xlsx',
    'cleaned_vaccine_introduction.xlsx',
    'cleaned_vaccine_schedule_data.xlsx'
]

def calculate_and_display_min_max(df, value_column, label_column, fig, table_ax):
    try:
        min_value = df[value_column].min()
        max_value = df[value_column].max()
        min_label = df[df[value_column] == min_value][label_column].values[0]
        max_label = df[df[value_column] == max_value][label_column].values[0]

        min_max_data = {
            "Type": ["Min", "Max"],
            label_column: [min_label, max_label],
            value_column: [f"{min_value:,.2f}", f"{max_value:,.2f}"]
        }

        min_max_df = pd.DataFrame(min_max_data)
        table_ax.clear()
        table_ax.axis('off')
        table = table_ax.table(
            cellText=min_max_df.values,
            colLabels=min_max_df.columns,
            loc='center',
            cellLoc='center'
        )
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.auto_set_column_width(col=list(range(len(min_max_df.columns))))
        fig.suptitle("Vaccination Data Analysis", fontsize=16)
    except Exception as e:
        print(f"Error in calculate_and_display_min_max: {e}")


def load_all_cleaned_data():
    data = {}
    for file_name in EXCEL_FILES:
        file_path = os.path.join(CLEANED_XLSX_DIR, file_name)
        try:
            df = pd.read_excel(file_path)
            data[file_name] = df
        except Exception as e:
            print(f"Error loading data from {file_name}: {e}")
    return data


def query_vaccine_introduction_by_year(coverage_data, ax):
    """Query vaccine introduction grouped by year."""
    try:
        if 'INTRODUCTION_YEAR' not in coverage_data.columns:
            print("Skipping query: 'INTRODUCTION_YEAR' column not found.")
            return
        result = coverage_data.groupby('INTRODUCTION_YEAR')['COVERAGE'].sum().reset_index()
        plot_bar(result['INTRODUCTION_YEAR'], result['COVERAGE'], "Vaccine Introduction by Year", "Year", VACCINATION_COVERAGE, ax=ax)
    except Exception as e:
        print(f"Error in query_vaccine_introduction_by_year: {e}")


def query_vaccine_schedule_by_area(coverage_data, ax):
    """Query vaccine schedule grouped by area."""
    try:
        if 'CODE' not in coverage_data.columns:
            print("Skipping query: 'CODE' column not found.")
            return
        result = coverage_data.groupby('CODE')['COVERAGE'].mean().reset_index()
        plot_bar(result['CODE'], result['COVERAGE'], "Vaccine Schedule by Area", "Area", "Average Coverage", ax=ax)
    except Exception as e:
        print(f"Error in query_vaccine_schedule_by_area: {e}")


def query_disease_incidence_by_year(coverage_data, ax):
    """Query disease incidence grouped by year."""
    try:
        if 'YEAR' not in coverage_data.columns or 'INCIDENCE' not in coverage_data.columns:
            print("Skipping query: Required columns not found.")
            return
        coverage_data['INCIDENCE'] = pd.to_numeric(coverage_data['INCIDENCE'], errors='coerce')
        result = coverage_data.groupby('YEAR')['INCIDENCE'].sum().reset_index()
        plot_line(result['YEAR'], result['INCIDENCE'], "Disease Incidence by Year", "Year", "Incidence", ax=ax)
    except Exception as e:
        print(f"Error in query_disease_incidence_by_year: {e}")


def query_reported_cases_by_area(coverage_data, ax):
    """Query reported cases grouped by area."""
    try:
        if 'CODE' not in coverage_data.columns or 'REPORTED_CASES' not in coverage_data.columns:
            print("Skipping query: Required columns not found.")
            return
        coverage_data['REPORTED_CASES'] = pd.to_numeric(coverage_data['REPORTED_CASES'], errors='coerce')
        result = coverage_data.groupby('CODE')['REPORTED_CASES'].sum().reset_index()
        plot_bar(result['CODE'], result['REPORTED_CASES'], "Reported Cases by Area", "Area", "Reported Cases", ax=ax)
    except Exception as e:
        print(f"Error in query_reported_cases_by_area: {e}")
def query_total_vaccinations_by_year(coverage_data, ax):
    """Query total vaccinations grouped by year."""
    try:
        if 'YEAR' not in coverage_data.columns or 'TOTAL_VACCINATIONS' not in coverage_data.columns:
            print("Skipping query: Required columns not found.")
            return
        result = coverage_data.groupby('YEAR')['TOTAL_VACCINATIONS'].sum().reset_index()
        plot_bar(result['YEAR'], result['TOTAL_VACCINATIONS'], "Total Vaccinations by Year", "Year", "Total Vaccinations", ax=ax)
    except Exception as e:
        print(f"Error in query_total_vaccinations_by_year: {e}")

def query_vaccine_introduction_by_year(coverage_data, ax):
    """Query vaccine introduction grouped by year."""
    try:
        if 'INTRODUCTION_YEAR' not in coverage_data.columns:
            print("Skipping query: 'INTRODUCTION_YEAR' column not found.")
            return
        result = coverage_data.groupby('INTRODUCTION_YEAR')['COVERAGE'].sum().reset_index()
        plot_bar(result['INTRODUCTION_YEAR'], result['COVERAGE'], "Vaccine Introduction by Year", "Year", VACCINATION_COVERAGE, ax=ax)
    except Exception as e:
        print(f"Error in query_vaccine_introduction_by_year: {e}")


if __name__ == "__main__":
    data = load_all_cleaned_data()
    coverage_data = data.get('cleaned_coverage_data.xlsx')

    if coverage_data is not None:
        fig, axes = plt.subplots(6, 2, figsize=(20, 30))
        fig.suptitle("Vaccination Data Analysis", fontsize=16)
        plt.subplots_adjust(hspace=0.6, wspace=0.4)

        query_total_vaccinations_by_year(coverage_data, axes[0, 0])
        query_vaccine_schedule_by_area(coverage_data, axes[0, 1])
        calculate_and_display_min_max(coverage_data, 'COVERAGE', 'YEAR', fig, axes[1, 0])
        calculate_and_display_min_max(coverage_data, 'COVERAGE', 'CODE', fig, axes[1, 1])
        query_vaccine_introduction_by_year(coverage_data, axes[2, 0])
        query_vaccine_schedule_by_area(coverage_data, axes[2, 1])
        calculate_and_display_min_max(coverage_data, 'INTRODUCTION_YEAR', 'CODE', fig, axes[3, 0])
        calculate_and_display_min_max(coverage_data, 'SCHEDULE_YEAR', 'CODE', fig, axes[3, 1])
        query_disease_incidence_by_year(coverage_data, axes[4, 0])
        query_reported_cases_by_area(coverage_data, axes[4, 1])
        calculate_and_display_min_max(coverage_data, 'INCIDENCE', 'YEAR', fig, axes[5, 0])
        calculate_and_display_min_max(coverage_data, 'REPORTED_CASES', 'CODE', fig, axes[5, 1])

        plt.show()
