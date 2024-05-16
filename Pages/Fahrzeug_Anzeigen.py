from datetime import datetime

import streamlit as st
from sqlalchemy import text

from Dashboard import db
from streamlit_timeline import st_timeline

st.set_page_config(
    page_icon="🚧",
    layout="wide",
    page_title=st.query_params["name"]
)
session = db.session
fahrzeug = db.query(f"SELECT * FROM fahrzeuge WHERE name = '{st.query_params['name']}'",
                    ttl=0)
fahrzeug_id = fahrzeug["id"][0]
st.page_link("pages/Fahrzeuge.py", label="Fahrzeuge", icon="⬅️")

st.title(fahrzeug["name"][0])
modell = db.query(f"SELECT fahrzeug_modell, elektrisch FROM fahrzeugmodelle WHERE id = {fahrzeug['modell_id'][0]}", ttl=0)
zuweisungen = db.query(f"SELECT baustellen.name, fahrzeuge_baustellen.fahrzeug_id, fahrzeuge_baustellen.start, "
                       f"fahrzeuge_baustellen.ende FROM fahrzeuge_baustellen JOIN "
                       f"baustellen ON baustellen.id = fahrzeuge_baustellen.fahrzeug_id WHERE fahrzeug_id = "
                       f"{fahrzeug_id}", ttl=0)
st.caption(modell["fahrzeug_modell"][0])
tab1, tab2, tab3 = st.tabs(["Übersicht", "Zuweisungen", "Dokumente"])
with tab1:  # Übersicht
    col1, col2 = st.columns([2, 1])
    with col1:
        col3, col4 = st.columns(2)
        with col3:
            name = st.text_input("Name des Fahrzeugs", fahrzeug["name"][0])
            st.checkbox("Elektrisch", value=modell["elektrisch"][0], disabled=True)
        with col4:
            kaufdatum = st.date_input("Kaufdatum", value=fahrzeug["kaufdatum"][0])
            baujahr = st.number_input("Baujahr", value=int(fahrzeug["baujahr_jahr"][0]))
        beschreibung = st.text_area("Beschreibung / Anmerkungen", fahrzeug["beschreibung"][0])
        if st.button("Aktualisieren"):
            try:
                jahr = datetime.strptime(str(baujahr), '%Y')
                query = text("UPDATE fahrzeuge SET name = :name, kaufdatum = :kaufdatum, baujahr = :baujahr, "
                             "beschreibung = :beschreibung WHERE id = :id")
                session.execute(query, {"name": name, "kaufdatum": kaufdatum, "baujahr": str(jahr.strftime('%Y-%m-%d')),
                                        "beschreibung": beschreibung, "id": fahrzeug_id})
                session.commit()
                st.success("Fahrzeug erfolgreich aktualisiert")
            except Exception as e:
                st.error(e)
    with col2:
        if fahrzeug["bild"][0] is not None:
            st.image(fahrzeug["bild"][0])
        else:
            bild = st.file_uploader("Bild Hinzufügen", type=["png", "jpg", "jpeg", "webp", "jfif"])
            query = text("UPDATE fahrzeuge SET bild = :bild WHERE id = :id")
            if bild is not None:
                session.execute(query, {"bild": bild.read(), "id": fahrzeug_id})
                session.commit()
                st.success("Bild erfolgreich hinzugefügt")
                st.rerun()

with tab2:  # Zuweisungen
    groups = [{
        "id": 0,
        "content": "Einsatz"},
        {"id": 1,
         "content": "Wartung"}
    ]

    timeline_data = []
    if not zuweisungen.empty:
        for index, row in zuweisungen.iterrows():
            timeline_data.append(
                {"id": index, "group": 0, "content": row["name"], "start": str(row["start"]), "end": str(row["ende"])})
        st_timeline(timeline_data, groups=groups, options={}, height="250px")
    else:
        st.caption("*Keine Zuweisungen vorhanden*")

with tab3:  # Dokumente
    col1, col2 = st.columns([2, 1])
    with col1:
        with st.spinner("Lade Dokumente..."):
            dokumente = db.query(f"SELECT * FROM fahrzeugdokumente WHERE fahrzeug_id = {fahrzeug_id}", ttl=0)
            dokumente = dokumente.sort_values(by="dateiname", ascending=True)
            if dokumente.empty:
                st.caption("*Keine Dokumente vorhanden*")
            else:
                for index, row in dokumente.iterrows():
                    st.download_button(label=str(row["dateiname"]), data=row["dokument"], file_name=row["dateiname"],
                                       use_container_width=True, key=f"d_{index}")
    with col2:
        with st.form("Dokumente Hochladen", clear_on_submit=True, border=False):
            dokumente = st.file_uploader("Dokument hinzufügen", accept_multiple_files=True, key="d_upload")
            if st.form_submit_button("Hochladen"):
                query = text("INSERT INTO fahrzeugdokumente (fahrzeug_id, dateiname, dokument) VALUES (:fahrzeug_id, "
                             ":dateiname, :dokument)")
                for d in dokumente:
                    session.execute(query, {"fahrzeug_id": fahrzeug_id, "dateiname": d.name, "dokument": d.read()})
                session.commit()
                st.rerun()
session.close()
