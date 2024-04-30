import streamlit as st
from Dashboard import showSidebar
showSidebar()


st.title("Fahrzeuge zuweisen")


name = st.text_input("Name des Fahrzeugs", st.query_params["name"])
