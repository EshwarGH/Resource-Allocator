import streamlit as st
import pandas as pd
import gspread

st.title("📊 Google Sheet Viewer & Updater")

# Use service_account_from_dict to avoid dealing with JSON file
gc = gspread.service_account_from_dict(st.secrets["gsheets"])

# Extract spreadsheet ID from URL
spreadsheet_url = st.secrets["gsheets"]["spreadsheet_url"]
spreadsheet_id = spreadsheet_url.split("/d/")[1].split("/")[0]

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

st.subheader("Add a New User")
name = st.text_input("Name")
pet = st.text_input("Pet")

if st.button("Add User"):
    if name and pet:
        worksheet.append_row([name, pet])
        st.success(f"Added {name} with pet {pet}!")
        df = get_data()
        st.dataframe(df)
    else:
        st.error("Please enter both Name and Pet.")
