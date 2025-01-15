import pandas as pd
import os
import sys
import matplotlib.pyplot as plt

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db_operations.db_connections import create_connection, close_connection
from db_operations.queries import get_vaccination_coverage_by_region, get_vaccination_and_disease_trends, get_highest_coverage_lowest_incidence
from visualizations.charts import plot_bar_chart, plot_line_chart, plot_scatter_plot, plot_geographical_heatmap

# Function to fetch data from the database using the provided query function
def fetch_data(query_func):
    # Establish connection using create_connection
    conn = create_connection()
    cursor = conn.cursor()
    
    # Execute the query passed as a function
    cursor.execute(query_func())
    data = cursor.fetchall()
    
    # Convert fetched data to a DataFrame for easier processing
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(data, columns=columns)
    
    # Close the cursor and connection separately
    cursor.close()  # Close the cursor here
    conn.close()  # Close the connection here
    
    return df
def visualize_multiple_plots():
    # Fetch data (example queries)
    df_coverage_by_region = fetch_data(get_vaccination_coverage_by_region)
    df_vaccination_trends = fetch_data(get_vaccination_and_disease_trends)

    # Create subplots: 1 row, 2 columns
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # Plot on the first subplot
    plot_bar_chart(df_coverage_by_region, "Vaccination Coverage by Region", "Region", "Vaccination Coverage (%)", axes[0])

    # Plot on the second subplot
    plot_line_chart(df_vaccination_trends, "Vaccination and Disease Trends", "Year", "Vaccination Coverage (%)", axes[1])

    # Show the plot
    plt.tight_layout()
    plt.show()
    
# Function to visualize easy-level question: Vaccination coverage by region
def visualize_vaccination_coverage_by_region():
    df = fetch_data(get_vaccination_coverage_by_region)
    plot_bar_chart(df, "Vaccination Coverage by Region", "Region", "Vaccination Coverage (%)")

# Function to visualize medium-level question: Vaccination and disease trends over time
def visualize_vaccination_and_disease_trends():
    df = fetch_data(get_vaccination_and_disease_trends)
    plot_line_chart(df, "Vaccination and Disease Incidence Trends", "Year", "Vaccination Coverage (%)")

# Function to visualize scenario-based question: Regions with highest vaccination coverage and lowest disease incidence
def visualize_highest_coverage_lowest_incidence():
    df = fetch_data(get_highest_coverage_lowest_incidence)
    plot_scatter_plot(df, "Vaccination Coverage", "Disease Incidence", "Highest Coverage and Lowest Disease Incidence")

# Main entry point to run all visualizations
def main():
    # Visualize all questions with subplots
    visualize_multiple_plots()

if __name__ == "__main__":
    main()
