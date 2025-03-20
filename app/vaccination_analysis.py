import os
import pandas as pd
from scipy.stats import pearsonr

# Define base directory and cleaned data directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLEANED_XLSX_DIR = os.path.join(BASE_DIR, '../cleaned_xlsx')

# Function to load data
def load_data(filename):
    filepath = os.path.join(CLEANED_XLSX_DIR, filename)
    return pd.read_excel(filepath, engine='openpyxl')

# Load datasets once here (not in other files)
coverage_data = load_data('cleaned_coverage_data.xlsx')
incidence_data = load_data('cleaned_incidence_rate.xlsx')
vaccine_schedule_data = load_data('cleaned_vaccine_schedule_data.xlsx')

def analyze_vaccination_vs_incidence_per_year():
    """Computes yearly correlation between vaccination coverage and disease incidence."""
    
    # Check if datasets are empty
    if coverage_data.empty or incidence_data.empty:
        print("❌ Coverage or Incidence dataset is empty.")
        return pd.DataFrame()

    # Ensure YEAR is numeric and CODE is consistent
    coverage_data["YEAR"] = pd.to_numeric(coverage_data["YEAR"], errors="coerce")
    incidence_data["YEAR"] = pd.to_numeric(incidence_data["YEAR"], errors="coerce")
    coverage_data["CODE"] = coverage_data["CODE"].astype(str).str.strip()
    incidence_data["CODE"] = incidence_data["CODE"].astype(str).str.strip()

    # Debugging: Print data samples before merging
    print("Coverage Data Sample:\n", coverage_data.head())
    print("Incidence Data Sample:\n", incidence_data.head())

    # Merge datasets
    merged_df = coverage_data.merge(incidence_data, on=["CODE", "YEAR"], how="inner")

    # Debugging: Check if merged_df is empty
    if merged_df.empty:
        print("❌ Merged DataFrame is empty. Check CODE and YEAR values.")
        print(f"Unique Coverage Years: {coverage_data['YEAR'].unique()}")
        print(f"Unique Incidence Years: {incidence_data['YEAR'].unique()}")
        print(f"Unique Coverage Codes: {coverage_data['CODE'].unique()}")
        print(f"Unique Incidence Codes: {incidence_data['CODE'].unique()}")
        return pd.DataFrame()

    # Compute correlation per year
    results = []
    
    for year in sorted(merged_df["YEAR"].unique()):
        yearly_data = merged_df[merged_df["YEAR"] == year]

        if yearly_data["COVERAGE"].count() > 1:  # Ensure at least two data points
            try:
                corr, p_value = pearsonr(yearly_data["COVERAGE"], yearly_data["INCIDENCE_RATE"])
            except ValueError:
                corr, p_value = None, None
        else:
            corr, p_value = None, None

        results.append({
            "YEAR": year,
            "correlation": round(corr, 2) if corr is not None else None,
            "p_value": round(p_value, 4) if p_value is not None else None,
            "avg_coverage": round(yearly_data["COVERAGE"].mean(), 2),
            "avg_incidence": round(yearly_data["INCIDENCE_RATE"].mean(), 2)
        })

    return pd.DataFrame(results)



def compute_drop_off_rate_per_year():
    """Computes per-year drop-off rates for vaccine schedules."""
    if vaccine_schedule_data is None or vaccine_schedule_data.empty:
        return pd.DataFrame(), 0

    # Convert TARGETPOP to numeric and drop NaNs
    vaccine_schedule_data["TARGETPOP"] = pd.to_numeric(vaccine_schedule_data["TARGETPOP"], errors="coerce")
    vaccine_schedule_data.dropna(subset=["TARGETPOP"], inplace=True)

    # Pivot table with year
    pivot_df = vaccine_schedule_data.pivot_table(
        index=["YEAR", "VACCINE_DESCRIPTION"], 
        columns="SCHEDULEROUNDS", 
        values="TARGETPOP", 
        aggfunc="mean"
    ).reset_index()

    drop_off_data = []

    for year in pivot_df["YEAR"].unique():
        yearly_df = pivot_df[pivot_df["YEAR"] == year].copy()

        drop_off_rates = {}
        for col in range(2, yearly_df.shape[1] - 1):  # Schedulerounds start at 2nd column
            first_dose = yearly_df.iloc[:, col]
            next_dose = yearly_df.iloc[:, col + 1]

            drop_off_rate = ((first_dose - next_dose) / first_dose.replace(0, float("nan"))) * 100
            drop_off_rates[f"Drop-off {col-1}-{col}"] = drop_off_rate.fillna(0)

        yearly_drop_off_df = pd.DataFrame(drop_off_rates)
        yearly_drop_off_df.insert(0, "VACCINE_DESCRIPTION", yearly_df["VACCINE_DESCRIPTION"])
        yearly_drop_off_df.insert(0, "YEAR", year)

        drop_off_data.append(yearly_drop_off_df)

    final_df = pd.concat(drop_off_data, ignore_index=True)

    return final_df, final_df.mean(numeric_only=True).mean()


# Example usage
if __name__ == "__main__":
    corr_df = analyze_vaccination_vs_incidence_per_year()
    print("Yearly correlation analysis:\n", corr_df)

    drop_off_df, avg_drop_off = compute_drop_off_rate_per_year()
    print("Yearly drop-off rate analysis:\n", drop_off_df)
    print("Average drop-off rate across years:", avg_drop_off)
