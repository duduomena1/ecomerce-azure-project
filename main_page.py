import streamlit as st

def welcome():
    st.title("Welcome to the E-commerce Azure Project! 🎉")
    st.write("""
        This application allows you to:
        - Register products with details and images.
        - Store product data securely in Azure Blob Storage and SQL Database.
        - View and manage your product catalog.
    """)
    st.success("Get started by navigating to the 'Register' page!")


welcome()
