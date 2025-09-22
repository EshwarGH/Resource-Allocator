import streamlit as st
import pandas as pd
import gspread

st.title("📊 Google Sheet Viewer & Updater")

# Load service account credentials from Streamlit secrets
service_account_info = dict(st.secrets["gsheets"])
gc = gspread.service_account_from_dict(service_account_info)

# Google Sheet ID (from secrets.toml or hardcode if needed)
spreadsheet_id = st.secrets["gsheets"]["spreadsheet_id"]

# Open the spreadsheet
sh = gc.open_by_key(spreadsheet_id)
worksheet = sh.sheet1

# Function to read data
def get_data():
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

# Display current data
st.subheader("Current Data")
df = get_data()
st.dataframe(df)

# Section to add a new user
st.subheader("Add a New User")
name = st.text_input("Name")
pet = st.text_input("Pet")

# Add button
if st.button("Add User"):
    if name and pet:
        # Append new row to Google Sheet
        worksheet.append_row([name, pet])
        st.success(f"Added {name} with pet {pet}!")

        # Refresh data
        df = get_data()
        st.dataframe(df)
    else:
        st.error("Please enter both Name and Pet.")
