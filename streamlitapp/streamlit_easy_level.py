import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import seaborn as sns

# Define base directory and cleaned data directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLEANED_XLSX_DIR = os.path.join(BASE_DIR, '../cleaned_xlsx')  # Move one level up

# Function to load data
@st.cache_data
def load_data(filename):
    filepath = os.path.join(CLEANED_XLSX_DIR, filename)
    return pd.read_excel(filepath, engine='openpyxl')

# Load datasets
coverage_data = load_data('cleaned_coverage_data.xlsx')
incidence_data = load_data('cleaned_incidence_rate.xlsx')
reported_cases_data = load_data('cleaned_reported_cases.xlsx')
vaccine_intro_data = load_data('cleaned_vaccine_introduction.xlsx')
vaccine_schedule_data = load_data('cleaned_vaccine_schedule_data.xlsx')

# Streamlit UI
st.title("📊 Vaccination Data Analysis")

# Query selection
query_options = [
    "How do vaccination rates correlate with a decrease in disease incidence?",
    "What is the drop-off rate between 1st dose and subsequent doses?",
    "Are vaccination rates different between genders?",
    "How does education level impact vaccination rates?",
    "What is the urban vs. rural vaccination rate difference?",
    "Has the rate of booster dose uptake increased over time?",
    "Is there a seasonal pattern in vaccination uptake?",
    "How does population density relate to vaccination coverage?",
    "Which regions have high disease incidence despite high vaccination rates?"
]
selected_query = st.selectbox("🔍 Select a Query:", query_options)

# Function to generate plots
def generate_plot(query):
    fig, ax = plt.subplots(figsize=(10, 5))

    if query == query_options[0]:  # Vaccination rates vs disease incidence
        merged_df = coverage_data.merge(incidence_data, on=["CODE", "YEAR"], how="inner")

        # Compute Pearson correlation
        corr, p_value = pearsonr(merged_df['COVERAGE'], merged_df['INCIDENCE_RATE'])

        # Define vaccine introduction year (adjust based on actual data)
        vaccine_year = 1995  

        # Compute average incidence before and after vaccination introduction
        before_vaccine = merged_df[merged_df['YEAR'] < vaccine_year]['INCIDENCE_RATE'].mean()
        after_vaccine = merged_df[merged_df['YEAR'] >= vaccine_year]['INCIDENCE_RATE'].mean()

        # Compute percentage decrease
        decrease_percentage = ((before_vaccine - after_vaccine) / before_vaccine) * 100

        # Display results
        st.write(f"### **Avg Disease Incidence Before {vaccine_year}:** {before_vaccine:.2f}")
        st.write(f"### **Avg Disease Incidence After {vaccine_year}:** {after_vaccine:.2f}")
        st.write(f"### **Percentage Decrease in Incidence:** {decrease_percentage:.2f}%")

        # Plot the incidence rate over the years
        sns.lineplot(data=merged_df, x="YEAR", y="INCIDENCE_RATE", marker='o', ax=ax, label="Disease Incidence")

        # Add a vertical line for vaccine introduction
        ax.axvline(x=vaccine_year, color='r', linestyle='--', label=f"Vaccine Introduced ({vaccine_year})")

        ax.set_xlabel("Year")
        ax.set_ylabel("Disease Incidence Rate")
        ax.set_title("Disease Incidence Over Time")
        ax.legend()
        ax.grid(True)

    elif query == query_options[1]:  # Drop-off rate between doses
        dose_counts = coverage_data.groupby(["NAME", "DOSES"]).agg({"COVERAGE": "mean"}).reset_index()

        # Compute drop-off rate between doses
        dose_counts['DROP_OFF'] = dose_counts.groupby("NAME")['COVERAGE'].pct_change() * 100

        # Display average drop-off rate
        avg_drop_off = dose_counts['DROP_OFF'].mean()
        st.write(f"### **Average Drop-off Rate Between Doses:** {avg_drop_off:.2f}%")

        # Plot drop-off trend
        sns.lineplot(data=dose_counts, x="DOSES", y="COVERAGE", hue="NAME", marker='o', ax=ax)
        ax.set_xlabel("Dose Number")
        ax.set_ylabel("Coverage (%)")
        ax.set_title("Drop-off Rate Between Doses")
        ax.legend(title="Vaccine")


    elif query == query_options[4]:  # Urban vs Rural Vaccination Difference
        vaccine_schedule_data_filtered = vaccine_schedule_data.head(20)  # Limiting for readability
        sns.barplot(data=vaccine_schedule_data_filtered, x="COUNTRYNAME", y="TARGETPOP", ax=ax)
        ax.set_title("Urban vs. Rural Vaccination Rate Difference")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    
    elif query == query_options[8]:  # High disease incidence despite high vaccination rates
        high_risk = incidence_data[(incidence_data["INCIDENCE_RATE"] > 50)].head(20)
        sns.barplot(data=high_risk, x="NAME", y="INCIDENCE_RATE", ax=ax)
        ax.set_title("High Disease Incidence Despite High Vaccination Rates")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

    st.pyplot(fig)

# Display plot
generate_plot(selected_query)
