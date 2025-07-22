"""
Wiederverwendbare CV-Editor-Komponenten
"""
import streamlit as st
from typing import Dict, List, Any, Optional
from utils.session_manager import SessionManager
from utils.error_handler import safe_streamlit_component, log_info

class CVEditorComponents:
    """Sammlung von wiederverwendbaren CV-Editor-Komponenten"""
    
    @staticmethod
    @safe_streamlit_component("Personal Data Editor")
    def render_personal_data_editor(profile_data: Dict) -> Dict[str, Any]:
        """
        Rendert den Editor für persönliche Daten
        
        Args:
            profile_data: Bestehende Profildaten
            
        Returns:
            Dict mit bearbeiteten persönlichen Daten
        """
        st.markdown("### 👤 Persönliche Daten")
        
        personal_data = profile_data.get("persönliche_daten", {})
        edited_data = {}
        
        # Name und Grunddaten
        col1, col2, col3 = st.columns(3)
        with col1:
            edited_data["name"] = st.text_input(
                "Name", 
                value=personal_data.get("name", ""),
                help="Vollständiger Name"
            )
        with col2:
            edited_data["wohnort"] = st.text_input(
                "Wohnort", 
                value=personal_data.get("wohnort", ""),
                help="Stadt/PLZ"
            )
        with col3:
            edited_data["jahrgang"] = st.text_input(
                "Jahrgang", 
                value=personal_data.get("jahrgang", ""),
                help="Geburtsjahr"
            )
        
        return edited_data
    
    @staticmethod
    @safe_streamlit_component("Contact Info Editor")
    def render_contact_editor() -> Dict[str, str]:
        """Rendert den Kontakt-Editor mit Ansprechpartner-Auswahl"""
        st.markdown("### 📞 Kontaktinformationen")
        
        # Ansprechpartner-Konfiguration
        ansprechpartner_config = {
            "Kai Fischer": {"email": "fischer@galdora.de", "telefon": "02161 62126-02"},
            "Melike Demirkol": {"email": "demirkol@galdora.de", "telefon": "02161 62126-02"},
            "Konrad Ruszczyk": {"email": "konrad@galdora.de", "telefon": "02161 62126-02"},
            "Alessandro Böhm": {"email": "boehm@galdora.de", "telefon": "02161 62126-02"},
            "Salim Alizai": {"email": "gl@galdora.de", "telefon": "+49 177 7089045"},
            "Kein Ansprechpartner": {"email": "", "telefon": ""}
        }
        
        col1, col2, col3 = st.columns(3)
        with col1:
            selected_ansprechpartner = st.selectbox(
                "Ansprechpartner",
                options=list(ansprechpartner_config.keys()),
                key="ansprechpartner_select"
            )
        
        # Automatische Kontaktdaten basierend auf Auswahl
        contact_info = ansprechpartner_config[selected_ansprechpartner]
        
        with col2:
            st.text_input(
                "Telefon", 
                value=contact_info["telefon"], 
                disabled=True,
                help="Automatisch basierend auf Ansprechpartner"
            )
        with col3:
            st.text_input(
                "E-Mail", 
                value=contact_info["email"], 
                disabled=True,
                help="Automatisch basierend auf Ansprechpartner"
            )
        
        return {
            "ansprechpartner": selected_ansprechpartner,
            "telefon": contact_info["telefon"],
            "email": contact_info["email"]
        }
    
    @staticmethod
    @safe_streamlit_component("CV Section Editor")
    def render_cv_section_editor(
        section_name: str,
        session_key: str, 
        fields_config: Dict[str, Dict],
        icon: str = "📋"
    ) -> List[Dict]:
        """
        Generischer CV-Abschnitt-Editor
        
        Args:
            section_name: Name der Sektion (z.B. "Berufserfahrung")
            session_key: Session State Key
            fields_config: Konfiguration der Felder
            icon: Icon für den Abschnitt
            
        Returns:
            Liste der bearbeiteten Einträge
        """
        st.markdown(f"### {icon} {section_name}")
        
        # Session State initialisieren
        if session_key not in st.session_state:
            st.session_state[session_key] = []
        
        # Hinzufügen-Button
        if st.button(f"➕ Neue {section_name} hinzufügen", key=f"add_{session_key}"):
            default_entry = {field: "" for field in fields_config.keys()}
            st.session_state[session_key].append(default_entry)
            st.rerun()
        
        # Einträge anzeigen
        entries = st.session_state[session_key]
        if not entries:
            st.info(f"Keine {section_name} vorhanden. Klicken Sie auf '➕' um einen Eintrag hinzuzufügen.")
            return []
        
        for i, entry in enumerate(entries):
            with st.container():
                # Navigation und Inhalt
                col_nav, col_content = st.columns([1, 9])
                
                with col_nav:
                    CVEditorComponents._render_navigation_buttons(session_key, i, len(entries))
                
                with col_content:
                    CVEditorComponents._render_entry_fields(entry, fields_config, i, session_key)
                
                st.divider()
        
        return entries
    
    @staticmethod
    def _render_navigation_buttons(session_key: str, index: int, total_entries: int):
        """Rendert Navigation-Buttons für CV-Einträge"""
        # Nach oben
        if st.button("⬆️", key=f"{session_key}_up_{index}", 
                    disabled=(index == 0), 
                    help="Nach oben verschieben", 
                    use_container_width=True):
            CVEditorComponents._move_entry(session_key, index, -1)
            st.rerun()
        
        # Nach unten
        if st.button("⬇️", key=f"{session_key}_down_{index}", 
                    disabled=(index == total_entries - 1), 
                    help="Nach unten verschieben", 
                    use_container_width=True):
            CVEditorComponents._move_entry(session_key, index, 1)
            st.rerun()
        
        # Löschen
        if st.button("🗑️", key=f"{session_key}_delete_{index}", 
                    help="Eintrag löschen", 
                    use_container_width=True):
            st.session_state[session_key].pop(index)
            st.rerun()
    
    @staticmethod
    def _render_entry_fields(entry: Dict, fields_config: Dict, index: int, session_key: str):
        """Rendert die Eingabefelder für einen CV-Eintrag"""
        # Felder in Spalten anordnen
        field_items = list(fields_config.items())
        
        # Zwei-Spalten-Layout für die meisten Felder
        if len(field_items) >= 2:
            col1, col2 = st.columns(2)
            columns = [col1, col2]
        else:
            columns = [st.container()]
        
        for i, (field_key, field_config) in enumerate(field_items):
            col = columns[i % len(columns)]
            
            with col:
                field_type = field_config.get("type", "text")
                label = field_config.get("label", field_key.title())
                help_text = field_config.get("help", "")
                
                if field_type == "textarea":
                    new_value = st.text_area(
                        label,
                        value=entry.get(field_key, ""),
                        key=f"{session_key}_{field_key}_{index}",
                        help=help_text
                    )
                elif field_type == "list":
                    # Für Listen (z.B. Aufgaben)
                    current_list = entry.get(field_key, [])
                    if isinstance(current_list, list):
                        list_text = '\n'.join(current_list)
                    else:
                        list_text = str(current_list)
                    
                    new_text = st.text_area(
                        label,
                        value=list_text,
                        key=f"{session_key}_{field_key}_{index}",
                        help=help_text
                    )
                    new_value = [item.strip() for item in new_text.split('\n') if item.strip()]
                else:
                    new_value = st.text_input(
                        label,
                        value=entry.get(field_key, ""),
                        key=f"{session_key}_{field_key}_{index}",
                        help=help_text
                    )
                
                entry[field_key] = new_value
    
    @staticmethod
    def _move_entry(session_key: str, index: int, direction: int):
        """Verschiebt einen Eintrag in der Liste"""
        entries = st.session_state[session_key]
        new_index = index + direction
        
        if 0 <= new_index < len(entries):
            entries[index], entries[new_index] = entries[new_index], entries[index]
            log_info(f"Eintrag in {session_key} verschoben: {index} -> {new_index}")

