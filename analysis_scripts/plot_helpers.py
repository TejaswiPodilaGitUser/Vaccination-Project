import matplotlib.pyplot as plt

def plot_scatter(x, y, title, xlabel, ylabel, ax=None):
    """
    Plot a scatter graph.
    
    Parameters:
        x (list): Values for the x-axis.
        y (list): Values for the y-axis.
        title (str): Title of the graph.
        xlabel (str): Label for the x-axis.
        ylabel (str): Label for the y-axis.
        ax (matplotlib.axes._axes.Axes, optional): Axes to plot on. Defaults to None.
        
    Returns:
        matplotlib.axes._axes.Axes: The Axes object with the plot.
    """
    if ax is None:
        fig, ax = plt.subplots()  # Create a new figure if ax is not provided
    ax.scatter(x, y)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return ax  # Return ax for further manipulation if needed

def plot_bar(x, y, title, xlabel, ylabel, ax=None, color=None):
    """
    Plot a bar graph.
    
    Parameters:
        x (list): Values for the x-axis (categories).
        y (list): Values for the y-axis (numeric values).
        title (str): Title of the graph.
        xlabel (str): Label for the x-axis.
        ylabel (str): Label for the y-axis.
        ax (matplotlib.axes._axes.Axes, optional): Axes to plot on. Defaults to None.
        color (str or list, optional): Color(s) for the bars. Defaults to None.
        
    Returns:
        matplotlib.axes._axes.Axes: The Axes object with the plot.
    """
    if ax is None:
        fig, ax = plt.subplots()  # Create a new figure if ax is not provided
    ax.bar(x, y, color=color)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis='x', rotation=30)  # Rotate x-axis labels for better visibility
    return ax  # Return ax for further manipulation if needed

def plot_line(x, y, title, xlabel, ylabel, ax=None):
    """
    Plot a line graph.
    
    Parameters:
        x (list): Values for the x-axis.
        y (list): Values for the y-axis.
        title (str): Title of the graph.
        xlabel (str): Label for the x-axis.
        ylabel (str): Label for the y-axis.
        ax (matplotlib.axes._axes.Axes, optional): Axes to plot on. Defaults to None.
        
    Returns:
        matplotlib.axes._axes.Axes: The Axes object with the plot.
    """
    if ax is None:
        fig, ax = plt.subplots()  # Create a new figure if ax is not provided
    ax.plot(x, y)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return ax  # Return ax for further manipulation if needed
