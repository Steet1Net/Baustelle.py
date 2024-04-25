from datetime import datetime
import traceback

import streamlit as st
from sqlalchemy import text

db = st.connection('mysql', type='sql')
typen = db.query("SELECT fahrzeug_typ FROM fahrzeugtypen")
modelle = db.query("SELECT fahrzeug_modell, beschreibung, fahrzeugtypen.Fahrzeug_typ FROM fahrzeugmodelle JOIN "
                   "fahrzeugtypen ON fahrzeugmodelle.typ_id = fahrzeugtypen.id", ttl=0)

st.title("Neues Fahrzeug hinzufügen")
name = st.text_input("Name")
baujahr = st.number_input("Baujahr", value=2000)
kaufdatum = st.date_input("Kaufdatum")
col1, col2 = st.columns(2)
with col1:
    typ = st.selectbox("Typ", typen)
with col2:
    fahrzeugmodell = st.selectbox("Modell", modelle.query('Fahrzeug_typ == ' + "'" + typ + "'"))
st.caption(str(db.query("SELECT beschreibung FROM fahrzeugmodelle WHERE fahrzeug_modell ='" + str(fahrzeugmodell)+"'")["beschreibung"][0]))
beschreibung = st.text_input("Anmerkung:")
if st.button("Fahrzeug hinzufügen"):
    if name != "":
        try:
            s = db.session
            a = datetime.strptime(str(baujahr), '%Y')
            typ_id = db.query("SELECT id FROM fahrzeugmodelle WHERE fahrzeug_modell ='" + str(fahrzeugmodell) + "'", ttl=0)["id"][0]
            print(typ_id)
            q = "('" + str(a.strftime('%Y-%m-%d')) + "','" + str(kaufdatum) + "'," + str(typ_id) + ",'" + name + "','" + beschreibung + "')"
            s.execute(text(
                f"INSERT INTO fahrzeuge(baujahr, kaufdatum, modell_id, name, beschreibung) VALUES" + q))
            s.commit()
            s.close()
            st.success("Fahrzeug hinzugefügt")
        except Exception as e:
            st.error(traceback.format_exc())
    else:
        st.error("Marke darf nicht leer sein!")
