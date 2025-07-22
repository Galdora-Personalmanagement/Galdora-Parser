"""
UI-Hilfsfunktionen für die CV2Profile-Anwendung.

Diese Datei enthält gemeinsame Funktionen, die in der gesamten UI verwendet werden.
Die Funktionen wurden aus app.py und 01_Konverter.py extrahiert, um Redundanz zu vermeiden.
"""

import streamlit as st
import os
import tempfile
import json
import base64
from PIL import Image
import io
import pandas as pd
import re
from pathlib import Path
from datetime import datetime
import atexit

# Stellen Sie sicher, dass alle erforderlichen Importe vorhanden sind
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Importe aus den reorganisierten Modulen
from src.utils.image_utils import get_image_path, ensure_images_in_static

def get_logo_as_base64():
    """
    Lädt das Logo und konvertiert es in base64 für die Einbettung in HTML.
    
    Returns:
        str: Base64-kodiertes Logo oder leerer String bei Fehler
    """
    try:
        # Stellt sicher, dass alle Bilder im static-Verzeichnis für HTTPS-Kompatibilität verfügbar sind
        ensure_images_in_static()
        
        # Versuche, das Logo mit unserer Bild-Utility zu finden
        # Für HTTPS-Kompatibilität use_static=True
        logo_path = get_image_path('cv2profile-loho.png', use_static=True)
        
        # Fallback-Speicherorte, wenn der erste Pfad nicht existiert
        if not os.path.exists(logo_path):
            logo_path = get_image_path('Galdoralogo.png', use_static=True)
        
        if not os.path.exists(logo_path):
            # Letzter Ausweg: Leeren String zurückgeben, wenn kein Logo gefunden wird
            return ""
        
        with open(logo_path, "rb") as f:
            logo_data = f.read()
            return base64.b64encode(logo_data).decode("utf-8")
    except Exception as e:
        print(f"Fehler beim Laden des Logos: {e}")
        return ""

def reset_session():
    """
    Setzt die Streamlit-Sitzung zurück und entfernt temporäre Dateien.
    """
    if "uploaded_file" in st.session_state:
        st.session_state.pop("uploaded_file")
    
    if "extracted_text" in st.session_state:
        st.session_state.pop("extracted_text")
    
    if "profile_data" in st.session_state:
        st.session_state.pop("profile_data")
    
    if "generated_pdf" in st.session_state:
        st.session_state.pop("generated_pdf")
    
    if "preview_pdf" in st.session_state:
        st.session_state.pop("preview_pdf")
    
    # Temporäre Dateien entfernen
    if "temp_dir" in st.session_state and os.path.exists(st.session_state.temp_dir):
        try:
            for file in os.listdir(st.session_state.temp_dir):
                os.remove(os.path.join(st.session_state.temp_dir, file))
        except Exception as e:
            print(f"Fehler beim Entfernen temporärer Dateien: {e}")

