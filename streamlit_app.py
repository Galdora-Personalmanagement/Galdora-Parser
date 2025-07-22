"""
CV2Profile - Streamlit Deployment Entry Point
Robuste Lösung für Streamlit Cloud mit Pfad-Management
"""

import streamlit as st
import os
import sys

# Streamlit Cloud-kompatible Pfad-Konfiguration
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Alle notwendigen Pfade hinzufügen
paths_to_add = [
    current_dir,
    os.path.join(current_dir, 'src'),
    os.path.join(current_dir, 'src', 'core'),
    os.path.join(current_dir, 'src', 'ui'),
    os.path.join(current_dir, 'src', 'templates'),
    os.path.join(current_dir, 'src', 'utils'),
]

for path in paths_to_add:
    if path not in sys.path and os.path.exists(path):
        sys.path.insert(0, path)

# Set page config
st.set_page_config(
    page_title="CV2Profile Parser", 
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS zum Verstecken der Seitenleiste
st.markdown("""
<style>
    .css-1d391kg {display: none !important;}
    .css-1cypcdb {display: none !important;}
    .css-17lntkn {display: none !important;}
    .css-1outpf7 {display: none !important;}
    section[data-testid="stSidebar"] {display: none !important;}
    .sidebar .sidebar-content {display: none !important;}
    .stSidebar {display: none !important;}
    [data-testid="stSidebar"] {display: none !important;}
    .css-1aumxhk {display: none !important;}
</style>
""", unsafe_allow_html=True)

# Import and run
try:
    # Versuche main.py zu importieren und auszuführen
    main_path = os.path.join(current_dir, 'main.py')
    if os.path.exists(main_path):
        with open(main_path, 'r', encoding='utf-8') as f:
            code = f.read()
        exec(code, {'__file__': main_path})
    else:
        raise FileNotFoundError("main.py nicht gefunden")
    
except Exception as e:
    st.error(f"🚨 Fehler beim Laden der Hauptanwendung: {e}")
    st.info("🔄 Versuche direkten Konverter-Modus...")
    
    # Fallback: Direkte Ausführung der Konverter-Seite
    try:
        konverter_path = os.path.join(current_dir, 'src', 'ui', 'pages', '01_Konverter.py')
        if os.path.exists(konverter_path):
            with open(konverter_path, 'r', encoding='utf-8') as f:
                code = f.read()
            exec(code, {'__file__': konverter_path})
        else:
            raise FileNotFoundError("Konverter-Seite nicht gefunden")
            
    except Exception as e2:
        st.error(f"💥 Kritischer Fehler: {e2}")
        st.error("📋 **Deployment-Checkliste:**")
        st.error("1. Ist das Repository korrekt gepusht?")
        st.error("2. Sind alle Dateien im src/ Verzeichnis vorhanden?")
        st.error("3. Wurde der OpenAI API-Key in den Streamlit Secrets konfiguriert?")
        
        # Zeige verfügbare Dateien für Debugging
        st.error("**Verfügbare Dateien im Root:**")
        try:
            files = os.listdir(current_dir)
            st.error(f"Root-Dateien: {files}")
        except:
            st.error("Kann Root-Verzeichnis nicht lesen")
        
        st.stop() 