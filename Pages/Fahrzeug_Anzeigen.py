import streamlit as st
from sqlalchemy import text

from Dashboard import db
from streamlit_timeline import st_timeline

st.set_page_config(
        page_icon="🚧",
        layout="wide"
    )
fahrzeug = db.query(f"SELECT id, name, bild, beschreibung FROM fahrzeuge WHERE name = '{st.query_params['name']}'", ttl=0)
fahrzeug_id = fahrzeug["id"][0]

st.title("Fahrzeug Anzeigen/Bearbeiten")


name = st.text_input("Name des Fahrzeugs", st.query_params["name"])

zuweisungen = db.query(f"SELECT baustellen.name, fahrzeuge_baustellen.fahrzeug_id, fahrzeuge_baustellen.start, "
                       f"fahrzeuge_baustellen.ende FROM fahrzeuge_baustellen JOIN "
                       f"baustellen ON baustellen.id = fahrzeuge_baustellen.fahrzeug_id WHERE fahrzeug_id = "
                       f"{fahrzeug_id}", ttl=0)

with st.sidebar:
    st.page_link("pages/Fahrzeuge.py", label="Fahrzeuge", icon="⬅️")
    st.title(fahrzeug["name"][0])
    st.caption(fahrzeug["beschreibung"][0])
    if fahrzeug["bild"][0] is not None:
        st.divider()
        st.image(fahrzeug["bild"][0])
    else:
        bild = st.file_uploader("Bild Hinzufügen", type=["png", "jpg", "jpeg", "webp", "jfif"])
        query = text("UPDATE fahrzeuge SET bild = :bild WHERE id = :id")
        if bild is not None:
            session = db.session
            session.execute(query, {"bild": bild.read(), "id": fahrzeug_id})
            session.commit()
            session.close()
            st.success("Bild erfolgreich hinzugefügt")
            st.rerun()
tab1, tab2 = st.tabs(["Zuweisungen", "Infos"])

with tab1:
    groups = [{
        "id": 0,
        "content": "Einsatz"},
        {"id": 1,
         "content": "Wartung"}
    ]

    timeline_data = []
    if not zuweisungen.empty:
        for index, row in zuweisungen.iterrows():
            timeline_data.append({"id": index, "group": 0, "content": row["name"], "start": str(row["start"]), "end": str(row["ende"])})
        st_timeline(timeline_data, groups=groups, options={}, height="250px")
