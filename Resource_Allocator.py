import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.title("📊 Google Sheet Viewer & Updater")

# Load credentials from Streamlit secrets
creds = Credentials.from_service_account_info(st.secrets["gsheets"])
gc = gspread.authorize(creds)

# Google Sheet ID (from your secrets or hardcoded)
spreadsheet_id = st.secrets["gsheets"]["spreadsheet_id"]

# Open the spreadsheet
sh = gc.open_by_key(st.secrets["gsheets"]["spreadsheet_id"])
worksheet = sh.sheet1

# Function to read data
def get_data():
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

# Display current data
st.subheader("Current Data")
df = get_data()
st.dataframe(df)

st.subheader("Add a New User")
# Input fields
name = st.text_input("Name")
pet = st.text_input("Pet")

# Add button
if st.button("Add User"):
    if name and pet:
        worksheet.append_row([name, pet])
        st.success(f"Added {name} with pet {pet}!")

        # Refresh and show updated data
        df = get_data()
        st.dataframe(df)
    else:
        st.error("Please enter both Name and Pet.")
