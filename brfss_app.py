# apps/brfss/brfss_app.py

import streamlit as st
from utils import clean, viz, ui

# === Configure Layout ===
ui.configure_page()

# === Load and Process Data ===
df_raw = clean.load_data()
impute_method, sex, hlth, educ = ui.sidebar_filters(df_raw)
df_processed = clean.process_di_data(df_raw, impute_method)
filtered = ui.apply_filters(df_processed, sex, hlth, educ)

# === Page Title & Intro ===
st.title("BRFSS Depression Index Explorer (2022)")
st.caption("Explore patterns in mental health using a custom PHQ-9-based index with live filters and visualizations.")

# === Tabs ===
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Histogram", "🗺️ Choropleth Map", "📈 Group Comparison", "📥 Download"
])

with tab1:
    viz.histogram_and_summary(filtered)

with tab2:
    viz.state_choropleth(filtered)

with tab3:
    viz.group_comparison(filtered)

with tab4:
    viz.download_csv_section(filtered)

# === Footer ===
ui.footer(impute_method)
