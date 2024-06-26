import pandas
import streamlit as st
from Dashboard import db, show_sidebar
import urllib.parse

st.set_page_config(
        page_icon="🚧",
        layout="wide",
        page_title="Fahrzeugübersicht"
    )

show_sidebar()

st.title("Fahrzeugübersicht")
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
    return f"Fahrzeug_Anzeigen?name={urllib.parse.quote(name)}"


col1, col2 = st.columns([1, 3])
with col1:
    suche = st.text_input("Suche", placeholder="🔍Suche nach Fahrzeug", help="Suche nach Name, Modell, Typ, Baujahr "
                                                                            "oder Datum")
if suche != "":
    suche = suche.lower()
    a = a[a.apply(lambda row: row.astype(str).str.lower().str.contains(suche).any(), axis=1)]


a["Anzeigen"] = a["Name"].apply(create_link)

st.dataframe(a, width=5000, height=400,
             column_config={"Anzeigen": st.column_config.LinkColumn(
                 display_text="Anzeigen"
             ),
                 "Baujahr": st.column_config.TextColumn()
             })