# Vordefinierte Feld-Konfigurationen
CV_FIELD_CONFIGS = {
    "berufserfahrung": {
        "zeitraum": {"label": "Zeitraum", "help": "z.B. 01/2020 - 12/2022"},
        "unternehmen": {"label": "Unternehmen", "help": "Firmenname"},
        "position": {"label": "Position", "help": "Jobtitel"},
        "aufgaben": {"label": "Aufgaben", "type": "list", "help": "Eine Aufgabe pro Zeile"}
    },
    "ausbildung": {
        "zeitraum": {"label": "Zeitraum", "help": "z.B. 09/2018 - 07/2021"},
        "institution": {"label": "Institution", "help": "Schule/Universität"},
        "abschluss": {"label": "Abschluss", "help": "Art des Abschlusses"},
        "note": {"label": "Note", "help": "Optional"},
        "schwerpunkte": {"label": "Schwerpunkte", "type": "textarea", "help": "Optional"}
    },
    "weiterbildungen": {
        "zeitraum": {"label": "Zeitraum", "help": "z.B. 03/2023"},
        "bezeichnung": {"label": "Bezeichnung", "help": "Name der Weiterbildung"},
        "abschluss": {"label": "Abschluss/Details", "help": "Zertifikat oder Details"}
    }
} 