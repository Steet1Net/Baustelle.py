import streamlit as st
from sqlalchemy import text
from Dashboard import showSidebar

db = st.connection('mysql', type='sql')

showSidebar()

st.title("Neue Baustelle hinzufügen")
with st.form("Baustelle hinzufügen", clear_on_submit=True):
    name = st.text_input("Name der Baustelle")
    col1, col2 = st.columns(2)
    with col1:
        start = st.date_input("Startdatum")
    with col2:
        ende = st.date_input("Enddatum")
    with st.expander("Adresse"):
        col1, col2 = st.columns(2)
        with col1:
            strasse = st.text_input("Straße")
        with col2:
            hausnummer = st.text_input("Hausnummer")
        col3, col4, col5 = st.columns(3)
        with col3:
            plz = st.text_input("PLZ")
        with col4:
            ort = st.text_input("Ort")
        with col5:
            land = st.text_input("Land")


    anmerkung = st.text_input("Anmerkungen")
    status_options = ["in Bearbeitung", "abgeschlossen", "in Planung"]
    status = st.selectbox("Status", status_options)
    dokumente = st.file_uploader("Dateien Hinzufügen", accept_multiple_files=True)
    if st.form_submit_button("Baustelle hinzufügen"):
        if name != "":
            if start > ende:
                st.error("Endzeitpunkt kann nicht vor dem Start sein!")
            else:
                try:
                    s = db.session
                    q = "(NULL,'"+name+"','"+str(start)+"','"+str(ende)+"','"+status+"','"+anmerkung+"')"
                    s.execute(text(
                         "INSERT INTO baustellen(id, name, start, ende, status, beschreibung) VALUES"+q))
                    s.commit()
                    s.close()
                    st.success("Baustelle hinzugefügt")
                except Exception as e:
                    st.error(e)
        else:
            st.error("Name darf nicht leer sein!")
