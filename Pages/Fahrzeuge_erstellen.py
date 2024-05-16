from datetime import datetime
import traceback
import streamlit as st
from sqlalchemy import text
from Dashboard import db, show_sidebar

st.set_page_config(
        page_icon="🚧",
        layout="wide",
        page_title="Neues Fahrzeug"
    )
show_sidebar()


def dokumente_hochladen(session, dokumente, fahrzeug_id):
    try:
        for doc in dokumente:
            data = doc.read()
            session.execute(text("INSERT INTO fahrzeugdokumente(fahrzeug_id, dokument, dateiname) VALUES("
                                 ":fahrzeug_id, :dokument, :dateiname)"),
                            {"fahrzeug_id": fahrzeug_id, "dokument": data, "dateiname": str(doc.name)})
            session.commit()
    except Exception as e:
        st.error(e)
        st.error(traceback.format_exc())


typen = db.query("SELECT fahrzeug_typ, id FROM fahrzeugtypen")
modelle = db.query("SELECT fahrzeug_modell, beschreibung, fahrzeugtypen.Fahrzeug_typ FROM fahrzeugmodelle JOIN "
                   "fahrzeugtypen ON fahrzeugmodelle.typ_id = fahrzeugtypen.id", ttl=0)
st.title("Neues Fahrzeug hinzufügen")

col3, col4 = st.columns(2)
col1, col2 = st.columns([2, 1])
with col2:
    c = st.container(border=True)
    image = c.file_uploader("Bild Hinzufügen", accept_multiple_files=False, type=["png", "jpg", "jpeg", "webp", "jfif"])
    if image is not None:
        c.image(image)
with col1:
    with col3:
        typ = st.selectbox("Typ", typen, index=None)
    with col4:
        col5, col6 = st.columns([3, 1])
        with col5:
            if typ is None:
                fahrzeugmodell = st.selectbox("Modell", [])
            else:
                fahrzeugmodell = st.selectbox("Modell", modelle.query('Fahrzeug_typ == ' + "'" + str(typ) + "'"),
                                              index=None)
        with col6:
            st.caption('<div style="height: 28px;">Neues Modell</div>', unsafe_allow_html=True)
            st.link_button("NEU", "Modell?typ=" + str(typ))
    try:
        st.caption(str(
            db.query(
                "SELECT id, beschreibung FROM fahrzeugmodelle WHERE fahrzeug_modell ='" + str(fahrzeugmodell) + "'")[
                "beschreibung"][0]))
    except:
        pass

    with st.form("Fahrzeug hinzufügen", clear_on_submit=True):
        name = st.text_input("Name", help="z.B. Auto vom Chef, Kennzeichen...")
        baujahr = st.number_input("Baujahr", value=2000)
        kaufdatum = st.date_input("Kaufdatum")
        beschreibung = st.text_input("Anmerkung:")
        dokumente = st.file_uploader("Dokumente Hinzufügen", accept_multiple_files=True, help="z.B. Kaufvertrag, Rechnung, Fahrzeugschein")
        if st.form_submit_button("Fahrzeug hinzufügen"):
            if name != "" and len(str(baujahr)) == 4 and typ is not None and fahrzeugmodell is not None:
                try:
                    s = db.session
                    a = datetime.strptime(str(baujahr), '%Y')
                    typ_id = \
                        db.query("SELECT id FROM fahrzeugmodelle WHERE fahrzeug_modell ='" + str(fahrzeugmodell) + "'",
                                 ttl=0)[
                            "id"][0]
                    if image is not None:
                        query = text("INSERT INTO fahrzeuge(baujahr, kaufdatum, modell_id, name, beschreibung, "
                                     "bild) VALUES (:baujahr, :kaufdatum, :modell_id, :name, :beschreibung, :bild)")
                        s.execute(query, {"baujahr": str(a.strftime('%Y-%m-%d')), "kaufdatum": str(kaufdatum),
                                          "modell_id": typ_id, "name": name, "beschreibung": beschreibung,
                                          "bild": image.read()})
                    else:
                        query = text("INSERT INTO fahrzeuge(baujahr, kaufdatum, modell_id, name, beschreibung) VALUES ("
                                     ":baujahr, :kaufdatum, :modell_id, :name, :beschreibung)")
                        s.execute(query, {"baujahr": str(a.strftime('%Y-%m-%d')), "kaufdatum": str(kaufdatum),
                                          "modell_id": typ_id, "name": name, "beschreibung": beschreibung})

                    s.commit()
                    anzahl = dokumente.__len__()
                    if anzahl > 0:
                        Text = "Dokumente werden hochgeladen"
                        if anzahl == 1:
                            Text = "Dokument wird hochgeladen"
                        fahrzeug_id = db.query("SELECT MAX(id) AS id FROM fahrzeuge", ttl=0)["id"][0]
                        with st.spinner(Text):
                            dokumente_hochladen(s, dokumente, fahrzeug_id)
                    s.commit()
                    s.close()
                    st.success("Fahrzeug hinzugefügt")
                except Exception as e:
                    st.error(e)
                    st.error(traceback.format_exc())
            else:
                db.session.rollback()
                st.error("Fehlerhafte eingabe!")
