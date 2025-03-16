import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

st. set_page_config(layout="wide")

# Define the directory containing the cleaned datasets
DATA_DIR = "cleaned_xlsx"

# Available datasets
DATASETS = {
    "Coverage Data": "cleaned_coverage_data.xlsx",
    "Incidence Rate Data": "cleaned_incidence_rate.xlsx",
    "Reported Cases Data": "cleaned_reported_cases.xlsx",
    "Vaccine Introduction Data": "cleaned_vaccine_introduction.xlsx",
    "Vaccine Schedule Data": "cleaned_vaccine_schedule_data.xlsx"
}

# Function to load data
def load_data(file_name):
    file_path = os.path.join(DATA_DIR, file_name)
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Function to display dataset preview and summary statistics in two columns
def display_dataset(df):
    st.subheader("Dataset Overview")

    col1, col_spacer, col2 = st.columns([2, 0.2, 1])  # Data Preview (2), Spacer (0.2), Summary (1)

    with col1:
        st.write("### Data Preview")
        st.write(df.head())

    with col2:
        st.write("### Summary Statistics")
        st.write(df.describe())

# Function to visualize correlation matrix
def plot_correlation_matrix(df):
    st.subheader("Correlation Matrix")
    
    numeric_df = df.select_dtypes(include=['number'])  # Select only numeric columns
    
    if not numeric_df.empty:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt='.2f', ax=ax)
        st.pyplot(fig)
    else:
        st.warning("No numeric columns available for correlation matrix.")

# Function to visualize distributions in two columns
def plot_distributions(df):
    st.subheader("Feature Distributions")

    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        col1, col2 = st.columns(2)
        for i, col in enumerate(numeric_cols):
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.histplot(df[col], kde=True, bins=30, ax=ax)
            ax.set_title(f"Distribution of {col}")
            
            if i % 2 == 0:
                col1.pyplot(fig)
            else:
                col2.pyplot(fig)
    else:
        st.warning("No numeric columns found for distribution plots.")

# Main function
def main():
    st.title("Vaccination Data EDA")
    
    # Sidebar selection for dataset
    selected_dataset = st.sidebar.selectbox("Select a dataset", list(DATASETS.keys()))
    
    # Load selected dataset
    df = load_data(DATASETS[selected_dataset])

    if df is not None:
        display_dataset(df)  # Display preview & summary in 2 columns
        plot_correlation_matrix(df)  # Correlation Matrix
        plot_distributions(df)  # Feature Distributions in 2 columns

if __name__ == "__main__":
    main()
