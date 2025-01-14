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

def load_cleaned_data(file_name):
    """Load cleaned data from the specified file in the cleaned_xlsx directory."""
    file_path = os.path.join(CLEANED_XLSX_DIR, file_name)
    try:
        return pd.read_excel(file_path)
    except Exception as e:
        print(f"Error loading data from {file_name}: {e}")
        return None


def query_total_vaccinations_by_year(coverage_data, ax):
    """Query total vaccinations grouped by year."""
    try:
        coverage_data['COVERAGE'] = pd.to_numeric(coverage_data['COVERAGE'], errors='coerce')
        result = coverage_data.groupby('YEAR')['COVERAGE'].sum().reset_index()
        plot_bar(result['YEAR'], result['COVERAGE'], "Total Vaccinations by Year", "Year", VACCINATION_COVERAGE, ax=ax)
    except Exception as e:
        print(f"Error in query_total_vaccinations_by_year: {e}")


def query_vaccination_coverage_by_area(coverage_data, ax):
    """Query vaccination coverage grouped by area and display top 10 and bottom 10 areas."""
    try:
        if 'CODE' not in coverage_data.columns:
            print("Skipping query: 'CODE' column not found in the data.")
            return
        
        coverage_data['COVERAGE'] = pd.to_numeric(coverage_data['COVERAGE'], errors='coerce')
        result = coverage_data.groupby('CODE')['COVERAGE'].mean().reset_index()

        # Sort data by coverage
        result_sorted = result.sort_values(by='COVERAGE', ascending=False)

        # Get top 10 and bottom 10 areas
        top_10 = result_sorted.head(10)
        bottom_10 = result_sorted.tail(10)
        
        # Combine top and bottom data for plotting
        combined = pd.concat([top_10, bottom_10])
        
        # Truncate names for better readability
        combined['Truncated_CODE'] = combined['CODE'].apply(lambda x: x[:8] + "..." if len(x) > 8 else x)

        # Plot the combined data
        plot_bar(
            combined['Truncated_CODE'],
            combined['COVERAGE'],
            "Vaccination Coverage by Area (Top 10 and Bottom 10)",
            "Area",
            "Average Coverage",
            ax=ax
        )

        # Rotate x-axis labels for better readability
        ax.set_xticklabels(combined['Truncated_CODE'], rotation=45, ha='right')

    except Exception as e:
        print(f"Error in query_vaccination_coverage_by_area: {e}")


def query_highest_vaccinated_antigen(coverage_data, ax):
    """Query the antigen with the highest vaccination coverage."""
    try:
        coverage_data['COVERAGE'] = pd.to_numeric(coverage_data['COVERAGE'], errors='coerce')
        result = coverage_data.groupby('ANTIGEN')['COVERAGE'].sum().reset_index()
        highest_vaccinated = result.sort_values(by='COVERAGE', ascending=False).head(20)
        plot_bar(highest_vaccinated['ANTIGEN'], highest_vaccinated['COVERAGE'], "Top 20 Highest Vaccinated Antigens", "Antigen", "Coverage", ax=ax)
    except Exception as e:
        print(f"Error in query_highest_vaccinated_antigen: {e}")


def query_lowest_vaccinated_year(coverage_data, ax):
    """Query the year with the lowest vaccination coverage."""
    try:
        coverage_data['COVERAGE'] = pd.to_numeric(coverage_data['COVERAGE'], errors='coerce')
        result = coverage_data.groupby('YEAR')['COVERAGE'].sum().reset_index()
        lowest_vaccinated_year = result.sort_values(by='COVERAGE', ascending=True).head(1)
        plot_bar(result['YEAR'], result['COVERAGE'], "Lowest Vaccinated Year", "Year",VACCINATION_COVERAGE, ax=ax)
    except Exception as e:
        print(f"Error in query_lowest_vaccinated_year: {e}")


def query_drop_off_rate(coverage_data, ax):
    """Query drop-off rate between 1st dose and subsequent doses."""
    try:
        # Group by DOSES and calculate counts
        dose_counts = coverage_data.groupby('DOSES')['COVERAGE'].count().reset_index()
        dose_counts.columns = ['Doses', 'Count']

        # Calculate drop-off rate
        dose_counts['Drop-Off Rate'] = dose_counts['Count'].diff().fillna(0)

        # Scatter plot for drop-off rates
        ax.scatter(dose_counts['Doses'], dose_counts['Drop-Off Rate'], color='blue', label='Drop-Off Rate')
        ax.plot(dose_counts['Doses'], dose_counts['Drop-Off Rate'], color='green', linestyle='--', label='Trend Line')
        ax.set_title("Drop-Off Rate Between Doses")
        ax.set_xlabel("Dose Number")
        ax.set_ylabel("Drop-Off Rate")
        ax.legend()
    except Exception as e:
        print(f"Error in query_drop_off_rate: {e}")


