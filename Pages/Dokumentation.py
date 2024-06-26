import streamlit as st
from Dashboard import show_sidebar

st.set_page_config(page_title="Dokumentation",
                   page_icon="🚧",
                   layout="wide")
show_sidebar()
st.image("logo.png")
password_placeholder = st.empty()
password_input = password_placeholder.text_input("Passwort", type="password", key="pw_box")

if password_input == st.secrets["docs_pw"]:
    password_placeholder.empty()
    st.title("Dokumentation")
    st.write(st.secrets["repo"])
    st.divider()
    with open("Dokumentation.pdf", "rb") as file:
        pdf = file.read()
        st.download_button("Download Dokumentation", data=pdf, file_name="Doku.pdf")
