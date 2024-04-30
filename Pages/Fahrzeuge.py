import pandas
import streamlit as st
import traceback
from Dashboard import showSidebar

showSidebar()

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
a.insert(0, "Anzeigen", "")


def create_link(name):
    return f"http://localhost:8501/Fahrzeug_Anzeigen/?name={name.replace(' ', '%20')}"


a["Anzeigen"] = a["Name"].apply(create_link)
# st.write(str(f"[{name}](http://localhost:8501/edit/?name={name.replace(' ', '%20')})"))

st.dataframe(a, width=1000, height=400,
             column_config={"Anzeigen": st.column_config.LinkColumn(
                 display_text='Anzeigen',
                 width=1,
             )})
