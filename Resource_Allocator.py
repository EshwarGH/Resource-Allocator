import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.title("📊 Google Sheet Viewer & Updater")

# Load credentials from Streamlit secrets
creds = Credentials.from_service_account_info(st.secrets["gsheets"])
gc = gspread.authorize(creds)

# Open the spreadsheet using the URL from secrets
spreadsheet_url = st.secrets["gsheets"]["spreadsheet_url"]
sh = gc.open_by_url(spreadsheet_url)
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
