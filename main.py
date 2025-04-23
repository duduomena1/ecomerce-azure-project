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

st.title('Cadastro de Produtos')
product_name = st.text_input('Nome do Produto')
product_price = st.number_input('Preço do Produto', min_value=0.0, format="%.2f")
product_description = st.text_area('Descrição do Produto')
product_image = st.file_uploader('Imagem do Produto', type=['jpg','png', 'jpeg'])

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
        insert_sql = f"INSERT INTO Produtos (preco, nome, descricao, imagem_url) VALUES ('{product_price}', '{product_name}', '{product_description}', '{image_url}')"
        cursor.execute(insert_sql)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erro ao inserir produto: {e}")
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
        st.error(f"Erro ao listar produtos: {e}")
        return []
def list_products_screen():
    products = list_products()
    if products:
        cards_por_linha = 3
        cols = st.columns(cards_por_linha)
        for i, products in enumerate(products):
            col = cols[i % cards_por_linha]
            with col:
                st.markdown(f"**Nome:** {products[2]}")
                st.write(f"**Preço:** {products[1]}")
                st.write(f"**Descrição:** {products[3]}")
                if products[4]:
                    html_img = f'<img src="{products[4]}" alt="Imagem do Produto" width="200" height="200"/>'
                    st.markdown(html_img, unsafe_allow_html=True)
                st.write("---")

    else:
        st.info("Nenhum produto cadastrado.")

if st.button('Cadastrar Produto'):
    insert_product(product_name, product_price, product_description, product_image)
    return_message = 'Produto salvo com Sucesso'
    list_products_screen()

st.header('Produtos Cadastrados')
if st.button('Listar Produtos'):
    list_products_screen()
    st.success('Produtos listados com Sucesso')

