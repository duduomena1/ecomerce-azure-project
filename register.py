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

st.title('Product registration')
product_name = st.text_input('Name of the Product')
product_price = st.number_input('Price', min_value=0.0, format="%.2f")
product_description = st.text_area('Description')
product_image = st.file_uploader('Image', type=['jpg','png', 'jpeg'])

#save image on Blob
def upload_blob(file):
    blob_service_client = BlobServiceClient.from_connection_string(blobConnectionString)
    container_client = blob_service_client.get_container_client(blobContainerName)
    blob_name = str(uuid.uuid4()) + file.name
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(file.read(), overwrite=True)
    image_url = f"https://{blobAccountName}.blob.core.windows.net/{blobContainerName}/{blob_name}"
    return image_url

def insert_product(product_name, product_price, product_description, product_image):
    try:
        image_url = upload_blob(product_image)
        conn = pymssql.connect(server=sqlServer, user=sqlUsername, password=sqlPassword, database=sqlDatabase)
        cursor = conn.cursor()
        insert_sql = f"INSERT INTO Produtos (price, name, description, image_url) VALUES ('{product_price}', '{product_name}', '{product_description}', '{image_url}')"
        cursor.execute(insert_sql)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"error registering product : {e}")
        return False

def list_products():
    try:
        conn = pymssql.connect(server=sqlServer, user=sqlUsername, password=sqlPassword, database=sqlDatabase)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Produtos")
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        st.error(f"Error listing product: {e}")
        return []
def list_products_screen():
    products = list_products()
    if products:
        cards_por_linha = 3
        cols = st.columns(cards_por_linha)
        for i, products in enumerate(products):
            col = cols[i % cards_por_linha]
            with col:
                st.markdown(f"**Name:** {products[2]}")
                st.write(f"**Price:** {products[1]}")
                st.write(f"**Description:** {products[3]}")
                if products[4]:
                    html_img = f'<img src="{products[4]}" alt="Image Product" width="200" height="200"/>'
                    st.markdown(html_img, unsafe_allow_html=True)
                st.write("---")

    else:
        st.info("No products registered.")

if st.button('Register Product'):
    insert_product(product_name, product_price, product_description, product_image)
    return_message = 'Product registered successfully!'
    list_products_screen()

st.header('Products List')
if st.button('List Products'):
    list_products_screen()
    st.success('Products listed successfully!')

