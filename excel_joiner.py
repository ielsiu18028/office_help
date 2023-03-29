import pandas as pd
import streamlit as st
from io import BytesIO

# Set page title and layout
st.set_page_config(page_title="Excel Joiner", page_icon=":memo:", layout="wide")

# Define function to join Excel files
def join_excel_files(files):
    dfs = []
    for file in files:
        try:
            df = pd.read_excel(file)
            dfs.append(df)
        except Exception as e:
            st.warning(f"Unable to read file {file.name}: {e}")
    if len(dfs) == 0:
        st.warning("No files were uploaded")
    else:
        result = pd.concat(dfs)
        return result#.reset_index(inplace=True)

# Define app layout
st.title("Excel Joiner")
st.write("Upload your Excel files below")
uploaded_files = st.file_uploader("Upload Excel files", accept_multiple_files=True, type=['xls', 'xlsx'])
saved_name = st.text_input('Output file name', 'joined_data')
join_button = st.button("Join Excel files")

# Join Excel files when button is clicked
if join_button:
    joined = join_excel_files(uploaded_files)
    if joined is not None:
        st.write("Joined data:")
        st.write(joined)
        # Download joined Excel file
        output_download_virtual_file = BytesIO()
        with pd.ExcelWriter(output_download_virtual_file, engine='xlsxwriter') as writer:
            # Export Drop summary
            joined.to_excel(writer, sheet_name='Joined Data', index=False)

        st.download_button(
            label = "Download joined file",
            data = output_download_virtual_file,
            file_name = str(saved_name) + ".xlsx",
            mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
