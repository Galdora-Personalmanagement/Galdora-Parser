"""
CV2Profile - Streamlit Deployment Entry Point
"""

import streamlit as st
import sys
import os

# Set page config frühzeitig
st.set_page_config(
    page_title="CV2Profile Parser", 
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS zum Verstecken der Seitenleiste
st.markdown("""
<style>
    section[data-testid="stSidebar"] {display: none !important;}
</style>
""", unsafe_allow_html=True)

# Führe die Hauptanwendung aus durch direkten Import
try:
    # Füge aktuelles Verzeichnis zum Python-Pfad hinzu
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    # Importiere und führe main.py aus
    import main
    
except Exception as e:
    st.error(f"🚨 Kritischer Fehler beim Laden der Hauptanwendung: {e}")
    st.error("Die Anwendung konnte nicht gestartet werden. Bitte überprüfen Sie die Logs.")
    st.error(f"Fehlerdetails: {type(e).__name__}: {str(e)}") 