def display_pdf(file_path):
    """
    Zeigt ein PDF-Dokument in der Streamlit-App an.
    
    Args:
        file_path: Pfad zur PDF-Datei
    
    Returns:
        HTML-Komponente, die das PDF anzeigt
    """
    try:
        # Öffne die PDF-Datei in Binärmode
        with open(file_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        
        # Erstelle HTML-Einbettung mit Bootstrap-Styling
        pdf_display = f"""
        <div style="display: flex; justify-content: center; width: 100%;">
            <iframe 
                src="data:application/pdf;base64,{base64_pdf}" 
                width="100%" 
                height="800px" 
                style="border: none; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);" 
                allowfullscreen>
            </iframe>
        </div>
        """
        return st.markdown(pdf_display, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Fehler beim Anzeigen des PDFs: {str(e)}")
        return None

def create_temp_directory():
    """
    Erstellt ein temporäres Verzeichnis für die Anwendung und speichert es in der Sitzung.
    
    Returns:
        str: Pfad zum temporären Verzeichnis
    """
    if "temp_dir" not in st.session_state:
        st.session_state.temp_dir = tempfile.mkdtemp()
    
    return st.session_state.temp_dir

def create_experience_editor(profile_data, key_prefix="berufserfahrung"):
    """
    Erstellt einen Editor für Berufserfahrung mit Drag & Drop-Funktionalität.
    
    Args:
        profile_data: Die Profildaten mit Berufserfahrungen
        key_prefix: Präfix für die Streamlit-Keys
    
    Returns:
        dict: Aktualisierte Profildaten
    """
    if "berufserfahrung" not in profile_data or not profile_data["berufserfahrung"]:
        profile_data["berufserfahrung"] = []
        return profile_data
    
    # Stelle sicher, dass session_state Indizes für diese Berufserfahrungen hat
    if f"{key_prefix}_indices" not in st.session_state:
        st.session_state[f"{key_prefix}_indices"] = list(range(len(profile_data["berufserfahrung"])))
    
    # Bei Änderungen in der Länge, aktualisiere die Indizes
    if len(st.session_state[f"{key_prefix}_indices"]) != len(profile_data["berufserfahrung"]):
        st.session_state[f"{key_prefix}_indices"] = list(range(len(profile_data["berufserfahrung"])))
    
    # Ausgabe der Berufserfahrungen in der Reihenfolge der session_state Indizes
    for i, idx in enumerate(st.session_state[f"{key_prefix}_indices"]):
        if idx < len(profile_data["berufserfahrung"]):
            erfahrung = profile_data["berufserfahrung"][idx]
            
            col1, col2, col3 = st.columns([0.15, 0.7, 0.15])
            
            # Auf/Ab-Buttons für Drag & Drop
            with col1:
                # Aufwärts-Button (deaktiviert für den ersten Eintrag)
                if i > 0:
                    if st.button(f"↑", key=f"{key_prefix}_up_{i}"):
                        # Tausche mit dem vorherigen Element
                        st.session_state[f"{key_prefix}_indices"][i], st.session_state[f"{key_prefix}_indices"][i-1] = \
                        st.session_state[f"{key_prefix}_indices"][i-1], st.session_state[f"{key_prefix}_indices"][i]
                        st.rerun()
                else:
                    st.write("")  # Platzhalter
                
                # Abwärts-Button (deaktiviert für den letzten Eintrag)
                if i < len(st.session_state[f"{key_prefix}_indices"]) - 1:
                    if st.button(f"↓", key=f"{key_prefix}_down_{i}"):
                        # Tausche mit dem nächsten Element
                        st.session_state[f"{key_prefix}_indices"][i], st.session_state[f"{key_prefix}_indices"][i+1] = \
                        st.session_state[f"{key_prefix}_indices"][i+1], st.session_state[f"{key_prefix}_indices"][i]
                        st.rerun()
                else:
                    st.write("")  # Platzhalter
            
            # Informationen anzeigen
            with col2:
                st.markdown(f"**{erfahrung.get('position', '')}** bei {erfahrung.get('unternehmen', '')}")
                st.markdown(f"*{erfahrung.get('zeitraum', '')}*")
                
                # Aufgaben als Liste anzeigen
                aufgaben = erfahrung.get('aufgaben', [])
                if aufgaben:
                    aufgaben_text = "\n".join([f"- {aufgabe}" for aufgabe in aufgaben])
                    st.markdown(aufgaben_text)
            
            # Bearbeitungs-Button
            with col3:
                if st.button("✏️", key=f"{key_prefix}_edit_{i}"):
                    st.session_state[f"{key_prefix}_edit_idx"] = idx
                    st.rerun()
            
            st.markdown("---")
    
    # Editor für ausgewählte Berufserfahrung
    if f"{key_prefix}_edit_idx" in st.session_state:
        edit_idx = st.session_state[f"{key_prefix}_edit_idx"]
        if edit_idx < len(profile_data["berufserfahrung"]):
            erfahrung = profile_data["berufserfahrung"][edit_idx]
            
            st.subheader("Berufserfahrung bearbeiten")
            
            # Formularfelder für die Bearbeitung
            position = st.text_input("Position", erfahrung.get("position", ""))
            unternehmen = st.text_input("Unternehmen", erfahrung.get("unternehmen", ""))
            zeitraum = st.text_input("Zeitraum", erfahrung.get("zeitraum", ""))
            
            # Aufgaben als Textfeld mit mehreren Zeilen
            aufgaben_text = "\n".join(erfahrung.get("aufgaben", []))
            aufgaben_neu = st.text_area("Aufgaben (eine pro Zeile)", aufgaben_text)
            aufgaben_liste = [aufgabe.strip() for aufgabe in aufgaben_neu.split('\n') if aufgabe.strip()]
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Speichern", key=f"{key_prefix}_save"):
                    profile_data["berufserfahrung"][edit_idx] = {
                        "position": position,
                        "unternehmen": unternehmen,
                        "zeitraum": zeitraum,
                        "aufgaben": aufgaben_liste
                    }
                    # Editor schließen
                    st.session_state.pop(f"{key_prefix}_edit_idx", None)
                    st.rerun()
            
            with col2:
                if st.button("Abbrechen", key=f"{key_prefix}_cancel"):
                    # Editor schließen ohne zu speichern
                    st.session_state.pop(f"{key_prefix}_edit_idx", None)
                    st.rerun()
    
    return profile_data

def reorder_profile_data(profile_data):
    """
    Ordnet die Profildaten gemäß der in der Session gespeicherten Reihenfolge neu an.
    
    Args:
        profile_data: Die ursprünglichen Profildaten
        
    Returns:
        dict: Neu geordnete Profildaten
    """
    # Kopie der Profildaten erstellen
    reordered_data = profile_data.copy()
    
    # Berufserfahrung neu ordnen
    if "berufserfahrung_indices" in st.session_state and "berufserfahrung" in profile_data:
        berufserfahrung = []
        for idx in st.session_state["berufserfahrung_indices"]:
            if idx < len(profile_data["berufserfahrung"]):
                berufserfahrung.append(profile_data["berufserfahrung"][idx])
        reordered_data["berufserfahrung"] = berufserfahrung
    
    # Ausbildung neu ordnen
    if "ausbildung_indices" in st.session_state and "ausbildung" in profile_data:
        ausbildung = []
        for idx in st.session_state["ausbildung_indices"]:
            if idx < len(profile_data["ausbildung"]):
                ausbildung.append(profile_data["ausbildung"][idx])
        reordered_data["ausbildung"] = ausbildung
    
    # Weiterbildungen neu ordnen
    if "weiterbildungen_indices" in st.session_state and "weiterbildungen" in profile_data:
        weiterbildungen = []
        for idx in st.session_state["weiterbildungen_indices"]:
            if idx < len(profile_data["weiterbildungen"]):
                weiterbildungen.append(profile_data["weiterbildungen"][idx])
        reordered_data["weiterbildungen"] = weiterbildungen
    
    return reordered_data

def cleanup():
    """
    Bereinigungsfunktion, die beim Beenden der Anwendung aufgerufen wird.
    Entfernt temporäre Dateien und Verzeichnisse.
    """
    if "temp_dir" in st.session_state and os.path.exists(st.session_state.temp_dir):
        try:
            for file in os.listdir(st.session_state.temp_dir):
                os.remove(os.path.join(st.session_state.temp_dir, file))
            os.rmdir(st.session_state.temp_dir)
        except Exception as e:
            print(f"Fehler beim Bereinigen temporärer Dateien: {e}")

# Registriere die Cleanup-Funktion, um beim Beenden der Anwendung aufgerufen zu werden
atexit.register(cleanup) 