import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from vaccination_analysis import analyze_vaccination_vs_incidence_per_year, compute_drop_off_rate_per_year

# Streamlit UI
st.title("📊 Vaccination Data Analysis")

# Query selection
query_options = [
    "How do vaccination rates correlate with a decrease in disease incidence?",
    "What is the drop-off rate between 1st dose and subsequent doses?"
]
selected_query = st.selectbox("🔍 Select a Query:", query_options)

# Initialize figure
fig, ax = plt.subplots(figsize=(10, 5))

if selected_query == query_options[0]:  # Vaccination vs Disease Incidence
    result = analyze_vaccination_vs_incidence_per_year()
    
    if result is not None and not result.empty and "data" in result:
        st.write(f"### **Correlation between Vaccination & Disease Incidence:** {result['correlation']:.3f}")
        st.write(f"### **P-value:** {result['p_value']:.5f}")
        st.write(f"### **Avg Disease Incidence Before Vaccine:** {result['before_vaccine']:.2f}")
        st.write(f"### **Avg Disease Incidence After Vaccine:** {result['after_vaccine']:.2f}")
        st.write(f"### **Percentage Decrease in Incidence:** {result['decrease_percentage']:.2f}%")

        # Plot incidence rate over time
        sns.lineplot(data=result["data"], x="YEAR", y="INCIDENCE_RATE", marker='o', ax=ax, label="Disease Incidence")
        ax.axvline(x=1995, color='r', linestyle='--', label="Vaccine Introduced (1995)")
        ax.set_xlabel("Year")
        ax.set_ylabel("Disease Incidence Rate")
        ax.set_title("Disease Incidence Over Time")
        ax.legend()
        ax.grid(True)
    else:
        st.error("❌ Data unavailable for Vaccination vs Incidence Analysis.")

elif selected_query == query_options[1]:  # Drop-off Rate Between Doses
    drop_off_result = compute_drop_off_rate_per_year()
    
    if drop_off_result and "drop_off_data" in drop_off_result:
        drop_off_df = drop_off_result["drop_off_data"]
        
        if not drop_off_df.empty:
            st.write(f"### **Average Drop-off Rate:** {drop_off_result['avg_drop_off']:.2f}%")
            
            # Convert drop-off rates to long format for better visualization
            drop_off_long = drop_off_df.melt(id_vars=["VACCINE_DESCRIPTION"], var_name="Dose Pair", value_name="Drop-off Rate")
            
            # Plot drop-off rates
            sns.lineplot(data=drop_off_long, x="Dose Pair", y="Drop-off Rate", hue="VACCINE_DESCRIPTION", marker='o', ax=ax)
            ax.set_xlabel("Dose Pair (1-2, 2-3, etc.)")
            ax.set_ylabel("Drop-off Rate (%)")
            ax.set_title("Drop-off Rate Between Doses")
            ax.legend(title="Vaccine")
            ax.grid(True)
        else:
            st.error("❌ No drop-off data available.")
    else:
        st.error("❌ Drop-off rate data is unavailable.")

# Display plot
st.pyplot(fig)