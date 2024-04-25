import time

import pandas
import streamlit as st
from sqlalchemy import text

db = st.connection('mysql', type='sql')

def get_available_vehicles(db, von, bis):
    # SQL query to get available vehicles
    query = f"""
    SELECT id, name
    FROM fahrzeuge
    WHERE id NOT IN (
        SELECT fahrzeug_id
        FROM fahrzeuge_baustellen
        WHERE (start <= '{bis}' AND ende >= '{von}')
    )
    """
    # Execute the query
    data = db.query(query)
    return pandas.DataFrame(data=data)

def assign_vehicles_to_baustelle(db, baustelle_id, vehicle_ids, von, bis):
    # SQL query to assign vehicles to a baustelle
    query = """
    INSERT INTO fahrzeuge_baustellen (baustellen_id, start, ende, fahrzeug_id)
    VALUES (:baustelle_id, :start, :ende, :fahrzeug_id)
    """
    s = db.session
    # Execute the query for each vehicle
    for vehicle_id in vehicle_ids:
        s.execute(text(query), {"baustelle_id": baustelle_id, "start": von, "ende": bis, "fahrzeug_id": vehicle_id})
        s.commit()
    s.close()



st.title("Baustellenübersicht")
# st.write("Dummy-Daten werden angezeigt.")
# Modify the query to also select the id
data = db.query("SELECT id, name, start, ende, status, Beschreibung FROM baustellen", ttl=0)
a = pandas.DataFrame(data=data)
a.columns = ["ID", "Name", "Start", "Ende", "Status", "Beschreibung"]
d = st.dataframe(a,
                 column_config={
                     "Start": st.column_config.DateColumn(),
                 }, height=400, width=950)
st.divider()
selMode = st.selectbox("Modus", ["Anzeigen", "Bearbeiten"])
if selMode == "Bearbeiten":
    st.header("Fahrzeuge zuweisen")
    selBaustelle = st.selectbox("Baustelle", a["Name"], index=None)

    if selBaustelle != None:
        col1, col2 = st.columns(2)
        with col1:
            von = st.date_input("Von:", value=None)
        with col2:
            bis = st.date_input("Bis:", value=None)

        baustellen_id = a[a['Name'] == selBaustelle]['ID'].values[0]

        if von != None and bis != None:
            st.divider()
            vehcls = get_available_vehicles(db, von, bis)
            selected_vehicles = st.multiselect("Fahrzeuge", vehcls["name"])
            button = st.button("Zuweisen")
            if button:
                # Get the IDs of the selected vehicles
                try:
                    selected_vehicle_ids = vehcls[vehcls['name'].isin(selected_vehicles)]['id'].tolist()
                    assign_vehicles_to_baustelle(db, baustellen_id, selected_vehicle_ids, von, bis)
                    st.success("Fahrzeuge zugewiesen")
                except Exception as e:
                    st.error(e)
elif selMode == "Anzeigen":
    st.write("Anzeigen")
