import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import os
import sys
import matplotlib.pyplot as plt
import io
from PIL import Image
import plotly.io as pio
import plotly.express as px

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db_operations.db_connections import create_connection, close_connection
from db_operations.queries import (
    get_vaccination_coverage_top_bottom,
    get_vaccination_and_disease_trends_grouped_by_area,
    get_highest_coverage_lowest_incidence_grouped_by_area,
    get_top_and_bottom_10_vaccination_coverage
)
from visualizations.charts import (
    plot_bar_chart, 
    plot_line_chart, 
    plot_scatter_plot, 
    plot_geographical_heatmap
)


# Function to fetch data from the database using the provided query function
def fetch_data(query_func):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(query_func())
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(data, columns=columns)
    cursor.close()
    conn.close()
    return df

# Function to plot vaccination coverage by region (Bar chart)
def visualize_vaccination_coverage_by_region(ax):
    df = fetch_data(get_top_and_bottom_10_vaccination_coverage)

    # Debug: Print the columns and the first few rows of the data
    print("1. DataFrame Columns:", df.columns)
    print("2. First few rows of the data:")
    print(df.head())

    # Check if the 'Area' and 'Average_Coverage' columns exist
    if 'CODE' not in df.columns or 'Average_Coverage' not in df.columns:
        print("3. Required columns ('CODE', 'Average Coverage') not found in the DataFrame.")
        return

    # Debug: Check if 'Area' contains expected data
    df_unique_names = df['CODE'].unique()
    print("3. Unique Areas in the data:", df_unique_names)
    df['CODE'] = df['CODE'].str[:6]

    # Plotting the bar chart
    plot_bar_chart(df[['CODE', 'Average_Coverage']].values, "Vaccination Coverage by Region", 'Region', 'Vaccination Coverage (%)', ax)

# Function to visualize vaccination and disease trends (Line chart)
def visualize_vaccination_and_disease_trends(ax):
    df = fetch_data(get_vaccination_and_disease_trends_grouped_by_area)

    # Debug: Print the columns and the first few rows of the data
    print("4. DataFrame Columns:", df.columns)
    print("5. First few rows of the data:")
    print(df.head())

    # Ensure that the 'YEAR' column is present in the DataFrame
    if 'YEAR' in df.columns:
        # Handle YEAR column to remove '.0' and convert to integers
        df['YEAR'] = df['YEAR'].apply(lambda x: int(float(x)) if isinstance(x, str) or isinstance(x, float) else x)
    else:
        print("6. 'YEAR' column not found in the DataFrame.")
        return

    # Ensure that the required columns are present in the DataFrame
    if 'Average Vaccination Coverage' in df.columns:
        plot_line_chart(df[['YEAR', 'Average Vaccination Coverage']].values, 
                        "Vaccination and Disease Incidence Trends", 
                        'Year', 'Vaccination Coverage (%)', ax)
        
        # Adjust font size for axis labels and ticks
        ax.tick_params(axis='both', labelsize=4)  # Adjust tick label font size

    else:
        print("6. Required column ('Average Vaccination Coverage') not found in the DataFrame.")



# Function to visualize highest coverage and lowest incidence (Scatter plot)
def visualize_highest_coverage_lowest_incidence(ax):
    df = fetch_data(get_highest_coverage_lowest_incidence_grouped_by_area)

    # Debug: Print the columns and the first few rows of the data
    print("7. DataFrame Columns:", df.columns)
    print("8. First few rows of the data:")
    print(df.head())

    # Check if the required columns are present
    if 'Average Vaccination Coverage' in df.columns and 'Average Disease Incidence' in df.columns:
        # Create Plotly scatter plot with smaller title font
        fig = plot_plotly_scatter(df)
        
        # Convert the Plotly figure to image
        img_bytes = fig.to_image(format="png", width=600, height=400)
        img = Image.open(io.BytesIO(img_bytes))
        
        # Display the image on the provided axis
        ax.imshow(img)
        ax.axis("off")  # Turn off axes for better visual appeal
       # ax.set_title("Highest Coverage and Lowest Disease Incidence", fontsize=8)  # Small font size
    else:
        print("Required columns ('Average Vaccination Coverage', 'Average Disease Incidence') not found in the DataFrame.")

