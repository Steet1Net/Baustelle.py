import pandas
import streamlit as st
import traceback
from Dashboard import db, show_sidebar
import urllib.parse

st.set_page_config(
        page_icon="🚧",
        layout="wide"
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
    # return f"http://localhost:8501/Fahrzeug_Anzeigen/?name={name.replace(' ', '%20')}"
    return f"Fahrzeug_Anzeigen?name={urllib.parse.quote(name)}"


def filter_baujahr(a):
    return a.query("Baujahr >= @baujahr_filter[0] and Baujahr <= @baujahr_filter[1]")


def baujahr_int(jahr):
    return int(jahr)


a["Baujahr"] = a["Baujahr"].apply(baujahr_int)
shit = '''Filter

def filter_modell(a):
    if modell_filter.__len__() > 0:
        return a.query("Modell in @modell_filter")
    else:
        return a


def filter_fahrzeugtyp(a):
    if fahrzeugtyp_filter.__len__() > 0:
        return a.query("Fahrzeugtyp in @fahrzeugtyp_filter")
    else:
        return a





min_baujahr = int(a["Baujahr"].min())
max_baujahr = int(a["Baujahr"].max())
fahrzeugtyp_filter = a["Fahrzeugtyp"].unique()
modell_filter = a["Modell"].unique()


baujahr_filter = [min_baujahr, max_baujahr]

col1, col2 = st.columns(2)
a = filter_fahrzeugtyp(a)
a = filter_modell(a)
a = filter_baujahr(a)

with col1.popover("Filter", use_container_width=True):
    tab1, tab2 = st.tabs(["Fahrzeugmodell", "Fahrzeugtyp"])
    with tab1:
        modell_filter = st.multiselect("Modell", a["Modell"].unique())
        if modell_filter.__len__() > 0:
            a = a.query("Modell in @modell_filter")
    with tab2:
        fahrzeugtyp_filter = st.multiselect("Fahrzeugtyp", a["Fahrzeugtyp"].unique())
        if fahrzeugtyp_filter.__len__() > 0:
            a = a.query("Fahrzeugtyp in @fahrzeugtyp_filter")

with col2.popover("Baujahr", use_container_width=True):
    min_baujahr = int(a["Baujahr"].min())
    max_baujahr = int(a["Baujahr"].max())
    if min_baujahr != max_baujahr:
        baujahr_filter = st.slider("Baujahr", min_baujahr, max_baujahr, (min_baujahr, max_baujahr))
    a = a.query("Baujahr >= @baujahr_filter[0] and Baujahr <= @baujahr_filter[1]")
'''

with st.popover("Baujahr"):
    baujahr_min = int(a["Baujahr"].min())
    baujahr_max = int(a["Baujahr"].max())
    baujahr_filter = st.slider("Baujahr", baujahr_min, baujahr_max, (baujahr_min, baujahr_max))
    filter_baujahr(a)


a["Anzeigen"] = a["Name"].apply(create_link)

st.dataframe(a, width=1000, height=400,
             column_config={"Anzeigen": st.column_config.LinkColumn(
                 display_text="Anzeigen"
             ),
                 "Baujahr": st.column_config.TextColumn()
             })
