import streamlit as st
import os
import tempfile
import json
import base64
from PIL import Image
import sys
import atexit

# Importe aus den Modulen
from src.core.document_processor import DocumentProcessor
from src.core.ai_extractor import AIExtractor  
from src.core.combined_processor import CombinedProcessor
from src.templates.template_generator import ProfileGenerator
import src.utils.config as config
from src.utils.image_utils import get_image_path, ensure_images_in_static, get_logo_as_base64
from src.utils.company_config import get_available_companies, get_company_config, get_company_logo_path, get_company_contacts
from src.utils.pdf_viewer import display_pdf_with_pdfjs
from src.ui.styles.main_styles import custom_css


# CSS für Farbverlaufshintergrund und weiße Schaltflächen
# (Ausgelagert nach src/ui/styles/main_styles.py)


# Session State für den mehrstufigen Prozess initialisieren
if 'step' not in st.session_state:
    st.session_state.step = 1  # Schritt 1: Kombinierte Extraktion & Analyse
if 'extracted_text' not in st.session_state:
    st.session_state.extracted_text = ""
if 'profile_data' not in st.session_state:
    st.session_state.profile_data = {}
if 'edited_data' not in st.session_state:
    st.session_state.edited_data = {}
if 'preview_pdf' not in st.session_state:
    st.session_state.preview_pdf = None
if 'temp_files' not in st.session_state:
    st.session_state.temp_files = []
if 'saved_api_key' not in st.session_state:
    # Lade den gespeicherten API-Key
    st.session_state.saved_api_key = config.get_openai_api_key_from_all_sources()



# Hilfsfunktionen
def create_cv_data_editor(profile_data):
    """
    Listen-basierte Bearbeitung von CV-Daten mit Pfeil-Navigation
    Arbeitet direkt mit Session State für persistente Speicherung
    
    Args:
        profile_data: Dictionary mit CV-Daten
    
    Returns:
        Dictionary mit bearbeiteten CV-Daten
    """
    
    # Session State für CV-Daten initialisieren falls noch nicht vorhanden
    if 'cv_berufserfahrung' not in st.session_state:
        st.session_state.cv_berufserfahrung = profile_data.get("berufserfahrung", [])
    if 'cv_ausbildung' not in st.session_state:
        st.session_state.cv_ausbildung = profile_data.get("ausbildung", [])
    if 'cv_weiterbildungen' not in st.session_state:
        st.session_state.cv_weiterbildungen = profile_data.get("weiterbildungen", [])
    
    def move_item_up(session_key, index):
        """Verschiebt ein Element nach oben in der Session State"""
        items = st.session_state[session_key]
        if index > 0:
            items[index], items[index-1] = items[index-1], items[index]
            st.session_state[session_key] = items
    
    def move_item_down(session_key, index):
        """Verschiebt ein Element nach unten in der Session State"""
        items = st.session_state[session_key]
        if index < len(items) - 1:
            items[index], items[index+1] = items[index+1], items[index]
            st.session_state[session_key] = items
    
    # Berufserfahrung Editor
    st.markdown("### 🏢 Berufserfahrung")
    
    # Add new entry button
    if st.button("➕ Neue Berufserfahrung hinzufügen"):
        st.session_state.cv_berufserfahrung.append({
            "zeitraum": "",
            "unternehmen": "",
            "position": "",
            "aufgaben": []
        })
        st.rerun()
    
    # Alle Berufserfahrungen untereinander anzeigen
    if st.session_state.cv_berufserfahrung:
        for i, entry in enumerate(st.session_state.cv_berufserfahrung):
            with st.container():
                # Navigations- und Aktions-Buttons links, Inhalt rechts
                col_nav, col_content = st.columns([1, 9])
                
                with col_nav:
                    # Pfeil-Buttons untereinander für kompakte Darstellung
                    if st.button("⬆️", key=f"be_up_{i}", disabled=(i == 0), help="Nach oben verschieben", use_container_width=True):
                        move_item_up('cv_berufserfahrung', i)
                        st.rerun()
                    if st.button("⬇️", key=f"be_down_{i}", disabled=(i == len(st.session_state.cv_berufserfahrung) - 1), help="Nach unten verschieben", use_container_width=True):
                        move_item_down('cv_berufserfahrung', i)
                        st.rerun()
                    if st.button("🗑️", key=f"delete_be_{i}", help="Eintrag löschen", use_container_width=True):
                        st.session_state.cv_berufserfahrung.pop(i)
                        st.rerun()
                
                with col_content:
                    # Input-Felder für den Eintrag
                    col1, col2 = st.columns(2)
                    with col1:
                        entry["zeitraum"] = st.text_input("Zeitraum", value=entry.get("zeitraum", ""), key=f"be_zeitraum_{i}")
                        entry["unternehmen"] = st.text_input("Unternehmen", value=entry.get("unternehmen", ""), key=f"be_unternehmen_{i}")
                    with col2:
                        entry["position"] = st.text_input("Position", value=entry.get("position", ""), key=f"be_position_{i}")
                        
                        # Aufgaben als mehrzeiliger Text - immer voll ausgeklappt anzeigen
                        aufgaben_text = '\n'.join(entry.get("aufgaben", [])) if isinstance(entry.get("aufgaben"), list) else str(entry.get("aufgaben", ""))
                        aufgaben_input = st.text_area("Aufgaben (eine pro Zeile)", value=aufgaben_text, key=f"be_aufgaben_{i}", height=150)
                        entry["aufgaben"] = [a.strip() for a in aufgaben_input.split('\n') if a.strip()]
                
                st.divider()
    
    st.divider()
    
    # Ausbildung Editor
    st.markdown("### 🎓 Ausbildung")
    
    # Add new entry button
    if st.button("➕ Neue Ausbildung hinzufügen"):
        st.session_state.cv_ausbildung.append({
            "zeitraum": "",
            "institution": "",
            "abschluss": "",
            "note": "",
            "schwerpunkte": ""
        })
        st.rerun()
    
    # Alle Ausbildungen untereinander anzeigen
    if st.session_state.cv_ausbildung:
        for i, entry in enumerate(st.session_state.cv_ausbildung):
            with st.container():
                # Navigations- und Aktions-Buttons links, Inhalt rechts
                col_nav, col_content = st.columns([1, 9])
                
                with col_nav:
                    # Pfeil-Buttons untereinander für kompakte Darstellung
                    if st.button("⬆️", key=f"edu_up_{i}", disabled=(i == 0), help="Nach oben verschieben", use_container_width=True):
                        move_item_up('cv_ausbildung', i)
                        st.rerun()
                    if st.button("⬇️", key=f"edu_down_{i}", disabled=(i == len(st.session_state.cv_ausbildung) - 1), help="Nach unten verschieben", use_container_width=True):
                        move_item_down('cv_ausbildung', i)
                        st.rerun()
                    if st.button("🗑️", key=f"delete_edu_{i}", help="Eintrag löschen", use_container_width=True):
                        st.session_state.cv_ausbildung.pop(i)
                        st.rerun()
                
                with col_content:
                    # Input-Felder für den Eintrag
                    col1, col2 = st.columns(2)
                    with col1:
                        entry["zeitraum"] = st.text_input("Zeitraum", value=entry.get("zeitraum", ""), key=f"edu_zeitraum_{i}")
                        entry["institution"] = st.text_input("Institution", value=entry.get("institution", ""), key=f"edu_institution_{i}")
                        entry["abschluss"] = st.text_input("Abschluss", value=entry.get("abschluss", ""), key=f"edu_abschluss_{i}")
                    with col2:
                        entry["note"] = st.text_input("Note", value=entry.get("note", ""), key=f"edu_note_{i}")
                        entry["schwerpunkte"] = st.text_area("Schwerpunkte", value=entry.get("schwerpunkte", ""), key=f"edu_schwerpunkte_{i}", height=150)
                
                st.divider()
    
    st.divider()
    
    # Weiterbildungen Editor
    st.markdown("### 📚 Weiterbildungen")
    
    # Add new entry button
    if st.button("➕ Neue Weiterbildung hinzufügen"):
        st.session_state.cv_weiterbildungen.append({
            "zeitraum": "",
            "bezeichnung": "",
            "abschluss": ""
        })
        st.rerun()
    
    # Alle Weiterbildungen untereinander anzeigen
    if st.session_state.cv_weiterbildungen:
        for i, entry in enumerate(st.session_state.cv_weiterbildungen):
            with st.container():
                # Navigations- und Aktions-Buttons links, Inhalt rechts
                col_nav, col_content = st.columns([1, 9])
                
                with col_nav:
                    # Pfeil-Buttons untereinander für kompakte Darstellung
                    if st.button("⬆️", key=f"wb_up_{i}", disabled=(i == 0), help="Nach oben verschieben", use_container_width=True):
                        move_item_up('cv_weiterbildungen', i)
                        st.rerun()
                    if st.button("⬇️", key=f"wb_down_{i}", disabled=(i == len(st.session_state.cv_weiterbildungen) - 1), help="Nach unten verschieben", use_container_width=True):
                        move_item_down('cv_weiterbildungen', i)
                        st.rerun()
                    if st.button("🗑️", key=f"delete_wb_{i}", help="Eintrag löschen", use_container_width=True):
                        st.session_state.cv_weiterbildungen.pop(i)
                        st.rerun()
                
                with col_content:
                    # Input-Felder für den Eintrag
                    col1, col2 = st.columns(2)
                    with col1:
                        entry["zeitraum"] = st.text_input("Zeitraum", value=entry.get("zeitraum", ""), key=f"wb_zeitraum_{i}")
                        entry["bezeichnung"] = st.text_input("Bezeichnung", value=entry.get("bezeichnung", ""), key=f"wb_bezeichnung_{i}")
                    with col2:
                        entry["abschluss"] = st.text_input("Abschluss/Details", value=entry.get("abschluss", ""), key=f"wb_abschluss_{i}")
                
                st.divider()
    
    # Rückgabe der aktuellen Session State Daten
    return {
        'berufserfahrung': st.session_state.cv_berufserfahrung,
        'ausbildung': st.session_state.cv_ausbildung,
        'weiterbildungen': st.session_state.cv_weiterbildungen
    }



