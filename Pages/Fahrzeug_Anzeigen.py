import streamlit as st
from sqlalchemy import text
from Dashboard import showSidebar
from streamlit_timeline import st_timeline
showSidebar()
db = st.connection('mysql', type='sql')
fahrzeug_id = db.query(f"SELECT id AS id FROM fahrzeuge WHERE name = '{st.query_params['name']}'", ttl=0)["id"][0]

st.title("Fahrzeuge zuweisen")


name = st.text_input("Name des Fahrzeugs", st.query_params["name"])

a = db.query(f"SELECT * FROM fahrzeuge_baustellen WHERE fahrzeug_id = {fahrzeug_id}", ttl=0)
#st.write(a)
groups = [{
    "id": 0,
    "content": "Wartung"},
    {"id": 1,
     "content": "Einsatz"}
]

timeline_data = []
if not a.empty:
    for index, row in a.iterrows():
        q = f"SELECT Name FROM baustellen WHERE id = {row['baustellen_id']}"
        baustelle = db.query(q, ttl=0)["Name"][0]
        timeline_data.append({"id": index, "group": 1, "content": baustelle, "start": str(row["start"]), "end": str(row["ende"])})
    st_timeline(timeline_data, groups=groups, options={}, height="350px")
