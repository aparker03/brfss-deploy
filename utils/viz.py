import streamlit as st
import plotly.express as px
import pandas as pd

def histogram_and_summary(df):
    st.subheader("Depression Index Distribution")
    col1, col2 = st.columns([3, 2])

    with col1:
        fig = px.histogram(
            df,
            x="DI",
            nbins=20,
            title="Distribution of Depression Index",
            labels={"DI": "Depression Index"},
        )
        fig.update_layout(margin=dict(t=40, r=10, l=10, b=40))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Summary Stats")
        st.metric("Filtered Responses", f"{len(df):,}")
        st.metric("Mean DI", f"{df['DI'].mean():.2f}")

def state_choropleth(df):
    st.subheader("Average Depression Index by State")
    state_avg = df.groupby("_STATE_ABV", as_index=False)["DI"].mean()

    fig = px.choropleth(
        state_avg,
        locations="_STATE_ABV",
        locationmode="USA-states",
        color="DI",
        scope="usa",
        color_continuous_scale=["yellow", "blue"],
        labels={"DI": "Depression Index"},
        title="State-Level Depression Index (Filtered View)"
    )
    fig.update_layout(margin=dict(t=20, r=20, l=20, b=20))
    st.plotly_chart(fig, use_container_width=True)

def group_comparison(df):
    st.subheader("Compare Depression Index Across Groups")
    group_var = st.selectbox(
        "Select grouping variable",
        options=["_SEX", "GENHLTH", "EDUCA"],
        format_func=lambda x: {
            "_SEX": "Sex",
            "GENHLTH": "General Health",
            "EDUCA": "Education Level"
        }[x]
    )

    fig = px.box(
        df,
        x=group_var,
        y="DI",
        color=group_var,
        title=f"Depression Index by {group_var.replace('_', '')}",
        labels={"DI": "Depression Index"},
        points=False  # Removed scatter points
    )
    st.plotly_chart(fig, use_container_width=True)

def download_csv_section(df):
    st.subheader("Download Filtered Data")

    if "csv_ready" not in st.session_state:
        st.session_state["csv_ready"] = False

    if not st.session_state["csv_ready"]:
        if st.button("📥 Click to Generate CSV"):
            st.session_state["csv_ready"] = True
            st.rerun()
    else:
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.success("✅ CSV is ready.")
        st.download_button(
            label="⬇️ Download Filtered CSV",
            data=csv_data,
            file_name="brfss_filtered_data.csv",
            mime="text/csv"
        )
