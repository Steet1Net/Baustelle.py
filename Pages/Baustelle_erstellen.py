import traceback
import streamlit as st
from sqlalchemy import text
from Dashboard import db, show_sidebar

st.set_page_config(
        page_icon="🚧",
        layout="wide"
    )
show_sidebar()


def dokumenteHochladen(session, dokumente, baustellen_id):
    try:
        for doc in dokumente:
            data = doc.read()
            session.execute(text("INSERT INTO baustellendokumente(baustellen_id, dokument, dateiname) VALUES("
                                 ":baustellen_id, :dokument, :dateiname)"),
                            {"baustellen_id": baustellen_id, "dokument": data, "dateiname": str(doc.name)})
            session.commit()
    except Exception as e:
        st.error(e)
        st.error(traceback.format_exc())


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
    dokumente = st.file_uploader("Dateien Hinzufügen", accept_multiple_files=True, help="z.B. Pläne, Bilder, CAD-Dateien...")
    if st.form_submit_button("Baustelle hinzufügen"):
        if name != "":
            if start > ende:
                st.error("Endzeitpunkt kann nicht vor dem Start sein!")
            else:
                try:
                    session = db.session

                    query = text("INSERT INTO adressen(id, strasse, hausnummer, plz, ort, land) VALUES (NULL, "
                                 ":strasse, :hausnummer, :plz, :ort, :land)")
                    session.execute(query,
                                    {"strasse": strasse, "hausnummer": hausnummer, "plz": plz, "ort": ort,
                                     "land": land})
                    session.commit()

                    adresse_id = db.query("SELECT MAX(id) AS id FROM adressen", ttl=0)["id"][0]
                    query = text("INSERT INTO baustellen(id, name, start, ende, status, beschreibung, adresse_id) "
                                 "VALUES (NULL, :name, :start, :ende, :status, :beschreibung, :adresse_id)")
                    session.execute(query, {"name": name, "start": str(start), "ende": str(ende), "status": status,
                                            "beschreibung": anmerkung, "adresse_id": adresse_id})
                    session.commit()

                    anzahl = dokumente.__len__()
                    if anzahl > 0:
                        Text = "Dokumente werden hochgeladen"
                        if anzahl == 1:
                            Text = "Dokument wird hochgeladen"
                        baustellen_id = db.query("SELECT MAX(id) AS id FROM baustellen", ttl=0)["id"][0]
                        with st.spinner(Text):
                            dokumenteHochladen(session, dokumente, baustellen_id)
                    session.commit()

                    session.close()
                    st.success("Baustelle hinzugefügt")
                except Exception as e:
                    st.error(traceback.format_exc())
        else:
            st.error("Name darf nicht leer sein!")
