import pandas as pd
import numpy as np
import streamlit as st
from sklearn.preprocessing import MinMaxScaler

# === STATE MAPPING ===
state_mapping = {
    1: 'AL', 2: 'AK', 4: 'AZ', 5: 'AR', 6: 'CA', 8: 'CO', 9: 'CT', 10: 'DE', 11: 'DC', 12: 'FL',
    13: 'GA', 15: 'HI', 16: 'ID', 17: 'IL', 18: 'IN', 19: 'IA', 20: 'KS', 21: 'KY', 22: 'LA',
    23: 'ME', 24: 'MD', 25: 'MA', 26: 'MI', 27: 'MN', 28: 'MS', 29: 'MO', 30: 'MT', 31: 'NE',
    32: 'NV', 33: 'NH', 34: 'NJ', 35: 'NM', 36: 'NY', 37: 'NC', 38: 'ND', 39: 'OH', 40: 'OK',
    41: 'OR', 42: 'PA', 44: 'RI', 45: 'SC', 46: 'SD', 47: 'TN', 48: 'TX', 49: 'UT', 50: 'VT',
    51: 'VA', 53: 'WA', 54: 'WV', 55: 'WI', 56: 'WY', 72: 'PR'
}

# === LOAD DATA ===
@st.cache_data
def load_data():
    df = pd.read_csv("notebooks/brfss/data/brfss_2022.csv")
    df.columns = df.columns.str.upper().str.strip()

    df = df[df["_SEX"].isin([1.0, 2.0])]
    df = df[df["GENHLTH"].isin([1.0, 2.0, 3.0, 4.0, 5.0])]
    df = df[df["EDUCA"].isin([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])]

    df["_SEX"] = df["_SEX"].map({1.0: "Male", 2.0: "Female"})
    df["GENHLTH"] = df["GENHLTH"].map({
        1.0: "Excellent", 2.0: "Very Good", 3.0: "Good",
        4.0: "Fair", 5.0: "Poor"
    })
    df["EDUCA"] = df["EDUCA"].map({
        1.0: "Never attended / Kindergarten only",
        2.0: "Grades 1–8", 3.0: "Grades 9–11",
        4.0: "High School Graduate", 5.0: "Some College",
        6.0: "College Graduate"
    })

    return df

# === CLEAN + IMPUTE ===
def clean_and_impute(df, method="median"):
    df = df.copy()

    invalids = {
        "MENTHLTH": [77, 99],
        "POORHLTH": [77, 99],
        "ADDEPEV3": [7, 9],
        "LSATISFY": [7, 9],
        "EMTSUPRT": [7, 9],
        "SDHISOLT": [7, 9],
        "SDHSTRE1": [7, 9]
    }
    for col, codes in invalids.items():
        df[col] = df[col].replace(codes, np.nan)

    df["MENTHLTH"] = df["MENTHLTH"].replace(88, 0)
    df["POORHLTH"] = df["POORHLTH"].replace(88, 0)
    df["ADDEPEV3"] = df["ADDEPEV3"].map({1.0: 1.0, 2.0: 0.0}).astype(float)

    ordinal_vars = ["LSATISFY", "EMTSUPRT", "SDHISOLT", "SDHSTRE1"]
    df[ordinal_vars] = df[ordinal_vars].astype(float)

    def impute_column(col):
        if method == "median":
            return col.fillna(col.median())
        elif method == "mean":
            return col.fillna(col.mean())
        elif method == "mode":
            return col.fillna(col.mode().iloc[0] if not col.mode().empty else np.nan)
        elif method == "zero":
            return col.fillna(0)
        return col

    for col in ["MENTHLTH", "POORHLTH"] + ordinal_vars:
        df[col] = impute_column(df[col])

    df["_STATE_ABV"] = df["_STATE"].map(state_mapping)
    return df

# === DEPRESSION INDEX ===
def compute_DI(df):
    df = df.copy()
    weights = {
        'MENTHLTH': 8,
        'POORHLTH': 5,
        'LSATISFY': 8,
        'EMTSUPRT': 3,
        'SDHISOLT': 7,
        'SDHSTRE1': 3,
        'ADDEPEV3': 10
    }

    reverse = {
        'LSATISFY': {1.0: 4, 2.0: 3, 3.0: 2, 4.0: 1},
        'SDHISOLT': {1.0: 5, 2.0: 4, 3.0: 3, 4.0: 2, 5.0: 1},
        'SDHSTRE1': {1.0: 5, 2.0: 4, 3.0: 3, 4.0: 2, 5.0: 1}
    }

    df.replace(reverse, inplace=True)

    scaler = MinMaxScaler()
    scale_cols = [col for col in weights if col != "ADDEPEV3"]
    df[scale_cols] = scaler.fit_transform(df[scale_cols])

    df["DI"] = sum(df[col] * w for col, w in weights.items())
    df["DI"] = (df["DI"] - df["DI"].min()) / (df["DI"].max() - df["DI"].min())

    return df

# === FULL PIPELINE ===
@st.cache_data
def process_di_data(df_raw, method):
    imputed_df = clean_and_impute(df_raw, method)
    return compute_DI(imputed_df)
