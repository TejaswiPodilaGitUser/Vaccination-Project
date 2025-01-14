import pandas as pd
import numpy as np
import sys
import os
import seaborn as sns
import matplotlib.pyplot as plt

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db_operations.db_connections import create_connection, close_connection

# EDA Functions
def generate_eda(df, table_name):
    """
    Perform Exploratory Data Analysis (EDA) on the DataFrame.
    
    Parameters:
        df (pd.DataFrame): DataFrame to analyze.
        table_name (str): Name of the table for saving visualizations.
    """
    # Descriptive Statistics
    print(f"\nDescriptive statistics for {table_name}:\n", df.describe())

    # Correlation Matrix
    if df.select_dtypes(include=['number']).shape[1] > 1:
        plt.figure(figsize=(10, 8))
        sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
        plt.title(f"Correlation Matrix for {table_name}")
        plt.savefig(f"eda/{table_name}_correlation_matrix.png")
        plt.close()

    # Visualizing missing data (if any)
    if df.isnull().sum().any():
        sns.heatmap(df.isnull(), cbar=False, cmap='viridis')
        plt.title(f"Missing Data Heatmap for {table_name}")
        plt.savefig(f"eda/{table_name}_missing_data.png")
        plt.close()

    # Distribution of numerical columns
    for col in df.select_dtypes(include=['number']).columns:
        plt.figure(figsize=(8, 5))
        sns.histplot(df[col], kde=True, bins=30, color='blue')
        plt.title(f"Distribution of {col} in {table_name}")
        plt.savefig(f"eda/{table_name}_{col}_distribution.png")
        plt.close()

def handle_nulls(df, strategy='drop', threshold=0.8):
    """
    Handle null values in the DataFrame based on the strategy.
    
    Parameters:
        df (pd.DataFrame): Input DataFrame.
        strategy (str): 'drop' or 'impute'. Default is 'drop'.
        threshold (float): Threshold for dropping rows/columns. Default is 0.8.

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    if strategy == 'drop':
        df = df.dropna(thresh=int((1 - threshold) * len(df.columns)), axis=0)
    elif strategy == 'impute':
        for col in df.columns:
            if df[col].dtype in ['float64', 'int64']:
                df[col].fillna(df[col].median(), inplace=True)
            else:
                df[col].fillna(df[col].mode()[0], inplace=True)
    return df

def remove_duplicates(df):
    """
    Remove duplicate rows from the DataFrame.

    Parameters:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: DataFrame without duplicates.
    """
    return df.drop_duplicates()

def convert_dtypes(df):
    """
    Convert data types to optimize memory usage.

    Parameters:
        df (pd.DataFrame): Input DataFrame.

    Returns:
        pd.DataFrame: Optimized DataFrame.
    """
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].astype('category')
    return df

def process_and_clean_data(table_name, query):
    """
    Perform EDA, clean data, and save it to output directory.

    Parameters:
        table_name (str): Name of the table.
        query (str): SQL query to fetch data.
    """
    # Fetch data from database
    engine = create_connection()
    df = pd.read_sql_query(query, engine)
    engine.dispose()

    # Perform EDA
    generate_eda(df, table_name)

    # Handle missing values
    df_cleaned = handle_nulls(df, strategy='impute')

    # Remove duplicates
    df_cleaned = remove_duplicates(df_cleaned)

    # Optimize Data Types
    df_cleaned = convert_dtypes(df_cleaned)

    # Save Cleaned Data
    output_path = os.path.join("cleaned_xlsx", f"cleaned_{table_name}.xlsx")
    df_cleaned.to_excel(output_path, index=False)
    print(f"Cleaned data for {table_name} saved to {output_path}.")
