import streamlit as st
from sqlalchemy import text

from Dashboard import db
import pandas as pd
from streamlit_timeline import st_timeline
from geopy import Nominatim

st.set_page_config(
    page_icon="🚧",
    layout="wide"
)
name = st.query_params["name"]

st.page_link("pages/Baustellen.py", label="Baustellen", icon="⬅️")
st.title(name)

baustelle_id = db.query(f"SELECT id as id FROM baustellen WHERE Name = '{name}'", ttl=0)["id"][0]
data = db.query(f"SELECT start, ende, status, adresse_id, bild FROM baustellen WHERE id = {baustelle_id}", ttl=0)
zuweisungen = db.query(f"SELECT fahrzeuge_baustellen.baustelle_id, fahrzeuge.name, fahrzeuge_baustellen.start, "
                       f"fahrzeuge_baustellen.ende FROM fahrzeuge_baustellen JOIN "
                       f"fahrzeuge ON fahrzeuge.id = fahrzeuge_baustellen.fahrzeug_id WHERE baustelle_id = "
                       f"{baustelle_id}", ttl=0)
adresse = db.query(f"SELECT strasse, hausnummer, plz, ort, land FROM adressen WHERE id = {data['adresse_id'][0]}",
                   ttl=0)

st.subheader("Zugewiesene Fahrzeuge")
timeline_data = []
tab1, tab2, tab3, tab4 = st.tabs(["Übersicht", "Adresse", "Zuweisungen", "Dokumente"])
if data["status"][0] == "in Planung":
    status_index = 0
elif data["status"][0] == "in Bearbeitung":
    status_index = 1
elif data["status"][0] == "abgeschlossen":
    status_index = 2
with tab1:  # Übersicht
    col0, col00, col000 = st.columns(3)
    with col0:
        name = st.text_input("Name", value=name)
        start = st.date_input("Startdatum", value=data["start"][0])
    with col00:
        status = st.selectbox("Status", ["in Planung", "in Bearbeitung", "abgeschlossen"], index=status_index)
        ende = st.date_input("Enddatum", value=data["ende"][0])
    with col000:
        if data["bild"][0] is not None:
            bild = data["bild"][0]
            st.image(bild)
        else:
            bild = st.file_uploader("Bild Hinzufügen", accept_multiple_files=False, type=["png", "jpg", "jpeg", "webp",
                                                                                          "jfif"])
            query = text("UPDATE baustellen SET bild = :bild WHERE id = :id")
            if bild is not None:
                session = db.session
                session.execute(query, {"bild": bild.read(), "id": baustelle_id})
                session.commit()
                session.close()
                st.rerun()
with tab2:  # Adresse
    col1, col2 = st.columns(2)
    with col1:
        col3, col4 = st.columns(2)
        with col3:
            strasse = st.text_input("Straße", value=adresse["strasse"][0])
            plz = st.text_input("PLZ", value=adresse["plz"][0])
            land = st.text_input("Land", value=adresse["land"][0])
        with col4:
            hausnummer = st.text_input("Hausnummer", value=adresse["hausnummer"][0])
            ort = st.text_input("Ort", value=adresse["ort"][0])
            st.caption('<div style="height: 29px;"></div>', unsafe_allow_html=True)
            aktualisieren = st.button("Aktualisieren")
            if aktualisieren:
                session = db.session
                query = text("UPDATE adressen SET strasse = :strasse, hausnummer = :hausnummer, plz = :plz, ort = :ort,"
                             " land = :land WHERE adresse_id = :id")
                session.execute(query, {"strasse": strasse, "hausnummer": hausnummer, "plz": plz, "ort": ort, "land":
                    land, "id": baustelle_id})
                session.commit()
                session.close()
                st.success("Adresse aktualisiert")
    with col2:
        with st.spinner("Lade Karte..."):
            geolocator = Nominatim(user_agent="baustelle.steet.net")
            location = geolocator.geocode(f"{strasse} {hausnummer}, {plz} {ort}, {land}")
            a = [{'lat': location.latitude, 'lon': location.longitude}]
            st.map(a, zoom=13, use_container_width=False)
            st.link_button("Auf Google Maps anzeigen", f"https://www.google.com/maps/search/?api=1&query="
                                                       f"{location.latitude},{location.longitude}",
                           use_container_width=True)
with tab3:  # Zuweisungen
    if not zuweisungen.empty:
        for index, row in zuweisungen.iterrows():
            with tab1:
                timeline_data.append({"id": index, "group": 1, "content": row["name"], "start": str(row["start"]),
                                      "end": str(row["ende"])})
        #with st.container(height=400):
        h = 80 + len(zuweisungen) * 40
        options = {
            "width": "100%",
            "align": "center",
            "orientation.axis": "top",
            "clickToUse": "true",
        }
        st_timeline(timeline_data, options={}, height=h)
    else:
        st.caption("_Keine Fahrzeuge zugewiesen_")
with tab4:  # Dokumente
    with st.spinner("Lade Dokumente..."):
        dokumente = db.query(f"SELECT dokument FROM baustellendokumente WHERE baustelle_id = {baustelle_id}", ttl=0)
        if dokumente.empty:
            st.caption("_Keine Dokumente vorhanden_")
        else:
            pass
