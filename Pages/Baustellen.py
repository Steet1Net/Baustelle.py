import pandas
import streamlit as st
from sqlalchemy import text

from Dashboard import db, show_sidebar

st.set_page_config(
        page_icon="🚧",
        layout="wide"
    )
show_sidebar()


def create_link(name):
    return f"Baustelle_Anzeigen?name={name.replace(' ', '%20').replace('&', '%26')}"


def bekomme_verfügbare_fahrzeuge(db, von, bis):
    query = f"""
    SELECT id, name
    FROM fahrzeuge
    WHERE id NOT IN (
        SELECT fahrzeug_id
        FROM fahrzeuge_baustellen
        WHERE (start <= '{bis}' AND ende >= '{von}')
    )
    """
    data = db.query(query)
    return pandas.DataFrame(data=data)


def fahrzeuge_zuweisen(db, baustelle_id, vehicle_ids, von, bis):
    query = text("INSERT INTO fahrzeuge_baustellen (baustelle_id, start, ende, fahrzeug_id) VALUES (:baustelle_id, "
                 ":start, :ende, :fahrzeug_id)")

    session = db.session
    for vehicle_id in vehicle_ids:
        session.execute(query, {"baustelle_id": baustelle_id, "start": von, "ende": bis, "fahrzeug_id": vehicle_id})
        session.commit()
    session.close()


st.title("Baustellenübersicht")
data = db.query("SELECT id, name, start, ende, status, Beschreibung FROM baustellen", ttl=0)
a = pandas.DataFrame(data=data)
a.columns = ["ID", "Name", "Start", "Ende", "Status", "Anmerkungen"]
a.insert(1, "Anzeigen", "")

a["Anzeigen"] = a["Name"].apply(create_link)

status = st.popover("Status")
inBearbeitung = status.checkbox("In Bearbeitung", value=True)
abgeschlossen = status.checkbox("Abgeschlossen", value=True)
inPlanung = status.checkbox("In Planung", value=True)
aa = a[0:0]
if inBearbeitung:
    aa = pandas.concat([aa, a.query("Status == 'in Bearbeitung'")])
if abgeschlossen:
    aa = pandas.concat([aa, a.query("Status == 'abgeschlossen'")])
if inPlanung:
    aa = pandas.concat([aa, a.query("Status == 'in Planung'")])
d = st.dataframe(aa,
                 column_config={
                     "Start": st.column_config.DateColumn(),
                     "Anzeigen": st.column_config.LinkColumn(
                         display_text="Anzeigen"
                     )
                 }, height=400, width=950)
st.divider()
selMode = st.selectbox("Modus", ["Anzeigen", "Bearbeiten"])
if selMode == "Bearbeiten":
    st.header("Fahrzeuge zuweisen")
    selBaustelle = st.selectbox("Baustelle", a["Name"], index=None)

    if selBaustelle is not None:
        col1, col2 = st.columns(2)
        with col1:
            von = st.date_input("Von:", value=None)
        with col2:
            bis = st.date_input("Bis:", value=None)

        baustellen_id = a[a['Name'] == selBaustelle]['ID'].values[0]

        if von is not None and bis is not None:
            st.divider()
            fahrzeuge = bekomme_verfügbare_fahrzeuge(db, von, bis)
            selected_vehicles = st.multiselect("Fahrzeuge", fahrzeuge["name"])
            button = st.button("Zuweisen")
            if button:
                try:
                    selected_vehicle_ids = fahrzeuge[fahrzeuge['name'].isin(selected_vehicles)]['id'].tolist()
                    fahrzeuge_zuweisen(db, baustellen_id, selected_vehicle_ids, von, bis)
                    st.success("Fahrzeuge zugewiesen")
                except Exception as e:
                    st.error(e)
elif selMode == "Anzeigen":
    st.write("Anzeigen")
