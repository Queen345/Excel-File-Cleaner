import streamlit as st
import streamlit.components as stc
import pandas as pd
import time
import re
import base64
timestr = time.strftime("%Y%m%d-%H%M%S")
global df
def remove_whitespace(df):
    """Function to remove white spaces from DataFrame"""
    df = df.applymap(lambda x: x.replace(" ", "") if isinstance(x, str) else x)
    return df

#remove duplicates
def checkDuplicates():
    df = df.drop_dulpicates()

def deleteDuplicates(df):
    duplicate_rows = df[df.duplicated()]
    if len(duplicate_rows)>0:
        df.drop_duplicates(inplace=True)
        df.to_excel(df, index=False)

# Create a function to upload the Excel file
def upload_file():
    global file
    file = st.file_uploader('Upload an Excel file', type=['xlsx','xls'])
    if file is not None:
        global df
        df = pd.read_excel(file)
    # else:
    #     st.error('Please upload an excel file', hidden=True)
    # if st.session_state.file_type != 'xlxs':
    #     st.error('Please upload an excel file')
    return df

# Create a function to clean the data
def clean_data(df):
    # checkSpaces = st.checkbox("Clean leading and trailing spaces")
    # checkCharacters = st.checkbox("Clean special characters")
    # checkMiddleSpace = st.checkbox("Provide space between words")
    # checkDuplicates = st.checkbox("Show duplicates")
    # deleteDuplicates = st.checkbox("Delete duplicates")

    col1,col2 = st.columns(2)
    checkSpaces = col1.checkbox("Remove leading and trailing spaces")
    checkCharacters = col2.checkbox("Remove special charaters")
    checkMiddleSpace = col1.checkbox("Provide Spaces in-between words")
    checkDuplicates = col2.checkbox("Check duplicates")
    deleteDuplicates = col1.checkbox("Delete Duplicates")

    if checkSpaces == True:
        # Remove spaces from the column names
        df = df.replace('^[\s]+|[\s]+$', '', regex=True)
        # r'^[A-Za-z]*( [A-Za-z]+)*$', ^[\s]+|[\s]+$
    
    if checkCharacters == True:
        # Remove special characters from the data
        df = df.replace('[^a-zA-Z0-9]', ' ', regex=True)

    if checkMiddleSpace == True:
        # Remove spaces from the column names
        df = df.replace('\\s+', ' ', regex=True)

    if checkDuplicates == True:
        duplicate_rows = df[df.duplicated()]
        if len(duplicate_rows)>0:
            st.warning("The excel file contains duplicate rows")
            st.write(duplicate_rows)
        else:
            st.success('The excel sheet does not contain any duplicates')

    if deleteDuplicates == True:
        duplicate_rows = df[df.duplicated()]
        if len(duplicate_rows)>0:
            df.drop_duplicates(inplace=True)
    return df

# Create a function to download the cleaned data
def download_data(df):
    st.download_button(
        label='Download Cleaned Data',
        filename='file.csv',
        data=df.to_excel(index=False),
        mime='text/csv'
    )

def csv_downloader(data):
    csvfile = data.to_csv()
    b64 = base64.b64encode(csvfile.encode()).decode()
    new_filename = "new_text_file_{}_.csv".format(timestr)
    st.markdown('#### Download File ###')
    href = f'<a href="data:file/csv;base64,{b64}" download="{new_filename}">Click Here!!</a>'
    st.markdown(href, unsafe_allow_html=True)

# Actions
st.header('Excel Data Cleaning Application')
# Create a function to display the cleaned data
def display_data(df):
    st.dataframe(df)
# Get the Excel file from the user
df = upload_file()
# Clean the data


df = clean_data(df)
# Display the cleaned data
csv_downloader(df)
display_data(df)
# Download the cleaned data
# download_data(df)


