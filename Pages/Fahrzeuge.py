import pandas
import streamlit as st

db = st.connection('mysql', type='sql')

st.title("Fahrzeugübersicht")
# st.write("Dummy-Daten werden angezeigt.")
data = db.query("""
    SELECT fahrzeuge.name, Fahrzeug_modell, Fahrzeug_typ, baujahr_jahr, kaufdatum 
    FROM fahrzeugmodelle 
    JOIN fahrzeuge ON fahrzeuge.modell_id = fahrzeugmodelle.id 
    JOIN fahrzeugtypen ON fahrzeugmodelle.typ_id = fahrzeugtypen.id
""", ttl=0)
a = pandas.DataFrame(data=data)
a.columns = ["Name", "Modell", "Fahrzeugtyp", "Baujahr", "Kaufdatum"]
st.dataframe(a, height=400, width=950)

st.divider()

