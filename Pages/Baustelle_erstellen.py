import traceback
import streamlit as st
from geopy import Nominatim
from sqlalchemy import text
from Dashboard import db, show_sidebar, status
from countries import get_countries

st.set_page_config(
    page_icon="🚧",
    layout="wide",
    page_title="Neue Baustelle"
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


def get_lat_long(adresse):
    geolocator = Nominatim(user_agent="baustelle.steet.net")
    location = geolocator.geocode(adresse)
    if location is not None:
        return location.latitude, location.longitude
    else:
        return None


st.title("Neue Baustelle hinzufügen")
col1, col2 = st.columns([2, 1])
with col2:
    c = st.container(border=True)
    image = c.file_uploader("Bild Hinzufügen", accept_multiple_files=False, type=["png", "jpg", "jpeg", "webp", "jfif"],
                            help="z.B. Lageplan, Baustellenfoto...")
    if image is not None:
        c.image(image)
with col1:
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
                land = st.selectbox("Land", get_countries(), index=None, placeholder="Land auswählen")

        anmerkung = st.text_area("Anmerkung:")
        status_options = status
        status = st.selectbox("Status", status_options)
        dokumente = st.file_uploader("Dateien Hinzufügen", accept_multiple_files=True,
                                     help="z.B. Pläne, Bilder, CAD-Dateien...")
        if st.form_submit_button("Baustelle hinzufügen"):
            if name != "":
                if start > ende:
                    st.error("Endzeitpunkt kann nicht vor dem Start sein!")
                else:
                    try:
                        lat, long = get_lat_long(f"{strasse} {hausnummer}, {plz} {ort}, {land}")

                        if lat is not None or long is not None:
                            session = db.session

                            query = text("INSERT INTO adressen(id, strasse, hausnummer, plz, ort, land, latitude, "
                                         "longitude) VALUES (NULL, :strasse, :hausnummer, :plz, :ort, :land, :latitude,"
                                         " :longitude)")
                            session.execute(query,
                                            {"strasse": strasse, "hausnummer": hausnummer, "plz": plz, "ort": ort,
                                             "land": land, "latitude": lat, "longitude": long})
                            session.commit()

                            adresse_id = db.query("SELECT MAX(id) AS id FROM adressen", ttl=0)["id"][0]

                            query = text("INSERT INTO baustellen(id, name, start, ende, status, beschreibung, "
                                         "adresse_id, bild) VALUES (NULL, :name, :start, :ende, :status, :beschreibung,"
                                         ":adresse_id, :bild)")
                            session.execute(query,
                                            {"name": name, "start": str(start), "ende": str(ende), "status": status,
                                             "beschreibung": anmerkung, "adresse_id": adresse_id, "bild": image})
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

                            st.success("Baustelle hinzugefügt")
                        else:
                            st.error("Adresse ist ungültig!")
                    except Exception as e:
                        st.error(e)
                        st.error(traceback.format_exc())
                        session.rollback()
                        session.close()
            else:
                st.error("Name darf nicht leer sein!")
