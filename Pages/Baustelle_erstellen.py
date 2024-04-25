import streamlit as st
from sqlalchemy import text

db = st.connection('mysql', type='sql')


st.title("Neue Baustelle hinzufügen")
name = st.text_input("Name der Baustelle")
start = st.date_input("Startdatum")
ende = st.date_input("Enddatum")
status_options = ["in Bearbeitung", "abgeschlossen", "in Planung"]
status = st.selectbox("Status", status_options)
st.write(status)
if st.button("Baustelle hinzufügen"):
    if name != "":
        if start > ende:
            st.error("Endzeitpunkt kann nicht vor dem Start sein!")
        else:
            try:
                s = db.session
                q = "(NULL,'"+name+"','"+str(start)+"','"+str(ende)+"','"+status+"')"
                s.execute(text(
                    f"INSERT INTO baustellen(id, name, start, ende, status) VALUES"+q))# ({str(name)}, {str(start)}, {str(ende)}, {str(status)});"))
                s.commit()
                s.close()
                st.success("Baustelle hinzugefügt")
            except Exception as e:
                st.error(e)
    else:
        st.error("Name darf nicht leer sein!")
