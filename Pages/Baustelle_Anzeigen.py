import streamlit as st
from sqlalchemy import text
from countries import get_countries
from Dashboard import db, status
from streamlit_timeline import st_timeline
from geopy import Nominatim

name = st.query_params["name"]
st.set_page_config(
    page_icon="🚧",
    layout="wide",
    page_title=name
)

session = db.session
st.page_link("pages/Baustellen.py", label="Baustellen", icon="⬅️")
st.title(name)

baustelle_id = db.query(f"SELECT id as id FROM baustellen WHERE Name = '{name}'", ttl=0)["id"][0]
baustelle = db.query(f"SELECT start, ende, status, adresse_id, bild, beschreibung FROM baustellen WHERE id = {baustelle_id}", ttl=0)
zuweisungen = db.query(f"SELECT fahrzeuge_baustellen.baustelle_id, fahrzeuge.name, fahrzeuge_baustellen.start, "
                       f"fahrzeuge_baustellen.ende FROM fahrzeuge_baustellen JOIN "
                       f"fahrzeuge ON fahrzeuge.id = fahrzeuge_baustellen.fahrzeug_id WHERE baustelle_id = "
                       f"{baustelle_id}", ttl=0)
adresse = db.query(f"SELECT strasse, hausnummer, plz, ort, land FROM adressen WHERE id = {baustelle['adresse_id'][0]}",
                   ttl=0)

timeline_data = []
tab1, tab2, tab3, tab4 = st.tabs(["Übersicht", "Adresse", "Zuweisungen", "Dokumente"])
if baustelle["status"][0] == "in Planung":
    status_index = 0
elif baustelle["status"][0] == "in Bearbeitung":
    status_index = 1
elif baustelle["status"][0] == "abgeschlossen":
    status_index = 2
with tab1:  # Übersicht
    col0, col00 = st.columns([2, 1])
    with col0:
        col10, col11 = st.columns(2)
        with col10:
            name = st.text_input("Name", value=name)
            start = st.date_input("Startdatum", value=baustelle["start"][0])
        with col11:
            status = st.selectbox("Status", status, index=status_index)
            ende = st.date_input("Enddatum", value=baustelle["ende"][0])
        beschreibung = st.text_area("Beschreibung / Anmerkungen", baustelle["beschreibung"][0])
        if st.button("Aktualisieren", key="übersicht_aktualisieren"):
            try:
                query = text("UPDATE baustellen SET name = :name, start = :start, ende = :ende, status = :status, "
                             "beschreibung = :beschreibung WHERE id = :id")
                session.execute(query, {"name": name, "start": str(start), "ende": str(ende), "status": status,
                                        "beschreibung": beschreibung, "id": baustelle_id})
                session.commit()
                st.success("Aktualisierung war erfolgreich")
            except Exception as e:
                st.error("Aktualisierung fehlgeschlagen: \n" + e)

    with col00:
        if baustelle["bild"][0] is not None:
            bild = baustelle["bild"][0]
            st.image(bild)
        else:
            bild = st.file_uploader("Bild Hinzufügen", accept_multiple_files=False, type=["png", "jpg", "jpeg", "webp",
                                                                                          "jfif"])
            query = text("UPDATE baustellen SET bild = :bild WHERE id = :id")
            if bild is not None:
                session.execute(query, {"bild": bild.read(), "id": baustelle_id})
                session.commit()
                st.rerun()

with tab2:  # Adresse
    col1, col2 = st.columns(2)
    with col1:
        col3, col4 = st.columns(2)
        with col3:
            strasse = st.text_input("Straße", value=adresse["strasse"][0])
            plz = st.text_input("PLZ", value=adresse["plz"][0])
            länder = get_countries()
            land = st.selectbox(label="Land", options=länder, index=länder.index(adresse["land"][0]))
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
                st.success("Adresse aktualisiert")
    with col2:
        try:
            with st.spinner("Lade Karte..."):
                geolocator = Nominatim(user_agent="**insert domain**")
                location = geolocator.geocode(f"{strasse} {hausnummer}, {plz} {ort}, {land}")
                a = [{'lat': location.latitude, 'lon': location.longitude}]
                st.map(a, zoom=14, use_container_width=False)
                st.link_button("Auf Google Maps anzeigen", f"https://www.google.com/maps/search/?api=1&query="
                                                           f"{location.latitude},{location.longitude}",
                               use_container_width=True)
        except:
            st.error("Karte konnte nicht geladen werden")
