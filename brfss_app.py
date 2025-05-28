import streamlit as st
from utils.load import load_data
from utils.clean import process_di_data
from utils.ui import configure_page, sidebar_filters, apply_filters, footer
from utils.viz import histogram_and_summary, state_choropleth, group_comparison, download_csv_section

# === CONFIGURE PAGE ===
configure_page()

# === LOAD AND PROCESS DATA ===
df_raw = load_data()
impute_method, sex, hlth, educ = sidebar_filters(df_raw)
df_processed = process_di_data(df_raw, impute_method)
filtered = apply_filters(df_processed, sex, hlth, educ)

st.warning(
    "Note: This deployed version uses a *sample* of the 2022 BRFSS dataset to improve load time. "
    "Visualizations and statistics are based on this subset. For full data analysis, run the app locally."
)

# === MAIN LAYOUT ===
st.title("BRFSS Depression Index Explorer (2022)")
st.caption("Explore patterns in mental health using a custom PHQ-9-based index with live filters and visualizations.")

with st.expander("ℹ️ About this app"):
    st.markdown("""
    This application visualizes mental health trends from the 2022 Behavioral Risk Factor Surveillance System (BRFSS), 
    focusing on a custom-built **Depression Index (DI)** based on PHQ-9-like variables, social support, and self-reported health.

    You can:
    - Filter by sex, education, and general health
    - Choose different imputation strategies for missing data
    - Compare depression trends across U.S. states and demographics
    - Download the filtered data for your own analysis

    The dataset is publicly available and processed from CDC’s BRFSS 2022 survey.
    """)

# === TABS ===
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Histogram", 
    "🗺️ Choropleth Map", 
    "📈 Group Comparison", 
    "📥 Download"
])

with tab1:
    histogram_and_summary(filtered)

with tab2:
    state_choropleth(filtered)

with tab3:
    group_comparison(filtered)

with tab4:
    download_csv_section(filtered)

# === FOOTER ===
footer(impute_method)