# Seitentitel und Konfiguration
st.set_page_config(page_title="CV2Profile Konverter", layout="wide")

# Stelle sicher, dass alle Bilder im static-Verzeichnis verfügbar sind für HTTPS-Kompatibilität
ensure_images_in_static()

# CSS einbinden
st.markdown(custom_css, unsafe_allow_html=True)

# Header-Bereich mit verbessertem Glasmorphismus-Effekt
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

st.markdown("""
<div style="background-color: rgba(255, 255, 255, 0.15); padding: 1.5rem; border-radius: 15px; margin-bottom: 1.5rem; color: white; text-align: center; backdrop-filter: blur(12px); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.25); border: 1px solid rgba(255, 255, 255, 0.18);">
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
        <img src="data:image/png;base64,{}" alt="CV2Profile Logo" style="max-width: 120px; margin-bottom: 1rem;">
        <h1 style="margin: 0; font-weight: 700; font-size: 2rem; text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);">CV2Profile Konverter</h1>
        <p style="margin-top: 0.8rem; font-size: 1rem; opacity: 0.95;">Konvertiere deinen Lebenslauf in ein professionelles Profil. Lade deine Datei hoch, wähle die gewünschten Informationen aus und gestalte dein Profil.</p>
    </div>
</div>
""".format(get_logo_as_base64()), unsafe_allow_html=True)

# Entfernte Seitenleiste - Einstellungen wurden in den Hauptbereich integriert

# Verwende den gespeicherten API-Key aus der Projektkonfiguration
openai_api_key = config.get_openai_api_key_from_all_sources()

# UNTERNEHMEN-AUSWAHL (Neu hinzugefügt)
st.markdown("---")
st.markdown("### 🏢 Unternehmen auswählen")
st.markdown("Wählen Sie das Unternehmen aus, für das Sie Profile erstellen möchten:")

# Unternehmen-Auswahl
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        companies = get_available_companies()
        
        # Standardauswahl aus Session State oder Default
        default_company = st.session_state.get('selected_company', 'galdora')
        
        # Selectbox für Unternehmen
        selected_company = st.selectbox(
            "Unternehmen:",
            options=list(companies.keys()),
            format_func=lambda x: companies[x],
            index=list(companies.keys()).index(default_company) if default_company in companies else 0,
            key="company_selector"
        )
        
        # In Session State speichern
        st.session_state.selected_company = selected_company
        
        # Unternehmen-Information anzeigen
        company_config = get_company_config(selected_company)
        
        # Logo und Beschreibung anzeigen
        col_logo, col_info = st.columns([1, 2])
        
        with col_logo:
            logo_path = get_company_logo_path(selected_company)
            if logo_path and os.path.exists(logo_path):
                st.image(logo_path, width=120)
            else:
                # Fallback-Icon
                st.markdown(f"""
                <div style="width: 120px; height: 60px; background: {company_config['colors']['primary']}; 
                     border-radius: 8px; display: flex; align-items: center; justify-content: center; 
                     color: white; font-weight: bold; font-size: 16px;">
                    {company_config['name']}
                </div>
                """, unsafe_allow_html=True)
        
        with col_info:
            st.markdown(f"""
            **{company_config['display_name']}**  
            *{company_config['description']}*
            
            Alle generierten Profile werden mit dem {company_config['display_name']}-Logo erstellt.
            """)
            
    except Exception as e:
        st.error(f"Fehler bei der Unternehmen-Auswahl: {str(e)}")
        # Fallback auf Galdora
        st.session_state.selected_company = 'galdora'
        selected_company = 'galdora'

st.markdown("---")

# Warnmeldung direkt unter der Trennlinie
st.warning("""
    **ACHTUNG:** Alle extrahierten Informationen müssen händisch geprüft werden. 
    Bei fehlerhafter Analyse des Lebenslaufes muss der Prozess neu gestartet werden.
""")

