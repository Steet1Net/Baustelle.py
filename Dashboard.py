import streamlit as st

st.set_page_config(
    page_icon="🚧",
    layout="wide",
    page_title="Dashboard"
)

status = ["in Planung", "in Bearbeitung", "abgeschlossen", 'abgebrochen']


def show_sidebar():
    """
    hide_decoration_bar_style = '''
        <style>
            header {visibility: hidden;}
        </style>
    '''
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)"""
    with st.sidebar:
        st.page_link("Dashboard.py", label="Dashboard", icon="📈")
        st.page_link("pages/Baustellen.py", label="Baustellen", icon="🏗️")
        st.page_link("pages/Fahrzeuge.py", label="Fahrzeuge", icon="🚚")
        st.page_link("pages/Fahrzeuge_erstellen.py", label="Fahrzeug erstellen", icon="🆕")
        st.page_link("pages/Baustelle_erstellen.py", label="Baustelle erstellen", icon="🆕")
        st.divider()
        st.page_link("pages/Dokumentation.py", label="Dokumentation", icon="📚")
        st.logo("logo.png")

show_sidebar()
db = st.connection('mysql', type='sql')

st.title("Baustellen und Fahrzeugverwaltung")
st.write("Willkommen im Baustellen und Fahrzeugverwaltungs Tool. Hier können Sie Baustellen und Fahrzeuge verwalten.")
st.divider()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Fahrzeuge", db.query("SELECT COUNT(id) AS id FROM fahrzeuge", ttl=0)["id"][0], "2")
col2.metric("Baustellen: Geplant",
            db.query("SELECT COUNT(id) AS id FROM baustellen WHERE status = 'in Planung'", ttl=0)["id"][0], "1")
col3.metric("Baustellen: Aktiv",
            db.query("SELECT COUNT(id) AS id FROM baustellen WHERE status = 'in Bearbeitung'", ttl=0)["id"][0], "-3")
col4.metric("Baustellen: Abgeschlossen",
            db.query("SELECT COUNT(id) AS id FROM baustellen WHERE status = 'abgeschlossen'", ttl=0)["id"][0], "1")
st.divider()

y = """
c = st.container(border=True)
with c:
    st.write("Adminbereich")
    st.page_link(page="pages/Modell.py", label="Modell hinzufügen")
    # st.link_button("Modell hinzufügen", "https://baustelle.steet.net/Modell?typ=None")
    # st.write("[Modell hinzufügen](Modell?typ=None)")
"""
with st.spinner("Lade Karte..."):
    query = "SELECT latitude, longitude FROM adressen WHERE latitude != 0 AND longitude != 0"
    a = db.query(query, ttl=0)
    st.map(a, size=None)
