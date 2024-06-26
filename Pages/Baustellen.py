import pandas
import streamlit as st
from sqlalchemy import text

from Dashboard import db, show_sidebar

st.set_page_config(
    page_icon="🚧",
    layout="wide",
    page_title="Baustellen"
)
show_sidebar()


def create_link(name):
    return f"Baustelle_Anzeigen?name={name.replace(' ', '%20').replace('&', '%26')}"


st.title("Baustellenübersicht")
data = db.query("SELECT id, name, start, ende, status, Beschreibung FROM baustellen", ttl=0)
a = pandas.DataFrame(data=data)
a.columns = ["ID", "Name", "Start", "Ende", "Status", "Anmerkungen"]
a.insert(1, "Anzeigen", "")

a["Anzeigen"] = a["Name"].apply(create_link)
col1, col2, col3 = st.columns(3)

with col2:
    st.write('<div style="height: 26px;">Status</div>', unsafe_allow_html=True)
    status = st.popover("Status")
    inBearbeitung = status.checkbox("In Bearbeitung", value=True)
    abgeschlossen = status.checkbox("Abgeschlossen", value=True)
    inPlanung = status.checkbox("In Planung", value=True)
    abgebrochen = status.checkbox('abgebrochen', value=True)
    aa = a[0:0]
    if inBearbeitung:
        aa = pandas.concat([aa, a.query("Status == 'in Bearbeitung'")])
    if abgeschlossen:
        aa = pandas.concat([aa, a.query("Status == 'abgeschlossen'")])
    if inPlanung:
        aa = pandas.concat([aa, a.query("Status == 'in Planung'")])
    if abgebrochen:
        aa = pandas.concat([aa, a.query("Status == 'abgebrochen'")])

with col1:
    suche = st.text_input("Suche", placeholder="🔍Suche nach Baustelle", help="Suche nach Name, Modell, Typ, Baujahr "
                                                                             "oder Datum")
    if suche != "":
        suche = suche.lower()
        aa = aa[aa.apply(lambda row: row.astype(str).str.lower().str.contains(suche).any(), axis=1)]
aa.drop("ID", axis=1, inplace=True)
d = st.dataframe(aa,
                 column_config={
                     "Start": st.column_config.DateColumn(),
                     "Anzeigen": st.column_config.LinkColumn(
                         display_text="Anzeigen"
                     )
                 }, height=400, width=5000)

