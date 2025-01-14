import matplotlib.pyplot as plt

def plot_scatter(x, y, title, xlabel, ylabel, ax=None):
    """Plot a scatter graph."""
    if ax is None:
        fig, ax = plt.subplots()  # Create a new figure if ax is not provided
    ax.scatter(x, y)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return ax  # Return ax for further manipulation if needed

def plot_bar(x, y, title, xlabel, ylabel, ax=None, color=None):
    """Plot a bar graph."""
    if ax is None:
        fig, ax = plt.subplots()  # Create a new figure if ax is not provided
    ax.bar(x, y, color=color)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis='x', rotation=30)  # Rotate x-axis labels if needed
    return ax  # Return ax for further manipulation if needed

def plot_line(x, y, title, xlabel, ylabel, ax=None):
    """Plot a line graph."""
    if ax is None:
        fig, ax = plt.subplots()  # Create a new figure if ax is not provided
    ax.plot(x, y)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return ax  # Return ax for further manipulation if needed
