import streamlit as st
import importlib

# Dictionary of pages
pages = {
    "1 Overview of annual school accounts of NYC public school": "page1",
    "2 Special Courses Insight": "page2",
    "3 Student Grade Distribution": "page3"
    # Add more pages as needed
}

# Sidebar selection
st.sidebar.title("Page:")
page = st.sidebar.selectbox("Select a page:", options=list(pages.keys()))

# Import the selected page module and call its show function
if page:
    page_module = importlib.import_module(pages[page])
    page_module.show()

