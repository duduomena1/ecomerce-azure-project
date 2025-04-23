import streamlit as st

# Define the pages
main_page = st.Page("main_page.py", title="Main Page", icon="🎈")
page_2 = st.Page("register.py", title="Register products", icon="🗃️")
page_3 = st.Page("users.py", title="Users", icon="👤")

# Set up navigation
pg = st.navigation([main_page, page_2, page_3])

# Run the selected page
pg.run()