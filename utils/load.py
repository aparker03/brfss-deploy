import streamlit as st
import os
st.write("Running in:", os.getcwd())

from utils.load import load_data
from utils.clean import process_di_data
from utils.ui import configure_page, sidebar_filters, apply_filters, footer
from utils.viz import histogram_and_summary, state_choropleth, group_comparison, download_csv_section

# === CONFIGURE PAGE ===
configure_page()

# === LOAD AND PROCESS DATA ===
try:
    df_raw = load_data()
    st.write(f"✅ Loaded data with {df_raw.shape[0]:,} rows and {df_raw.shape[1]} columns.")
except Exception as e:
    st.error(f"❌ Failed to load data: {e}")
    st.stop()

impute_method, sex, hlth, educ = sidebar_filters(df_raw)
df_processed = process_di_data(df_raw, impute_method)
filtered = apply_filters(df_processed, sex, hlth, educ)
