import streamlit as st
from Dashboard import db
from streamlit_timeline import st_timeline

#db = st.connection('mysql', type='sql')
fahrzeug = db.query(f"SELECT id, name, bild, beschreibung FROM fahrzeuge WHERE name = '{st.query_params['name']}'", ttl=0)
fahrzeug_id = fahrzeug["id"][0]

st.title("Fahrzeug Anzeigen/Bearbeiten")


name = st.text_input("Name des Fahrzeugs", st.query_params["name"])

zuweisungen = db.query(f"SELECT baustellen.name, fahrzeuge_baustellen.fahrzeug_id, fahrzeuge_baustellen.start, "
                       f"fahrzeuge_baustellen.ende FROM fahrzeuge_baustellen JOIN "
                       f"baustellen ON baustellen.id = fahrzeuge_baustellen.fahrzeug_id WHERE fahrzeug_id = "
                       f"{fahrzeug_id}", ttl=0)

#st.write(a)
with st.sidebar:
    st.title(fahrzeug["name"][0])
    st.caption(fahrzeug["beschreibung"][0])
    if fahrzeug["bild"][0] is not None:
        st.divider()
        st.image(fahrzeug["bild"][0])


groups = [{
    "id": 0,
    "content": "Wartung"},
    {"id": 1,
     "content": "Einsatz"}
]

timeline_data = []
if not zuweisungen.empty:
    for index, row in zuweisungen.iterrows():
        timeline_data.append({"id": index, "group": 1, "content": row["name"], "start": str(row["start"]), "end": str(row["ende"])})
    st_timeline(timeline_data, groups=groups, options={}, height="350px")
