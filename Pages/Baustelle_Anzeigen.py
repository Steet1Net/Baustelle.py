import streamlit as st
from Dashboard import db
from streamlit_timeline import st_timeline

name = st.query_params["name"]
st.title(name)

baustelle_id = db.query(f"SELECT id as id FROM baustellen WHERE Name = '{name}'", ttl=0)["id"][0]
zuweisungen = db.query(f"SELECT fahrzeuge_baustellen.baustelle_id, fahrzeuge.name, fahrzeuge_baustellen.start, "
                       f"fahrzeuge_baustellen.ende FROM fahrzeuge_baustellen JOIN "
                       f"fahrzeuge ON fahrzeuge.id = fahrzeuge_baustellen.fahrzeug_id WHERE baustelle_id = "
                       f"{baustelle_id}", ttl=0)


st.header("Zugewiesene Fahrzeuge")

timeline_data = []
if not zuweisungen.empty:
    for index, row in zuweisungen.iterrows():
        timeline_data.append({"id": index, "group": 1, "content": row["name"], "start": str(row["start"]), "end": str(row["ende"])})
    with st.container(height=400):
        h = len(zuweisungen) * 50
        st.write(h)
        options = {
            "width": "100%",
            "height": h,
            "align": "center",
            "orientation.axis": "top",
            "clickToUse": "true",
        }
        st_timeline(timeline_data, options={})
