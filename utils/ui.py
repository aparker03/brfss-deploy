import streamlit as st

def configure_page():
    st.set_page_config(page_title="BRFSS Depression Explorer", layout="wide")
    if "csv_ready" not in st.session_state:
        st.session_state["csv_ready"] = False


def sidebar_filters(df):
    st.sidebar.header("Options")

    impute_method = st.sidebar.selectbox(
        "Imputation Method",
        options=["median", "mean", "mode", "zero", "none"],
        index=0
    )

    sex = st.sidebar.selectbox("Sex", ["All"] + sorted(df["_SEX"].dropna().unique()))
    hlth = st.sidebar.selectbox("General Health", ["All"] + sorted(df["GENHLTH"].dropna().unique()))
    educ = st.sidebar.selectbox("Education Level", ["All"] + sorted(df["EDUCA"].dropna().unique()))

    return impute_method, sex, hlth, educ


def apply_filters(df, sex, hlth, educ):
    filtered = df.copy()
    if sex != "All":
        filtered = filtered[filtered["_SEX"] == sex]
    if hlth != "All":
        filtered = filtered[filtered["GENHLTH"] == hlth]
    if educ != "All":
        filtered = filtered[filtered["EDUCA"] == educ]
    return filtered


def footer(impute_method):
    st.markdown("---")
    st.markdown(f"Built by Alexis Parker · BRFSS 2022 · Imputation method: **{impute_method.capitalize()}**")
