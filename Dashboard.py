import numpy as np
import pandas
import pandas as pd
import streamlit as st


def showSidebar():
    st.sidebar.page_link("Dashboard.py", label="Dashboard", icon="📈")
    st.sidebar.page_link("Pages/Baustellen.py", label="Baustellen", icon="🏗")
    st.sidebar.page_link("Pages/Fahrzeuge.py", label="Fahrzeuge", icon="🚚")
    st.sidebar.page_link("Pages/Fahrzeuge_erstellen.py", label="Fahrzeug erstellen", icon="🆕")
    st.sidebar.page_link("Pages/Baustelle_erstellen.py", label="Baustelle Erstellen", icon="🆕")


st.set_page_config(
        page_title="Baustellen- und Fahrzeugverwaltung",
        page_icon="🚧",
        layout="wide"
    )

st.title("Baustellen und Fahrzeugverwaltungs Tool")

db = st.connection('mysql', type='sql')


showSidebar()

chart_data = pd.DataFrame(np.random.randn(10, 3), columns=["Bagger", "Kräne", "Kipper"])

st.bar_chart(chart_data)

