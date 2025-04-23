import streamlit as st
from azure.storage.blob import BlobServiceClient
import os
import pymssql
import uuid
import json
from dotenv import load_dotenv

load_dotenv()

blobConnectionString = os.getenv('BLOB_CONNECTION_STRING')
blobContainerName = os.getenv('BLOB_CONTAINER_NAME')
blobAccountName = os.getenv('BLOB_ACCOUNT_NAME')
sqlServer = os.getenv('SQL_SERVER')
sqlDatabase = os.getenv('SQL_DATABASE')
sqlUsername = os.getenv('SQL_USER')
sqlPassword = os.getenv('SQL_PASSWORD')

st.title('User Registration')
user_name = st.text_input('Full Name')
user_email = st.text_input('Best Email')
user_phone = st.text_input('Phone Number')


def register_user():
    try:
        conn = pymssql.connect(server=sqlServer, user=sqlUsername, password=sqlPassword, database=sqlDatabase)
        cursor = conn.cursor()
        insert_sql = f"INSERT INTO Users (user_name, user_email, user_phone  ) VALUES ('{user_name}', '{user_email}', '{user_phone}')"
        cursor.execute(insert_sql)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
            st.error(f"Error registering user : {e}")
            return False 


if st.button('Register'):
    if register_user():
        st.success("User registered successfully!")
    else:
        st.error("Error registering user.")