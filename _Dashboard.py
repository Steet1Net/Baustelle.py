import numpy as np
import pandas as pd
import streamlit as st
import st_pages as stp

st.set_page_config(
        page_title="Baustellen- und Fahrzeugverwaltung",
        page_icon="🚧",
        layout="wide"
    )
st.title("Baustellen und Fahrzeugverwaltungs Tool")

stp.show_pages(
    [
        stp.Page("_Dashboard.py", "Dashboard", "📈"),
        stp.Page("Pages/Baustellen.py", "Baustellen", "🏗"),
        stp.Page("Pages/Fahrzeuge.py", "Fahrzeuge", "🚚"),
        stp.Page("Pages/Fahrzeuge_erstellen.py", "Fahrzeug erstellen"),
        stp.Page("Pages/Baustelle_erstellen.py", "Baustelle Erstellen"),
    ]
)

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["Bagger", "Kräne", "Kipper"])

st.area_chart(chart_data)
