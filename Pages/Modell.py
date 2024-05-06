import traceback
import streamlit as st
from sqlalchemy import text
from Dashboard import showSidebar
showSidebar()

db = st.connection('mysql', type='sql')
typen = db.query("SELECT fahrzeug_typ, id FROM fahrzeugtypen")
marken = db.query("SELECT marke, id FROM marken")


st.title("Neues Modell hinzufügen")
with st.form("Neues Modell", clear_on_submit=True):
    typ = st.selectbox("Fahrzeugtyp", typen, index=None)

    col1, col2 = st.columns([1, 2])
    with col1:
        marke = st.selectbox("Marke", marken["marke"], index=None)
    with col2:
        name = st.text_input("Name")
    gewicht = st.number_input("Gewicht in Kg", value=0)
    elektrisch = st.checkbox("Elektrisch")
    beschreibung = st.text_area("Beschreibung")
    if st.form_submit_button("Modell hinzufügen"):
        if name != "":
            try:
                if marke != "":
                    if marke + " " not in name:
                        name = marke + " " + name
                s = db.session
                typ_id = db.query("SELECT id FROM fahrzeugtypen WHERE fahrzeug_typ ='" + str(typ) + "'", ttl=0)["id"][0]
                query = text(
                    "INSERT INTO fahrzeugmodelle(typ_id, fahrzeug_modell, gewicht, beschreibung, elektrisch) VALUES ("
                    ":typ_id, :name, :gewicht, :beschreibung, :elektrisch)")
                s.execute(query, {"typ_id": typ_id, "name": name, "gewicht": gewicht, "beschreibung": beschreibung,
                                  "elektrisch": elektrisch})
                s.commit()
                s.close()
                st.success("Modell hinzugefügt")
            except Exception as e:
                st.error(traceback.format_exc())
        else:
            st.error("Fehlerhafte eingabe!")
