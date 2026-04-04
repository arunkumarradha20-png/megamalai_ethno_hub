import streamlit as st
import pandas as pd
from PIL import Image
import os

@st.cache_data
def load_data():
    return pd.read_excel("xlfile.xlsx")

df = load_data()

st.title("ARUN KUMAR ")

# Select column
column = st.selectbox("Select column to search", df.columns)

# Decide input type
unique_values = df[column].dropna().unique()

# If column has few unique values → dropdown
if len(unique_values) < 20:
    value = st.selectbox("Select value", unique_values)
else:
    value = st.text_input("Enter value to search")

# Search button
if st.button("Search"):
    if isinstance(value, str):
        result = df[df[column].astype(str).str.contains(value, case=False, na=False)]
    else:
        result = df[df[column] == value]

    if not result.empty:
        st.success(f"Found {len(result)} result(s)")

        for _, row in result.iterrows():
            col1, col2 = st.columns([1, 2])

            with col1:
                if "Image" in df.columns:
                    image_path = row.get("Image", "")
                    if os.path.exists(str(image_path)):
                        st.image(image_path, width=150)

            with col2:
                for col in df.columns:
                    if col != "Image":
                        st.write(f"**{col}:** {row[col]}")

            st.markdown("---")
    else:
        st.warning("No matching data found")