import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    df = pd.read_csv("https://drive.google.com/file/d/1kBfb36YYRPS2ouLCK0-UQcczTmC3SFUh/view?usp=drive_link")
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
