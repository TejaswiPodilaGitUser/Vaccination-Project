import matplotlib.pyplot as plt
import pandas as pd

def plot_line_chart(df, x_col, y_col, title, xlabel, ylabel):
    """Utility for plotting line charts."""
    plt.plot(df[x_col], df[y_col])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

def read_cleaned_data(file_path):
    """Read cleaned Excel data."""
    return pd.read_excel(file_path)
