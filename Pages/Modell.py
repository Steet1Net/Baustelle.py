import traceback
import streamlit as st
from sqlalchemy import text
from Dashboard import db, show_sidebar

st.set_page_config(
    page_icon="🚧",
    layout="wide",
    page_title="Neues Fahrzeugmodell"
)
show_sidebar()
if st.query_params == {}:
    st.query_params["typ"] = None
    st.query_params["s"] = None


def neues_modell():
    typen = db.query("SELECT fahrzeug_typ, id FROM fahrzeugtypen")

    st.title("Neues Modell hinzufügen")
    with st.form("Neues Modell", clear_on_submit=True):
        if st.query_params["typ"] is not None:
            filtered_typen = typen[typen["fahrzeug_typ"] == str(st.query_params["typ"])]
            if not filtered_typen.empty:
                typ = st.selectbox("Fahrzeugtyp", typen["fahrzeug_typ"], index=int(filtered_typen.index[0]))
            else:
                typ = st.selectbox("Fahrzeugtyp", typen["fahrzeug_typ"], index=None)
        else:
            typ = st.selectbox("Fahrzeugtyp", typen["fahrzeug_typ"], index=None)

        col1, col2 = st.columns([1, 2])
        with col1:
            marke = st.text_input("Marke")
        with col2:
            name = st.text_input("Name")
        gewicht = st.number_input("Gewicht in Kg", value=0)
        elektrisch = st.checkbox("Elektrisch")
        beschreibung = st.text_area("Beschreibung")
        if st.form_submit_button("Modell hinzufügen"):
            if name != "" and marke != "":
                try:
                    if marke != "":
                        name = marke + " " + name
                    session = db.session
                    typ_id = \
                        db.query("SELECT id FROM fahrzeugtypen WHERE fahrzeug_typ ='" + str(typ) + "'", ttl=0)["id"][0]
                    query = text(
                        "INSERT INTO fahrzeugmodelle(typ_id, fahrzeug_modell, gewicht, beschreibung, elektrisch) "
                        "VALUES (:typ_id, :name, :gewicht, :beschreibung, :elektrisch)")
                    session.execute(query,
                                    {"typ_id": typ_id, "name": name, "gewicht": gewicht, "beschreibung": beschreibung,
                                     "elektrisch": elektrisch})
                    session.commit()
                    session.close()
                    st.success("Modell hinzugefügt")
                    if st.query_params["s"] is not None:
                        st.switch_page("pages/Fahrzeuge_erstellen.py")
                except Exception:
                    st.error(traceback.format_exc())
            else:
                st.error("Fehlerhafte eingabe!")


neues_modell()
