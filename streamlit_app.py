"""
CV2Profile - Streamlit Deployment Entry Point (Vereinfacht)
"""

import streamlit as st
import os

# Set page config frühzeitig
st.set_page_config(
    page_title="CV2Profile Parser", 
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS zum Verstecken der Seitenleiste (bleibt wichtig für das UI)
st.markdown("""
<style>
    section[data-testid="stSidebar"] {display: none !important;}
</style>
""", unsafe_allow_html=True)

# Führe die Hauptanwendung aus
try:
    with open('main.py', 'r', encoding='utf-8') as f:
        code = f.read()
    exec(code, {'__name__': '__main__'})
except Exception as e:
    st.error(f"🚨 Kritischer Fehler beim Laden der Hauptanwendung: {e}")
    st.error("Die Anwendung konnte nicht gestartet werden. Bitte überprüfen Sie die Logs.") 