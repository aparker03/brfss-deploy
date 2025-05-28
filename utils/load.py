import pandas as pd
import streamlit as st

# Flag to toggle between full and sample dataset
USE_SAMPLE = True  # Set to False for full dataset

# Dropbox links
FULL_DATA_URL = "https://www.dropbox.com/scl/fi/7uu8km9qqinzpn3lcfl88/brfss_2022.csv?rlkey=er6mrhhizmhk6i9sn2coobo1h&st=65awlrqm&dl=1"
SAMPLE_DATA_URL = "https://www.dropbox.com/scl/fi/7qyci8spfk60szrj0nsml/brfss_sample.csv?rlkey=6dvfakgoqepu893vtrb134j28&st=zuqqjzrm&dl=1"  # Replace with your own sample file link

@st.cache_data
def load_data():
    url = SAMPLE_DATA_URL if USE_SAMPLE else FULL_DATA_URL
    df = pd.read_csv(url)
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
