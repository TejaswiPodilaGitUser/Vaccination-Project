import matplotlib.pyplot as plt
import plotly.express as px

# Function for Bar Chart (Vaccination Coverage and Disease Incidence)
def plot_bar_chart(data, title, x_label, y_label, ax=None):
    categories = [item[0] for item in data]
    values = [item[1] for item in data]

    if ax is None:
        fig, ax = plt.subplots()  # Create a new figure if ax is not provided
    ax.bar(categories, values)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.tick_params(axis='x', rotation=45)  # Rotate x-axis labels for better visibility
    plt.tight_layout()
    return ax  # Return ax for further manipulation if needed

# Function for Pie Chart (Distribution of Vaccination Coverage or Disease Incidence)
def plot_pie_chart(data, title):
    categories = [item[0] for item in data]
    values = [item[1] for item in data]

    plt.pie(values, labels=categories, autopct='%1.1f%%', startangle=90)
    plt.title(title)
    plt.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
    plt.show()

# Function for Line Chart (Trends in Vaccination Coverage or Disease Rates)
def plot_line_chart(data, title, x_label, y_label, ax=None):
    x = [item[0] for item in data]
    y = [item[1] for item in data]

    if ax is None:
        fig, ax = plt.subplots()  # Create a new figure if ax is not provided
    ax.plot(x, y, marker='o')
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.grid(True)
    plt.tight_layout()
    return ax  # Return ax for further manipulation if needed

# Function for Geographical Heatmap (Vaccination Coverage or Disease Incidence by Region)
def plot_geographical_heatmap(df, location_col, value_col):
    fig = px.choropleth(df, 
                        locations=location_col, 
                        color=value_col, 
                        hover_name=location_col, 
                        color_continuous_scale="Viridis")
    fig.update_layout(title="Geographical Heatmap")
    fig.show()

# Function for Scatter Plot (Correlation between Vaccination Coverage and Disease Incidence)
def plot_scatter_plot(df, x_col, y_col, title):
    fig = px.scatter(df, x=x_col, y=y_col, title=title)
    fig.show()