# Function to visualize geographical heatmap using the chart utility
def visualize_geographical_heatmap(ax):
    df = fetch_data(get_vaccination_coverage_top_bottom)
    print("9. DataFrame Columns:", df.columns)
    print("10. First few rows of the data:")
    print(df.head())

    if 'NAME' not in df.columns or 'Average Coverage' not in df.columns:
        print("Error: Required columns ('NAME', 'Average Coverage') are missing from the DataFrame.")
        return

    # Create Plotly heatmap with smaller font size for title
    fig = px.choropleth(
        df,
        locations='NAME',
        color='Average Coverage',
        hover_name='NAME',
        color_continuous_scale="Viridis",
        title="Geographical Heatmap of Vaccination Coverage"
    )

    # Convert Plotly figure to image and render in Matplotlib subplot
    img_bytes = fig.to_image(format="png", width=600, height=400)
    img = Image.open(io.BytesIO(img_bytes))
    ax.imshow(img)
    ax.axis("off")  # Turn off axes for better visual appeal
   # ax.set_title("Geographical Heatmap", fontsize=8)  # Small font size

# Function to visualize highest coverage and lowest incidence (Scatter plot)
def visualize_highest_coverage_lowest_incidence(ax):
    df = fetch_data(get_highest_coverage_lowest_incidence_grouped_by_area)

    # Debug: Print the columns and the first few rows of the data
    print("7. DataFrame Columns:", df.columns)
    print("8. First few rows of the data:")
    print(df.head())

    # Check if the required columns are present
    if 'Average Vaccination Coverage' in df.columns and 'Average Disease Incidence' in df.columns:
        # Create Plotly scatter plot
        fig = plot_plotly_scatter(df)
        
        # Convert the Plotly figure to an image (PNG format)
        img_bytes = pio.to_image(fig, format="png", width=600, height=400)
        img = Image.open(io.BytesIO(img_bytes))
        
        # Display the image on the provided axis
        ax.imshow(img)
        ax.axis("off")  # Turn off axes for better visual appeal
        #ax.set_title("Highest Coverage and Lowest Disease Incidence")
    else:
        print("Required columns ('Average Vaccination Coverage', 'Average Disease Incidence') not found in the DataFrame.")

def plot_plotly_scatter(df):
    # Create a Plotly scatter plot
    fig = px.scatter(df, x='Average Vaccination Coverage', y='Average Disease Incidence', title="Highest Coverage and Lowest Disease Incidence")
    return fig  # Return the Plotly figure directly

# Main function to create a GUI with a scroll bar
def main():
    # Create the main Tkinter window
    root = tk.Tk()
    root.title("Vaccination Data Visualizations")
    root.geometry("500x200")

    # Create a frame for the scrollable area
    frame = ttk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    # Add a canvas and scrollbars to the frame
    canvas = tk.Canvas(frame)
    scrollbar_y = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar_x = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=canvas.xview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
    scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Create subplots for the visualizations
    fig, axes = plt.subplots(2, 2, figsize=(8, 6))  # Create a 2x2 grid of subplots

    # Call each visualization function
    visualize_vaccination_coverage_by_region(axes[0, 0])
    visualize_vaccination_and_disease_trends(axes[0, 1])
    visualize_highest_coverage_lowest_incidence(axes[1, 0])
    visualize_geographical_heatmap(axes[1, 1])

    # Embed the Matplotlib figure into the Tkinter canvas
    canvas_plot = FigureCanvasTkAgg(fig, master=scrollable_frame)
    canvas_plot.draw()
    canvas_plot.get_tk_widget().pack()

    plt.tight_layout()  # Adjust layout

    # Run the Tkinter event loop
    root.mainloop()

# Entry point of the script
if __name__ == "__main__":
    main()
