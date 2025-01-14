import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Input directory for cleaned data
input_dir = "cleaned_xlsx"
output_dir = "visualizations"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Function to visualize data
def visualize_data(file_name):
    print(f"\n--- Visualizing {file_name} ---\n")

    # Load the cleaned data
    file_path = os.path.join(input_dir, file_name)
    df = pd.read_excel(file_path)

    # Pairplot for correlations
    if df.select_dtypes(include=['number']).shape[1] > 1:
        sns.pairplot(df.select_dtypes(include=['number']), diag_kind='kde')
        plt.suptitle(f"Pairplot for {file_name}", y=1.02)
        plt.savefig(os.path.join(output_dir, f"pairplot_{file_name}.png"))
        plt.close()

    # Distribution plots for numerical columns
    for col in df.select_dtypes(include=['number']).columns:
        plt.figure(figsize=(8, 5))
        sns.histplot(df[col], kde=True, bins=30, color='blue')
        plt.title(f"Distribution of {col} in {file_name}")
        plt.savefig(os.path.join(output_dir, f"dist_{col}_{file_name}.png"))
        plt.close()

    print(f"Visualizations for {file_name} saved to {output_dir}.")

# List of cleaned datasets
datasets = [
    "cleaned_coverage_data.xlsx",
    "cleaned_incidence_rate.xlsx",
    "cleaned_reported_cases.xlsx",
    "cleaned_vaccine_introduction.xlsx",
    "cleaned_vaccine_schedule_data.xlsx",
]

# Process each dataset
for dataset in datasets:
    visualize_data(dataset)