# Hauptbereich - basierend auf dem aktuellen Schritt
if st.session_state.step == 1:
    # Schritt 1: Datei hochladen und Text extrahieren/analysieren oder leere Vorlage erstellen
    st.subheader("1. Lebenslauf hochladen und verarbeiten")
    
    # Auswahl zwischen CV-Upload und leerer Vorlage
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        mode_selection = st.radio(
            "Wie möchten Sie vorgehen?",
            options=["📄 Lebenslauf hochladen", "📝 Leere Profilvorlage erstellen"],
            horizontal=True,
            key="mode_selection"
        )
    
    # Normaler Modus - Standardmäßig wird der "Standard (Extraktion → Analyse)"-Modus verwendet
    processing_mode = "Standard (Extraktion → Analyse)"
    
    uploaded_file = None
    
    if mode_selection == "📄 Lebenslauf hochladen":
        # Zentrale Spalte für den File Uploader
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            uploaded_file = st.file_uploader(
                "📁 Lebenslauf hochladen (PDF, JPG, PNG, DOCX)",
                label_visibility="visible",
                help="Unterstützte Dateiformate für die Verarbeitung"
            )
    
    elif mode_selection == "📝 Leere Profilvorlage erstellen":
        # Erklärung zur leeren Profilvorlage
        st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.15); border-radius: 12px; backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.2); box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15); padding: 15px 20px; margin-bottom: 20px;">
            <div style="display: flex; align-items: center;">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="white" style="margin-right: 10px;">
                    <path d="M14,3V5H17.59L7.76,14.83L9.17,16.24L19,6.41V10H21V3M19,19H5V5H12V3H5C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V12H19V19Z"/>
                </svg>
                <span style="color: white; font-weight: 500;">Erstellen Sie eine Profilvorlage ohne Lebenslauf-Upload. Alle Felder können manuell ausgefüllt werden.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Zentrale Spalte für den Button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Weiter zu Schritt 2 - Profil bearbeiten", use_container_width=True, type="primary"):
                # Initialisiere leere Profildaten
                empty_profile_data = {
                    "persönliche_daten": {
                        "name": "",
                        "wohnort": "",
                        "jahrgang": "",
                        "führerschein": "",
                        "wunschgehalt": ""
                    },
                    "berufserfahrung": [],
                    "ausbildung": [],
                    "weiterbildungen": []
                }
                
                # Setze Profile-Daten für die weitere Verarbeitung
                st.session_state.profile_data = empty_profile_data
                st.session_state.empty_template_mode = True  # Markiere als leere Vorlage
        
        # Wenn leere Vorlage ausgewählt wurde, zeige die Tabs direkt an
        if st.session_state.get('empty_template_mode'):
            profile_data = st.session_state.profile_data
            
            # Visueller Trenner
            st.markdown("""
            <div style="height: 30px;"></div>
            <div style="background: rgba(255, 255, 255, 0.2); height: 2px; border-radius: 1px; margin: 10px 0;"></div>
            <div style="height: 30px;"></div>
            """, unsafe_allow_html=True)
            
            st.subheader("2. Profil erstellen und exportieren")
            
            # Profildaten aus der Session holen
            edited_data = {}
            
            # Zwei Tabs erstellen für Informationsauswahl und Profil-Generierung mit verbessertem Stil
            st.markdown("""
            <style>
                .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
                    background-color: rgba(255, 255, 255, 0.2) !important;
                    color: white !important;
                    font-weight: 600 !important;
                }
                .stTabs [data-baseweb="tab-list"] button {
                    padding: 10px 20px !important;
                }
            </style>
            """, unsafe_allow_html=True)
            tab1, tab2 = st.tabs(["Informationen bearbeiten", "Profil exportieren"])
            
            with tab1:
                # Persönliche Daten
                st.markdown("### Persönliche Daten")
                personal_data = profile_data.get("persönliche_daten", {})
                
                # Name und Grunddaten
                col1, col2, col3 = st.columns(3)
                with col1:
                    edited_data["name"] = st.text_input("Name", value=personal_data.get("name", ""), key="empty_name")
                with col2:
                    edited_data["wohnort"] = st.text_input("Wohnort", value=personal_data.get("wohnort", ""), key="empty_wohnort")
                with col3:
                    edited_data["jahrgang"] = st.text_input("Jahrgang", value=personal_data.get("jahrgang", ""), key="empty_jahrgang")
                
                # Führerschein und Wunschgehalt
                col1, col2 = st.columns(2)
                with col1:
                    # Führerschein-Multiselect mit definierten Optionen
                    fuehrerschein_options = [
                        "Klasse B",
                        "Klasse B + PKW vorhanden",
                        "Kein Führerschein",
                        "LKW-Führerschein",
                        "Staplerschein"
                    ]
                    
                    selected_fuehrerschein = st.multiselect(
                        "Führerschein",
                        options=fuehrerschein_options,
                        default=[],
                        help="Mehrfachauswahl möglich",
                        key="empty_fuehrerschein"
                    )
                    
                    # Konvertiere die ausgewählten Optionen in einen kommagetrennten String
                    edited_data["führerschein"] = ", ".join(selected_fuehrerschein) if selected_fuehrerschein else ""
                
                with col2:
                    edited_data["wunschgehalt"] = st.text_input("Wunschgehalt", value="", key="empty_wunschgehalt")
                
                # Verfügbarkeit des Bewerbers
                st.markdown("### Verfügbarkeit")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Dropdown für Verfügbarkeitsstatus
                    verfuegbarkeit_optionen = [
                        "Sofort verfügbar",
                        "Verfügbar ab bestimmtem Datum",
                        "Kündigungsfrist 1 Monat",
                        "Kündigungsfrist 2 Monate",
                        "Kündigungsfrist 3 Monate",
                        "Derzeit nicht verfügbar",
                        "Verfügbar mit Einschränkungen"
                    ]
                    
                    verfuegbarkeit_status = st.selectbox(
                        "Verfügbarkeitsstatus",
                        options=verfuegbarkeit_optionen,
                        index=0,
                        key="empty_verfuegbarkeit_status"
                    )
                
                with col2:
                    # Kalender für Verfügbarkeitsdatum, nur anzeigen wenn "Verfügbar ab bestimmtem Datum" ausgewählt
                    if verfuegbarkeit_status == "Verfügbar ab bestimmtem Datum":
                        verfuegbarkeit_datum = st.date_input(
                            "Verfügbar ab",
                            value=None,
                            key="empty_verfuegbarkeit_datum"
                        )
                        verfuegbarkeit_details = f"Verfügbar ab {verfuegbarkeit_datum.strftime('%d.%m.%Y')}" if verfuegbarkeit_datum else ""
                    else:
                        verfuegbarkeit_details = ""
                
                # Verfügbarkeitsdaten speichern
                edited_data["verfuegbarkeit_status"] = verfuegbarkeit_status
                edited_data["verfuegbarkeit_details"] = verfuegbarkeit_details

                # Kontaktinformationen
                st.markdown("### Kontaktinformationen")
                kontakt = personal_data.get("kontakt", {})
                
                # Ansprechpartner basierend auf ausgewähltem Unternehmen anzeigen
                company_key = st.session_state.get('selected_company', 'galdora')
                company_contacts = get_company_contacts(company_key)
                
                # Ansprechpartner-Optionen erstellen
                ansprechpartner_options = ["Kein Ansprechpartner"]
                
                # Ansprechpartner aus der Unternehmenskonfiguration hinzufügen
                for contact in company_contacts:
                    ansprechpartner_options.append(contact["name"])
                
                # Ansprechpartner auswählen
                col1, col2, col3 = st.columns(3)
                with col1:
                    selected_ansprechpartner = st.selectbox(
                        "Ansprechpartner",
                        options=ansprechpartner_options,
                        index=0,
                        key="empty_ansprechpartner"
                    )
                    edited_data["ansprechpartner"] = selected_ansprechpartner
                    
                    # E-Mail-Adresse und Telefon basierend auf dem ausgewählten Ansprechpartner
                    email = ""
                    telefon = ""
                    
                    if selected_ansprechpartner != "Kein Ansprechpartner":
                        # Suche den ausgewählten Ansprechpartner in der Liste
                        for contact in company_contacts:
                            if contact["name"] == selected_ansprechpartner:
                                email = contact["email"]
                                telefon = contact["phone"]
                                break
                    
                    edited_data["email"] = email
                
                with col2:
                    # Telefonnummer anzeigen
                    edited_data["telefon"] = st.text_input("Telefon", value=telefon, disabled=True, key="empty_telefon")
                
                with col3:
                    # E-Mail-Adresse anzeigen
                    st.text_input("E-Mail", value=email, disabled=True, key="empty_email")
                
                # CV-Daten-Editor mit eindeutigen Keys
                
                # Bereite die Daten vor
                cv_data = {
                    'berufserfahrung': profile_data.get("berufserfahrung", []),
                    'ausbildung': profile_data.get("ausbildung", []),
                    'weiterbildungen': profile_data.get("weiterbildungen", [])
                }
                
                # Dropdown-basierter CV-Editor
                edited_cv_data = create_cv_data_editor(cv_data)
                
                # Aktualisierte Daten aus Session State verwenden (für persistente Sortierung)
                all_experience = st.session_state.get('cv_berufserfahrung', [])
                all_education = st.session_state.get('cv_ausbildung', [])
                all_training = st.session_state.get('cv_weiterbildungen', [])
                
                # Zusammenführen der bearbeiteten Daten
                complete_edited_data = {
                    "persönliche_daten": {
                        "name": edited_data.get("name", ""),
                        "wohnort": edited_data.get("wohnort", ""),
                        "jahrgang": edited_data.get("jahrgang", ""),
                        "führerschein": edited_data.get("führerschein", ""),
                        "kontakt": {
                            "ansprechpartner": edited_data.get("ansprechpartner", ""),
                            "telefon": edited_data.get("telefon", ""),
                            "email": edited_data.get("email", "")
                        },
                        "profile_image": st.session_state.get("profile_image_path", None)
                    },
                    "berufserfahrung": all_experience,
                    "ausbildung": all_education,
                    "weiterbildungen": all_training,
                    "wunschgehalt": edited_data.get("wunschgehalt", ""),
                    "verfuegbarkeit_status": edited_data.get("verfuegbarkeit_status", "Sofort verfügbar"),
                    "verfuegbarkeit_details": edited_data.get("verfuegbarkeit_details", "")
                }
                
                # Speichern der bearbeiteten Daten in der Session
                st.session_state.edited_data = complete_edited_data
            
            with tab2:
                # Profil generieren und Vorschau anzeigen
                st.markdown("### Profilvorschau und Export")
                
                # Zuerst prüfen, ob edited_data in der Session verfügbar ist und wenn nicht, initialisieren
                if "edited_data" not in st.session_state:
                    # Vorbereitete Daten für Tab2 erstellen
                    complete_edited_data = {
                        "persönliche_daten": {
                            "name": profile_data.get("persönliche_daten", {}).get("name", ""),
                            "wohnort": profile_data.get("persönliche_daten", {}).get("wohnort", ""),
                            "jahrgang": profile_data.get("persönliche_daten", {}).get("jahrgang", ""),
                            "führerschein": profile_data.get("persönliche_daten", {}).get("führerschein", ""),
                            "kontakt": profile_data.get("persönliche_daten", {}).get("kontakt", {})
                        },
                        "berufserfahrung": profile_data.get("berufserfahrung", []),
                        "ausbildung": profile_data.get("ausbildung", []),
                        "weiterbildungen": profile_data.get("weiterbildungen", []),
                        "wunschgehalt": profile_data.get("wunschgehalt", "")
                    }
                    # In Session State speichern
                    st.session_state.edited_data = complete_edited_data
                
                # Profildaten aus der Session holen und mit aktuellen CV-Daten aktualisieren
                try:
                    edited_data_to_use = st.session_state.edited_data.copy()
                    
                    # Sicherstellen, dass die aktuellsten CV-Daten aus Session State verwendet werden
                    edited_data_to_use["berufserfahrung"] = st.session_state.get('cv_berufserfahrung', [])
                    edited_data_to_use["ausbildung"] = st.session_state.get('cv_ausbildung', [])
                    edited_data_to_use["weiterbildungen"] = st.session_state.get('cv_weiterbildungen', [])
                    
                    # Sicherstellen, dass es ein Dictionary ist
                    if not isinstance(edited_data_to_use, dict):
                        edited_data_to_use = {
                            "persönliche_daten": profile_data.get("persönliche_daten", {}),
                            "berufserfahrung": st.session_state.get('cv_berufserfahrung', []),
                            "ausbildung": st.session_state.get('cv_ausbildung', []),
                            "weiterbildungen": st.session_state.get('cv_weiterbildungen', []),
                            "wunschgehalt": profile_data.get("wunschgehalt", "")
                        }
                except Exception as e:
                    print(f"Fehler beim Laden der bearbeiteten Daten: {e}")
                    # Fallback auf ursprüngliche Daten mit Session State CV-Daten
                    edited_data_to_use = {
                        "persönliche_daten": profile_data.get("persönliche_daten", {}),
                        "berufserfahrung": st.session_state.get('cv_berufserfahrung', profile_data.get("berufserfahrung", [])),
                        "ausbildung": st.session_state.get('cv_ausbildung', profile_data.get("ausbildung", [])),
                        "weiterbildungen": st.session_state.get('cv_weiterbildungen', profile_data.get("weiterbildungen", [])),
                        "wunschgehalt": profile_data.get("wunschgehalt", "")
                    }
                
                # Vorlage auswählen
                st.markdown("#### Vorlage auswählen")
                
                # Standard-Vorlage aus der Konfiguration holen
                default_template = config.get_all_settings().get("default_template", "professional")
                
                # Template-Auswahl als Variable speichern
                template_to_use = default_template
                
                # Nur Classic Template verfügbar
                template_to_use = "classic"
                st.info("📄 Klassisches Template wird verwendet")
                        
                # Profil-Vorschau generieren und anzeigen
                if 'preview_pdf' not in st.session_state or st.button("Vorschau aktualisieren", key="empty_preview") or st.session_state.get('update_preview', False):
                    # Reset des Update-Flags
                    st.session_state.update_preview = False
                    with st.spinner("Profil wird generiert..."):
                        try:
                            # Verwende das ausgewählte Unternehmen für den Generator
                            selected_company = st.session_state.get('selected_company', 'galdora')
                            generator = ProfileGenerator(selected_company=selected_company)
                            output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                            output_path = output_file.name
                            output_file.close()
                            st.session_state.temp_files.append(output_path)
                            
                            # Generiere Profil mit dem ausgewählten Template
                            profile_path = generator.generate_profile(edited_data_to_use, output_path, template=template_to_use)
                            st.session_state.preview_pdf = profile_path
                            
                            # Zeige eine Erfolgsmeldung an
                            st.success("Profil erfolgreich generiert!")
                            
                            # Speichere das ausgewählte Template für zukünftige Aktualisierungen
                            st.session_state.selected_template = template_to_use
                        except Exception as e:
                            st.error(f"Fehler bei der Generierung des Profils: {str(e)}")
                
                # PDF-Vorschau anzeigen mit PDF.js
                if st.session_state.preview_pdf:
                    st.markdown("#### 📄 Profil-Vorschau")
                    # Prüfen ob die Datei existiert, bevor wir versuchen sie anzuzeigen
                    if st.session_state.preview_pdf and os.path.exists(st.session_state.preview_pdf):
                        
                        try:
                            # Verwende die A4-optimierte PDF.js-basierte Vorschau
                            st.markdown("**📄 A4-Format Vorschau** (mit Navigation und Zoom):")
                            display_pdf_with_pdfjs(st.session_state.preview_pdf)
                            
                            # Zusätzlicher Download-Button für direkten Zugriff
                            with open(st.session_state.preview_pdf, "rb") as pdf_file:
                                pdf_bytes = pdf_file.read()
                            # Name für die Vorschau-Datei
                            try:
                                if isinstance(edited_data_to_use, dict) and "persönliche_daten" in edited_data_to_use:
                                    personal_data_name = edited_data_to_use["persönliche_daten"]
                                    if isinstance(personal_data_name, dict) and "name" in personal_data_name:
                                        preview_name = str(personal_data_name["name"]).replace(" ", "-")
                                    else:
                                        preview_name = "Unbekannt"
                                else:
                                    preview_name = "Unbekannt"
                                
                                if not preview_name or preview_name == "" or preview_name == "-":
                                    preview_name = "Unbekannt"
                            except Exception as e:
                                preview_name = "Unbekannt"
                            
                            st.download_button(
                                label="📥 PDF herunterladen",
                                data=pdf_bytes,
                                file_name=f"Profilvorlage-{preview_name}.pdf",
                                mime="application/pdf",
                                help="Laden Sie das PDF direkt herunter",
                                use_container_width=True,
                                key="empty_download_preview"
                            )
                            
                        except Exception as e:
                            st.error(f"Fehler bei der PDF-Anzeige: {str(e)}")
                    else:
                        st.error("Die PDF-Vorschau ist nicht verfügbar. Bitte generieren Sie die Vorschau erneut.")
                    
                    # Name für das Profil
                    try:
                        if isinstance(edited_data_to_use, dict) and "persönliche_daten" in edited_data_to_use:
                            personal_data_name = edited_data_to_use["persönliche_daten"]
                            if isinstance(personal_data_name, dict) and "name" in personal_data_name:
                                name = str(personal_data_name["name"]).replace(" ", "-")
                            else:
                                name = "Profil"
                        else:
                            name = "Profil"
                        
                        if not name or name == "" or name == "-":
                            name = "Profil"
                    except Exception as e:
                        print(f"Fehler beim Laden des Namens: {e}")
                        name = "Profil"
                    
                    # Auswahl des Formats mit RadioButtons
                    st.markdown("#### Format wählen")
                    format_option = st.radio(
                        "In welchem Format möchten Sie das Profil herunterladen?",
                        options=["PDF", "Word"],
                        horizontal=True,
                        key="empty_format_choice"
                    )
                    
                    # Je nach Auswahl unterschiedlichen Download-Button anzeigen
                    if format_option == "PDF":
                        # PDF-Download
                        if st.session_state.preview_pdf and os.path.exists(st.session_state.preview_pdf):
                            with open(st.session_state.preview_pdf, "rb") as file:
                                st.download_button(
                                    label="Profil herunterladen",
                                    data=file,
                                    file_name=f"Profilvorlage-{name}.pdf",
                                    mime="application/pdf",
                                    key="empty_download_pdf"
                                )
                        else:
                            st.error("Bitte generieren Sie zuerst eine Vorschau des Profils.")
                    else:
                        # Word-Dokument generieren und herunterladen
                        # Temporäre Datei für das Word-Dokument erstellen
                        output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
                        output_path = output_file.name
                        output_file.close()
                        st.session_state.temp_files.append(output_path)
                        
                        try:
                            # Stelle sicher, dass generator definiert ist mit der richtigen Unternehmens-Auswahl
                            selected_company = st.session_state.get('selected_company', 'galdora')
                            generator = ProfileGenerator(selected_company=selected_company)
                            
                            # Stelle sicher, dass template_to_use definiert ist
                            template_to_use = st.session_state.get('selected_template', 'classic')
                            
                            # Word-Dokument mit dem gleichen Generator erstellen
                            docx_path = generator.generate_profile(
                                edited_data_to_use, 
                                output_path, 
                                template=template_to_use,
                                format="docx"
                            )
                            
                            # Word-Dokument zum Download anbieten
                            with open(docx_path, "rb") as file:
                                st.download_button(
                                    label="Profil herunterladen",
                                    data=file,
                                    file_name=f"Profilvorlage-{name}.docx",
                                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                    key="empty_download_word"
                                )
                        except Exception as e:
                            st.error(f"Fehler bei der Word-Dokument-Generierung: {str(e)}")
    
    # Wenn eine Datei hochgeladen wurde, zeige den Dateinamen kleiner und zentriert an
    if uploaded_file:
        st.markdown(f"""
        <div style="display: flex; justify-content: center; margin-top: 10px;">
            <div style="background: rgba(255, 255, 255, 0.15); border-radius: 8px; padding: 8px 16px; 
                 backdrop-filter: blur(5px); -webkit-backdrop-filter: blur(5px); 
                 border: 1px solid rgba(255, 255, 255, 0.1); max-width: 80%; text-align: center;">
                <div style="display: flex; align-items: center; justify-content: center;">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16" fill="white" style="margin-right: 8px;">
                        <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
                    </svg>
                    <span style="color: white; font-size: 0.9rem;">{uploaded_file.name}</span>
                </div>
                <div style="font-size: 0.7rem; color: rgba(255,255,255,0.7); margin-top: 4px;">
                    {round(len(uploaded_file.getvalue())/1024, 1)} KB
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Prüfen, ob File und API Key vorhanden sind
    if uploaded_file and not openai_api_key:
        st.error("🚨 Kein OpenAI API-Key gefunden. Bitte hinterlegen Sie Ihren Key in den Streamlit Cloud Secrets.")
        st.info("Klicken Sie auf 'Manage app' → 'Settings' → 'Secrets' und fügen Sie `openai_api_key = 'sk-...'` hinzu.")
    
    # Prüfen, ob File und API Key vorhanden sind
    if uploaded_file and openai_api_key:
            with st.spinner("Datei wird verarbeitet..."):
                # Temporäre Datei erstellen
                file_extension = os.path.splitext(uploaded_file.name)[1].lower()
                with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
                    tmp_file.write(uploaded_file.getbuffer())
                    temp_file_path = tmp_file.name
                    st.session_state.temp_files.append(temp_file_path)
                
                try:
                    # Initialisiere den kombinierten Prozessor
                    combined_processor = CombinedProcessor(openai_api_key)
                    
                    # Vor der Verarbeitung prüfen, ob die Datei im Cache ist
                    file_hash = combined_processor._get_file_hash(temp_file_path)
                    is_cached = combined_processor._check_cache(file_hash) is not None
                    
                    # Verarbeite das Dokument im ausgewählten Modus
                    if "Umgekehrt" in processing_mode:
                        # Umgekehrte Reihenfolge (Analyse → Extraktion)
                        cache_status = "aus Cache geladen" if is_cached else "wird verarbeitet"
                        with st.spinner(f"Analysiere Lebenslauf in umgekehrter Reihenfolge... ({cache_status})"):
                            profile_data, extracted_text = combined_processor.extract_and_process(temp_file_path, file_extension)
                    else:
                        # Standard-Reihenfolge (Extraktion → Analyse)
                        cache_status = "aus Cache geladen" if is_cached else "wird verarbeitet"
                        with st.spinner(f"Extrahiere Text und analysiere Lebenslauf... ({cache_status})"):
                            extracted_text, profile_data = combined_processor.process_and_extract(temp_file_path, file_extension)
                    
                    # Speichere Ergebnisse in der Session
                    st.session_state.extracted_text = extracted_text
                    st.session_state.profile_data = profile_data
                
                except Exception as e:
                    st.error(f"Fehler bei der Verarbeitung: {str(e)}")
                    st.stop()

                # Speichere die Ergebnisse für die spätere Anzeige am Ende der Seite
                
                # Zeige einen Erfolgshinweis an
                st.markdown("""
                <div style="background: rgba(255, 255, 255, 0.15); border-radius: 12px; backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.2); box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15); padding: 15px 20px; margin-bottom: 20px;">
                    <div style="display: flex; align-items: center;">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="white" style="margin-right: 10px;">
                            <path d="M12 2C6.5 2 2 6.5 2 12S6.5 22 12 22 22 17.5 22 12 17.5 2 12 2M10 17L5 12L6.41 10.59L10 14.17L17.59 6.58L19 8L10 17Z"/>
                        </svg>
                        <span style="color: white; font-weight: 500;">Dein Lebenslauf wurde erfolgreich analysiert. Jetzt kannst du die gewünschten Informationen auswählen.</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Visueller Trenner und Abstand zwischen den Abschnitten
                st.markdown("""
                <div style="height: 30px;"></div>
                <div style="background: rgba(255, 255, 255, 0.2); height: 2px; border-radius: 1px; margin: 10px 0;"></div>
                <div style="height: 30px;"></div>
                """, unsafe_allow_html=True)
                
                # Statt Button für nächsten Schritt direkt Schritt 2 (Profil erstellen) anzeigen
                st.subheader("2. Profil erstellen und exportieren")
                
                # Profildaten aus der Session holen
                edited_data = {}
                
                # Zwei Tabs erstellen für Informationsauswahl und Profil-Generierung mit verbessertem Stil
                st.markdown("""
                <style>
                    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
                        background-color: rgba(255, 255, 255, 0.2) !important;
                        color: white !important;
                        font-weight: 600 !important;
                    }
                    .stTabs [data-baseweb="tab-list"] button {
                        padding: 10px 20px !important;
                    }
                </style>
                """, unsafe_allow_html=True)
                tab1, tab2 = st.tabs(["Informationen bearbeiten", "Profil exportieren"])
                
                with tab1:
                    # Persönliche Daten
                    st.markdown("### Persönliche Daten")
                    personal_data = profile_data.get("persönliche_daten", {})
                    
                    # Name und Grunddaten
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        edited_data["name"] = st.text_input("Name", value=personal_data.get("name", ""))
                    with col2:
                        edited_data["wohnort"] = st.text_input("Wohnort", value=personal_data.get("wohnort", ""))
                    with col3:
                        edited_data["jahrgang"] = st.text_input("Jahrgang", value=personal_data.get("jahrgang", ""))
                    

                    

                    
                    # Führerschein und Wunschgehalt
                    col1, col2 = st.columns(2)
                    with col1:
                        # Führerschein-Multiselect mit definierten Optionen
                        fuehrerschein_options = [
                            "Klasse B",
                            "Klasse B + PKW vorhanden",
                            "Kein Führerschein",
                            "LKW-Führerschein",
                            "Staplerschein"
                        ]
                        
                        # Aktuellen Führerscheineintrag in Liste aufteilen, wenn er bereits existiert
                        current_fuehrerschein = personal_data.get("führerschein", "")
                        default_selected = []
                        
                        # Versuche, den aktuellen Wert den Optionen zuzuordnen
                        if current_fuehrerschein:
                            # Exakte Übereinstimmungen
                            for option in fuehrerschein_options:
                                if option in current_fuehrerschein:
                                    default_selected.append(option)
                            
                            # Wenn keine Übereinstimmungen gefunden wurden, füge Default-Option hinzu
                            if not default_selected and "Klasse B" in current_fuehrerschein:
                                default_selected.append("Klasse B")
                                if "PKW vorhanden" in current_fuehrerschein or "Pkw vorhanden" in current_fuehrerschein:
                                    default_selected.append("Klasse B + PKW vorhanden")
                        
                        selected_fuehrerschein = st.multiselect(
                            "Führerschein",
                            options=fuehrerschein_options,
                            default=default_selected,
                            help="Mehrfachauswahl möglich"
                        )
                        
                        # Konvertiere die ausgewählten Optionen in einen kommagetrennten String
                        edited_data["führerschein"] = ", ".join(selected_fuehrerschein) if selected_fuehrerschein else ""
                    
                    with col2:
                        edited_data["wunschgehalt"] = st.text_input("Wunschgehalt", value=profile_data.get("wunschgehalt", ""))
                    
                    # Verfügbarkeit des Bewerbers
                    st.markdown("### Verfügbarkeit")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Dropdown für Verfügbarkeitsstatus
                        verfuegbarkeit_optionen = [
                            "Sofort verfügbar",
                            "Verfügbar ab bestimmtem Datum",
                            "Kündigungsfrist 1 Monat",
                            "Kündigungsfrist 2 Monate",
                            "Kündigungsfrist 3 Monate",
                            "Derzeit nicht verfügbar",
                            "Verfügbar mit Einschränkungen"
                        ]
                        
                        verfuegbarkeit_status = st.selectbox(
                            "Verfügbarkeitsstatus",
                            options=verfuegbarkeit_optionen,
                            index=0,
                            key="verfuegbarkeit_status"
                        )
                    
                    with col2:
                        # Kalender für Verfügbarkeitsdatum, nur anzeigen wenn "Verfügbar ab bestimmtem Datum" ausgewählt
                        if verfuegbarkeit_status == "Verfügbar ab bestimmtem Datum":
                            verfuegbarkeit_datum = st.date_input(
                                "Verfügbar ab",
                                value=None,
                                key="verfuegbarkeit_datum"
                            )
                            verfuegbarkeit_details = f"Verfügbar ab {verfuegbarkeit_datum.strftime('%d.%m.%Y')}" if verfuegbarkeit_datum else ""
                        else:
                            verfuegbarkeit_details = ""
                    
                    # Verfügbarkeitsdaten speichern
                    edited_data["verfuegbarkeit_status"] = verfuegbarkeit_status
                    edited_data["verfuegbarkeit_details"] = verfuegbarkeit_details

                    # Kontaktinformationen
                    st.markdown("### Kontaktinformationen")
                    kontakt = personal_data.get("kontakt", {})
                    
                    # Ansprechpartner basierend auf ausgewähltem Unternehmen anzeigen
                    company_key = st.session_state.get('selected_company', 'galdora')
                    company_contacts = get_company_contacts(company_key)
                    
                    # Ansprechpartner-Optionen erstellen
                    ansprechpartner_options = ["Kein Ansprechpartner"]
                    
                    # Ansprechpartner aus der Unternehmenskonfiguration hinzufügen
                    for contact in company_contacts:
                        ansprechpartner_options.append(contact["name"])
                    
                    # Vorauswahl des Ansprechpartners (falls vorhanden)
                    current_ansprechpartner = kontakt.get("ansprechpartner", "Kein Ansprechpartner")
                    default_index = 0
                    if current_ansprechpartner in ansprechpartner_options:
                        default_index = ansprechpartner_options.index(current_ansprechpartner)
                    
                    # Ansprechpartner auswählen
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        selected_ansprechpartner = st.selectbox(
                            "Ansprechpartner",
                            options=ansprechpartner_options,
                            index=default_index,
                            key="ansprechpartner"
                        )
                        edited_data["ansprechpartner"] = selected_ansprechpartner
                        
                        # E-Mail-Adresse und Telefon basierend auf dem ausgewählten Ansprechpartner
                        email = ""
                        telefon = ""
                        
                        if selected_ansprechpartner != "Kein Ansprechpartner":
                            # Suche den ausgewählten Ansprechpartner in der Liste
                            for contact in company_contacts:
                                if contact["name"] == selected_ansprechpartner:
                                    email = contact["email"]
                                    telefon = contact["phone"]
                                    break
                        
                        edited_data["email"] = email
                    
                    with col2:
                        # Telefonnummer anzeigen
                        edited_data["telefon"] = st.text_input("Telefon", value=telefon, disabled=True)
                    
                    with col3:
                        # E-Mail-Adresse anzeigen
                        st.text_input("E-Mail", value=email, disabled=True)
                    
                    # CV-Daten-Editor
                    
                    # Bereite die Daten vor
                    cv_data = {
                        'berufserfahrung': profile_data.get("berufserfahrung", []),
                        'ausbildung': profile_data.get("ausbildung", []),
                        'weiterbildungen': profile_data.get("weiterbildungen", [])
                    }
                    
                    # Dropdown-basierter CV-Editor
                    edited_cv_data = create_cv_data_editor(cv_data)
                    
                    # Aktualisierte Daten aus Session State verwenden (für persistente Sortierung)
                    all_experience = st.session_state.get('cv_berufserfahrung', [])
                    all_education = st.session_state.get('cv_ausbildung', [])
                    all_training = st.session_state.get('cv_weiterbildungen', [])
                    
                    # Zusammenführen der bearbeiteten Daten
                    complete_edited_data = {
                        "persönliche_daten": {
                            "name": edited_data.get("name", ""),
                            "wohnort": edited_data.get("wohnort", ""),
                            "jahrgang": edited_data.get("jahrgang", ""),
                            "führerschein": edited_data.get("führerschein", ""),
                            "kontakt": {
                                "ansprechpartner": edited_data.get("ansprechpartner", ""),
                                "telefon": edited_data.get("telefon", ""),
                                "email": edited_data.get("email", "")
                            },
                            "profile_image": st.session_state.get("profile_image_path", None)
                        },
                        "berufserfahrung": all_experience,
                        "ausbildung": all_education,
                        "weiterbildungen": all_training,
                        "wunschgehalt": edited_data.get("wunschgehalt", ""),
                        "verfuegbarkeit_status": edited_data.get("verfuegbarkeit_status", "Sofort verfügbar"),
                        "verfuegbarkeit_details": edited_data.get("verfuegbarkeit_details", "")
                    }
                    
                    # Speichern der bearbeiteten Daten in der Session
                    st.session_state.edited_data = complete_edited_data
                    
                    # Prüfen auf Vollständigkeit der kritischen Daten
                    validation_errors = []
                    if not edited_data.get("name"):
                        validation_errors.append("Name fehlt")
                    if not edited_data.get("email") and not edited_data.get("telefon"):
                        validation_errors.append("Mindestens eine Kontaktmöglichkeit (E-Mail oder Telefon) wird benötigt")
                    
                    # Wenn es Validierungsfehler gibt, diese anzeigen
                    if validation_errors:
                        for error in validation_errors:
                            st.error(error)
                
                with tab2:
                    # Profil generieren und Vorschau anzeigen
                    st.markdown("### Profilvorschau und Export")
                    
                    # Zuerst prüfen, ob edited_data in der Session verfügbar ist und wenn nicht, initialisieren
                    if "edited_data" not in st.session_state:
                        # Vorbereitete Daten für Tab2 erstellen
                        complete_edited_data = {
                            "persönliche_daten": {
                                "name": profile_data.get("persönliche_daten", {}).get("name", ""),
                                "wohnort": profile_data.get("persönliche_daten", {}).get("wohnort", ""),
                                "jahrgang": profile_data.get("persönliche_daten", {}).get("jahrgang", ""),
                                "führerschein": profile_data.get("persönliche_daten", {}).get("führerschein", ""),
                                "kontakt": profile_data.get("persönliche_daten", {}).get("kontakt", {})
                            },
                            "berufserfahrung": profile_data.get("berufserfahrung", []),
                            "ausbildung": profile_data.get("ausbildung", []),
                            "weiterbildungen": profile_data.get("weiterbildungen", []),
                            "wunschgehalt": profile_data.get("wunschgehalt", "")
                        }
                        # In Session State speichern
                        st.session_state.edited_data = complete_edited_data
                    
                    # Profildaten aus der Session holen und mit aktuellen CV-Daten aktualisieren
                    try:
                        edited_data_to_use = st.session_state.edited_data.copy()
                        
                        # Sicherstellen, dass die aktuellsten CV-Daten aus Session State verwendet werden
                        edited_data_to_use["berufserfahrung"] = st.session_state.get('cv_berufserfahrung', [])
                        edited_data_to_use["ausbildung"] = st.session_state.get('cv_ausbildung', [])
                        edited_data_to_use["weiterbildungen"] = st.session_state.get('cv_weiterbildungen', [])
                        
                        # Sicherstellen, dass es ein Dictionary ist
                        if not isinstance(edited_data_to_use, dict):
                            edited_data_to_use = {
                                "persönliche_daten": profile_data.get("persönliche_daten", {}),
                                "berufserfahrung": st.session_state.get('cv_berufserfahrung', []),
                                "ausbildung": st.session_state.get('cv_ausbildung', []),
                                "weiterbildungen": st.session_state.get('cv_weiterbildungen', []),
                                "wunschgehalt": profile_data.get("wunschgehalt", "")
                            }
                    except Exception as e:
                        print(f"Fehler beim Laden der bearbeiteten Daten: {e}")
                        # Fallback auf ursprüngliche Daten mit Session State CV-Daten
                        edited_data_to_use = {
                            "persönliche_daten": profile_data.get("persönliche_daten", {}),
                            "berufserfahrung": st.session_state.get('cv_berufserfahrung', profile_data.get("berufserfahrung", [])),
                            "ausbildung": st.session_state.get('cv_ausbildung', profile_data.get("ausbildung", [])),
                            "weiterbildungen": st.session_state.get('cv_weiterbildungen', profile_data.get("weiterbildungen", [])),
                            "wunschgehalt": profile_data.get("wunschgehalt", "")
                        }
                    
                    # Vorlage auswählen
                    st.markdown("#### Vorlage auswählen")
                    
                    # Standard-Vorlage aus der Konfiguration holen
                    default_template = config.get_all_settings().get("default_template", "professional")
                    
                    # Template-Auswahl als Variable speichern
                    template_to_use = default_template
                    
                    # Nur Classic Template verfügbar
                    template_to_use = "classic"
                    st.info("📄 Klassisches Template wird verwendet")
                            
                    # Profil-Vorschau generieren und anzeigen
                    if 'preview_pdf' not in st.session_state or st.button("Vorschau aktualisieren") or st.session_state.get('update_preview', False):
                        # Reset des Update-Flags
                        st.session_state.update_preview = False
                        with st.spinner("Profil wird generiert..."):
                            try:
                                # Verwende das ausgewählte Unternehmen für den Generator
                                selected_company = st.session_state.get('selected_company', 'galdora')
                                generator = ProfileGenerator(selected_company=selected_company)
                                output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                                output_path = output_file.name
                                output_file.close()
                                st.session_state.temp_files.append(output_path)
                                
                                # Generiere Profil mit dem ausgewählten Template
                                profile_path = generator.generate_profile(edited_data_to_use, output_path, template=template_to_use)
                                st.session_state.preview_pdf = profile_path
                                
                                # Zeige eine Erfolgsmeldung an
                                st.success("Profil erfolgreich generiert!")
                                
                                # Speichere das ausgewählte Template für zukünftige Aktualisierungen
                                st.session_state.selected_template = template_to_use
                            except Exception as e:
                                st.error(f"Fehler bei der Generierung des Profils: {str(e)}")
                    
                    # PDF-Vorschau anzeigen mit PDF.js
                    if st.session_state.preview_pdf:
                        st.markdown("#### 📄 Profil-Vorschau")
                        # Prüfen ob die Datei existiert, bevor wir versuchen sie anzuzeigen
                        if st.session_state.preview_pdf and os.path.exists(st.session_state.preview_pdf):
                            
                            try:
                                # Verwende die A4-optimierte PDF.js-basierte Vorschau
                                st.markdown("**📄 A4-Format Vorschau** (mit Navigation und Zoom):")
                                display_pdf_with_pdfjs(st.session_state.preview_pdf)
                                
                                # Zusätzlicher Download-Button für direkten Zugriff
                                with open(st.session_state.preview_pdf, "rb") as pdf_file:
                                    pdf_bytes = pdf_file.read()
                                # Name für die Vorschau-Datei
                                try:
                                    if isinstance(edited_data_to_use, dict) and "persönliche_daten" in edited_data_to_use:
                                        personal_data_name = edited_data_to_use["persönliche_daten"]
                                        if isinstance(personal_data_name, dict) and "name" in personal_data_name:
                                            preview_name = str(personal_data_name["name"]).replace(" ", "-")
                                        else:
                                            preview_name = "Unbekannt"
                                    else:
                                        preview_name = "Unbekannt"
                                    
                                    if not preview_name or preview_name == "" or preview_name == "-":
                                        preview_name = "Unbekannt"
                                except Exception as e:
                                    preview_name = "Unbekannt"
                                
                                st.download_button(
                                    label="📥 PDF herunterladen",
                                    data=pdf_bytes,
                                    file_name=f"Profilvorlage-{preview_name}.pdf",
                                    mime="application/pdf",
                                    help="Laden Sie das PDF direkt herunter",
                                    use_container_width=True
                                )
                                
                            except Exception as e:
                                st.error(f"Fehler bei der PDF-Anzeige: {str(e)}")
                        else:
                            st.error("Die PDF-Vorschau ist nicht verfügbar. Bitte generieren Sie die Vorschau erneut.")
                        
                        # Name für das Profil
                        try:
                            if isinstance(edited_data_to_use, dict) and "persönliche_daten" in edited_data_to_use:
                                personal_data_name = edited_data_to_use["persönliche_daten"]
                                if isinstance(personal_data_name, dict) and "name" in personal_data_name:
                                    name = str(personal_data_name["name"]).replace(" ", "-")
                                else:
                                    name = "Unbekannt"
                            else:
                                name = "Unbekannt"
                            
                            if not name or name == "" or name == "-":
                                name = "Unbekannt"
                        except Exception as e:
                            print(f"Fehler beim Laden des Namens: {e}")
                            name = "Unbekannt"
                        
                        # Auswahl des Formats mit RadioButtons
                        st.markdown("#### Format wählen")
                        format_option = st.radio(
                            "In welchem Format möchten Sie das Profil herunterladen?",
                            options=["PDF", "Word"],
                            horizontal=True,
                            key="format_choice"
                        )
                        
                        # Je nach Auswahl unterschiedlichen Download-Button anzeigen
                        if format_option == "PDF":
                            # PDF-Download
                            if st.session_state.preview_pdf and os.path.exists(st.session_state.preview_pdf):
                                with open(st.session_state.preview_pdf, "rb") as file:
                                    st.download_button(
                                        label="Profil herunterladen",
                                        data=file,
                                        file_name=f"Profilvorlage-{name}.pdf",
                                        mime="application/pdf",
                                        key="download_pdf"
                                    )
                            else:
                                st.error("Bitte generieren Sie zuerst eine Vorschau des Profils.")
                        else:
                            # Word-Dokument generieren und herunterladen
                            # Temporäre Datei für das Word-Dokument erstellen
                            output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
                            output_path = output_file.name
                            output_file.close()
                            st.session_state.temp_files.append(output_path)
                            
                            try:
                                # Stelle sicher, dass generator definiert ist mit der richtigen Unternehmens-Auswahl
                                selected_company = st.session_state.get('selected_company', 'galdora')
                                generator = ProfileGenerator(selected_company=selected_company)
                                
                                # Stelle sicher, dass template_to_use definiert ist
                                template_to_use = st.session_state.get('selected_template', 'classic')
                                
                                # Word-Dokument mit dem gleichen Generator erstellen
                                docx_path = generator.generate_profile(
                                    edited_data_to_use, 
                                    output_path, 
                                    template=template_to_use,
                                    format="docx"
                                )
                                
                                # Word-Dokument zum Download anbieten
                                with open(docx_path, "rb") as file:
                                    st.download_button(
                                        label="Profil herunterladen",
                                        data=file,
                                        file_name=f"Profilvorlage-{name}.docx",
                                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                        key="download_word"
                                    )
                            except Exception as e:
                                st.error(f"Fehler bei der Word-Dokument-Generierung: {str(e)}")
                
    elif uploaded_file and not openai_api_key:
        st.warning("Bitte gib einen OpenAI API Key in der Seitenleiste ein, um fortzufahren.")



# Footer
st.divider()
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center;">
    <span>CV2Profile Konverter | Alle Rechte vorbehalten © 2025</span>
    <div>
        <a href="#" style="margin-right: 10px;">Datenschutz</a>
        <a href="#" style="margin-right: 10px;">AGB</a>
        <a href="#">Impressum</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Aufräumen von temporären Dateien, wenn das Programm beendet wird
def cleanup():
    """Räumt temporäre Dateien auf, wenn die App beendet wird"""
    try:
        # Überprüfe, ob temp_files in der Session existiert, bevor darauf zugegriffen wird
        if hasattr(st, 'session_state') and 'temp_files' in st.session_state:
            for temp_file in st.session_state.temp_files:
                try:
                    if os.path.exists(temp_file):
                        os.unlink(temp_file)
                        print(f"Temporäre Datei gelöscht: {temp_file}")
                except Exception as e:
                    print(f"Fehler beim Löschen der temporären Datei {temp_file}: {str(e)}")
    except Exception as e:
        print(f"Fehler beim Aufräumen: {str(e)}")
    finally:
        # Sicherstellen, dass keine Fehler unbehandelt bleiben
        print("Cleanup abgeschlossen.")

# Cleanup-Funktion registrieren
atexit.register(cleanup)

st.markdown("""
<meta name="description" content="CV2Profile: Professioneller Lebenslauf-Konverter für automatische PDF-Erstellung. GALDORA Personalmanagement.">
""", unsafe_allow_html=True)


