import matplotlib.pyplot as plt
import plotly.express as px

# Utility function to extract data for charts
def extract_data(data, key_idx=0, value_idx=1):
    keys = [item[key_idx] for item in data]
    values = [item[value_idx] for item in data]
    return keys, values

# Bar Chart
def plot_bar_chart(data, title, x_label, y_label, ax=None):
    categories, values = extract_data(data)
    if ax is None:
        fig, ax = plt.subplots()
    ax.bar(categories, values)
    ax.set_title(title, fontsize=6)
    ax.set_xlabel(x_label, fontsize=4)
    ax.set_ylabel(y_label, fontsize=4)
    ax.tick_params(axis='x', labelsize=4, rotation=30)
    plt.tight_layout()
    return ax

# Pie Chart
def plot_pie_chart(data, title):
    categories, values = extract_data(data)
    plt.pie(values, labels=categories, autopct='%1.1f%%', startangle=90)
    plt.title(title, fontsize=6)
    plt.axis('equal')
    plt.show()

# Line Chart
def plot_line_chart(data, title, x_label, y_label, ax=None):
    x, y = extract_data(data)
    if ax is None:
        fig, ax = plt.subplots()
    ax.plot(x, y, marker='o')
    ax.set_title(title, fontsize=6)
    ax.set_xlabel(x_label, fontsize=4)
    ax.set_ylabel(y_label, fontsize=4)
    ax.tick_params(axis='x', labelsize=4, rotation=30)
    ax.grid(True)
    plt.tight_layout()
    return ax

# Geographical Heatmap
def plot_geographical_heatmap(df, location_col, value_col):
    df = df.dropna(subset=[location_col, value_col])
    fig = px.choropleth(
        df,
        locations=location_col,
        color=value_col,
        hover_name=location_col,
        color_continuous_scale="Viridis"
    )
    fig.update_layout(title="Geographical Heatmap", title_font_size=8, title_x=0.5)
    fig.show()

# Scatter Plot
def plot_scatter_plot(df, x_col, y_col, title):
    fig = px.scatter(df, x=x_col, y=y_col, title=title)
    fig.update_layout(title_font_size=6, title_x=0.5)
    fig.show()