def query_yearly_pattern(coverage_data, ax):
    """Query yearly pattern in vaccination uptake."""
    try:
        # Check if 'YEAR' column exists
        if 'YEAR' not in coverage_data.columns:
            raise KeyError("Column 'YEAR' not found in coverage_data")

        # Group by year and calculate the total vaccination coverage
        result = coverage_data.groupby('YEAR')['COVERAGE'].sum().reset_index()

        # Plot the data
        plot_line(
            result['YEAR'], result['COVERAGE'],
            "Yearly Pattern in Vaccination Uptake", "Year", "Vaccination Coverage", ax=ax
        )
    except Exception as e:
        print(f"Error in query_yearly_pattern: {e}")


def query_population_density_vs_coverage(coverage_data, ax):
    """Query relationship between population density and vaccination coverage."""
    try:
        if 'POP_DENSITY' not in coverage_data.columns:
            print("Skipping query: 'POP_DENSITY' column not found in the data.")
            return
        result = coverage_data.groupby('POP_DENSITY')['COVERAGE'].mean().reset_index()
        plot_scatter(result['POP_DENSITY'], result['COVERAGE'], "Population Density vs. Vaccination Coverage", "Population Density", VACCINATION_COVERAGE, ax=ax)
    except Exception as e:
        print(f"Error in query_population_density_vs_coverage: {e}")


def query_high_disease_incidence_regions(coverage_data, ax):
    """Query regions with high disease incidence despite high vaccination rates."""
    try:
        coverage_data['DISEASE_INC'] = pd.to_numeric(coverage_data['DISEASE_INC'], errors='coerce')
        high_incidence = coverage_data[coverage_data['DISEASE_INC'] > coverage_data['COVERAGE']]
        plot_bar(high_incidence['CODE'], high_incidence['COVERAGE'], "High Disease Incidence Regions with High Vaccination Coverage", "Region", VACCINATION_COVERAGE, ax=ax)
    except Exception as e:
        print(f"Error in query_high_disease_incidence_regions: {e}")


def show_plots_in_scrollable_window(fig):
    """Display plots in a scrollable window using tkinter."""
    # Create tkinter root window
    root = tk.Tk()
    root.title("Vaccination Data Analysis")  # Set the window title

    # Create a frame for canvas and scrollbar
    frame = ttk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    # Add a canvas
    canvas = tk.Canvas(frame)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add a vertical scrollbar linked to the canvas
    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas to hold the figure
    figure_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=figure_frame, anchor="nw")

    # Add the Matplotlib figure to the tkinter frame
    canvas_agg = FigureCanvasTkAgg(fig, master=figure_frame)
    canvas_agg.draw()
    canvas_agg.get_tk_widget().pack()

    # Configure the canvas scroll region
    figure_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    # Run the tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    # Load the cleaned data
    coverage_data = load_cleaned_data('cleaned_coverage_data.xlsx')

    # Check data validity
    if coverage_data is not None:
        print("Coverage Data Loaded Successfully")
        
        # Create subplots for each query (adjusted to 3x2 grid for all 6 plots)
        fig, axes = plt.subplots(3, 2, figsize=(15, 18))  # 3 rows, 2 columns grid
        fig.suptitle("Vaccination Data Analysis", fontsize=16)

        # Execute queries and plot results
        query_total_vaccinations_by_year(coverage_data, axes[0, 0])
        query_vaccination_coverage_by_area(coverage_data, axes[0, 1])
        query_highest_vaccinated_antigen(coverage_data, axes[1, 0])
        query_lowest_vaccinated_year(coverage_data, axes[1, 1])
        query_drop_off_rate(coverage_data, axes[2, 0])
        query_yearly_pattern(coverage_data, axes[2, 1])

        # Adjust layout
        plt.tight_layout(rect=[0, 0, 1, 0.96])

        # Show plots in a scrollable window
        show_plots_in_scrollable_window(fig)
    else:
        print("Failed to load coverage data. Ensure the file exists and is accessible.")