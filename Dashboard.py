import streamlit as st


def show_sidebar():
    st.sidebar.page_link("/Dashboard.py", label="Dashboard", icon="📈")
    st.sidebar.page_link("pages/Baustellen.py", label="Baustellen", icon="🏗")
    st.sidebar.page_link("pages/Fahrzeuge.py", label="Fahrzeuge", icon="🚚")
    st.sidebar.page_link("pages/Fahrzeuge_erstellen.py", label="Fahrzeug erstellen", icon="🆕")
    st.sidebar.page_link("pages/Baustelle_erstellen.py", label="Baustelle Erstellen", icon="🆕")


st.set_page_config(
        page_title="Baustellen- und Fahrzeugverwaltung",
        page_icon="🚧",
        layout="wide"
    )
db = st.connection('mysql', type='sql')
show_sidebar()


st.title("Baustellen und Fahrzeugverwaltungs Tool")

st.write("Willkommen im Baustellen und Fahrzeugverwaltungs Tool. Hier können Sie Baustellen und Fahrzeuge verwalten.")
st.divider()


col1, col2, col3, col4 = st.columns(4)
col1.metric("Baustellen", db.query("SELECT COUNT(id) AS id FROM baustellen")["id"][0], "-3")
col2.metric("Fahrzeuge", db.query("SELECT COUNT(id) AS id FROM fahrzeuge")["id"][0], "2")
col3.metric("Fahrzeugmodelle", db.query("SELECT COUNT(id) AS id FROM fahrzeugmodelle")["id"][0], "1")
col4.metric("Fahrzeugtypen", db.query("SELECT COUNT(id) AS id FROM fahrzeugtypen")["id"][0], "1")

st.divider()
c = st.container(border=True)
with c:
    st.write("Adminbereich")
    st.write("[Modell hinzufügen](Modell)")