with tab3:  # Zuweisungen
    if not zuweisungen.empty:
        for index, row in zuweisungen.iterrows():
            with tab1:
                timeline_data.append({"id": index, "group": 1, "content": row["name"], "start": str(row["start"]),
                                      "end": str(row["ende"])})
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

    st.divider()
    st.header("Fahrzeuge zuweisen")

    col22, col33 = st.columns(2)
    with col22:
        start_d = st.date_input("Startdatum", value=None, max_value=ende, min_value=start)
    with col33:
        ende_d = st.date_input("Enddatum", value=None, max_value=ende, min_value=start)
    if start_d is not None and ende_d is not None:
        if not start_d <= ende_d:
            st.error("Wähle einen gültigen Zeitraum aus!")
        else:
            if start_d >= start and ende_d <= ende:
                q = f"""
                    SELECT id, name
                    FROM fahrzeuge
                    WHERE id NOT IN (
                        SELECT fahrzeug_id
                        FROM fahrzeuge_baustellen
                        WHERE (start <= '{ende_d}' AND ende >= '{start_d}')
                    )
                    """
                fahrzeuge = db.query(q, ttl=0)
                if not fahrzeuge.empty:
                    sel_fahrzeuge = st.multiselect("Fahrzeuge", fahrzeuge["name"])
                    if st.button("Zuweisen"):
                        query = text(
                            "INSERT INTO fahrzeuge_baustellen (baustelle_id, start, ende, fahrzeug_id) VALUES (:baustelle_id, "
                            ":start, :ende, :fahrzeug_id)")
                        fahrzeuge_ids = fahrzeuge[fahrzeuge['name'].isin(sel_fahrzeuge)]['id'].tolist()
                        session = db.session
                        for fahrzeuge_id in fahrzeuge_ids:
                            session.execute(query, {"baustelle_id": baustelle_id, "start": start_d, "ende": ende_d,
                                                    "fahrzeug_id": fahrzeuge_id})
                            session.commit()
                        session.close()
                        st.rerun()
                else:
                    st.error("Keine Fahrzeuge verfügbar")
            else:
                st.error("Zeitraum liegt nicht innerhalb der Baustelle!")

with tab4:  # Dokumente
    col1, col2 = st.columns([2, 1])
    with col1:
        with st.spinner("Lade Dokumente..."):
            dokumente = db.query(f"SELECT * FROM baustellendokumente WHERE baustelle_id = {baustelle_id}", ttl=0)
            dokumente = dokumente.sort_values(by="dateiname", ascending=True)
            if dokumente.empty:
                st.caption("_Keine Dokumente vorhanden_")
            else:
                for index, row in dokumente.iterrows():
                    st.download_button(label=str(row["dateiname"]), data=row["dokument"], file_name=row["dateiname"],
                                       use_container_width=True, key=f"d_{index}")
    with col2:
        with st.form("Dokumente Hochladen", clear_on_submit=True, border=False):
            dokumente = st.file_uploader("Dokument hinzufügen", accept_multiple_files=True, key="d_upload")
            if st.form_submit_button("Hochladen"):
                query = text("INSERT INTO baustellendokumente (baustelle_id, dateiname, dokument) VALUES ("
                             ":baustelle_id, :dateiname, :dokument)")
                for d in dokumente:
                    session.execute(query, {"baustelle_id": baustelle_id, "dateiname": d.name, "dokument": d.read()})
                session.commit()
                st.rerun()
session.close()
