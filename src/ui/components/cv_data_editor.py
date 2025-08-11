"""
CV Data Editor Component
Extracted from main.py to improve maintainability and reduce code complexity.
Handles the editing interface for CV data with drag-and-drop reordering.
"""

import streamlit as st
from typing import Dict, List, Any
from src.core.config_manager import ValidationRules, CompanyContactConfig


class CVDataEditor:
    """Handles CV data editing UI components with session state management"""
    
    def __init__(self):
        self.validation_rules = ValidationRules()
        self.company_contacts = CompanyContactConfig()
    
    def initialize_session_state(self, profile_data: Dict[str, Any]) -> None:
        """Initialize session state for CV data if not already present"""
        if 'cv_berufserfahrung' not in st.session_state:
            st.session_state.cv_berufserfahrung = profile_data.get("berufserfahrung", [])
        if 'cv_ausbildung' not in st.session_state:
            st.session_state.cv_ausbildung = profile_data.get("ausbildung", [])
        if 'cv_weiterbildungen' not in st.session_state:
            st.session_state.cv_weiterbildungen = profile_data.get("weiterbildungen", [])
    
    def render_personal_data_section(self, profile_data: Dict[str, Any], key_prefix: str = "") -> Dict[str, Any]:
        """Render the personal data editing section"""
        st.markdown("### Persönliche Daten")
        personal_data = profile_data.get("persönliche_daten", {})
        edited_data = {}
        
        # Name and basic data
        col1, col2, col3 = st.columns(3)
        with col1:
            edited_data["name"] = st.text_input(
                "Name", 
                value=personal_data.get("name", ""), 
                key=f"{key_prefix}name"
            )
        with col2:
            edited_data["wohnort"] = st.text_input(
                "Wohnort", 
                value=personal_data.get("wohnort", ""), 
                key=f"{key_prefix}wohnort"
            )
        with col3:
            edited_data["jahrgang"] = st.text_input(
                "Jahrgang", 
                value=personal_data.get("jahrgang", ""), 
                key=f"{key_prefix}jahrgang"
            )
        
        # Driver's license and salary expectations
        col1, col2 = st.columns(2)
        with col1:
            edited_data["führerschein"] = self._render_fuehrerschein_selector(
                personal_data, key_prefix
            )
        with col2:
            edited_data["wunschgehalt"] = st.text_input(
                "Wunschgehalt", 
                value=profile_data.get("wunschgehalt", ""), 
                key=f"{key_prefix}wunschgehalt"
            )
        
        return edited_data
    
    def render_availability_section(self, key_prefix: str = "") -> Dict[str, Any]:
        """Render the availability editing section"""
        st.markdown("### Verfügbarkeit")
        
        col1, col2 = st.columns(2)
        availability_data = {}
        
        with col1:
            verfuegbarkeit_status = st.selectbox(
                "Verfügbarkeitsstatus",
                options=self.validation_rules.VERFUEGBARKEIT_OPTIONS,
                index=0,
                key=f"{key_prefix}verfuegbarkeit_status"
            )
            availability_data["verfuegbarkeit_status"] = verfuegbarkeit_status
        
        with col2:
            if verfuegbarkeit_status == "Verfügbar ab bestimmtem Datum":
                verfuegbarkeit_datum = st.date_input(
                    "Verfügbar ab",
                    value=None,
                    key=f"{key_prefix}verfuegbarkeit_datum"
                )
                if verfuegbarkeit_datum:
                    availability_data["verfuegbarkeit_details"] = f"Verfügbar ab {verfuegbarkeit_datum.strftime('%d.%m.%Y')}"
                else:
                    availability_data["verfuegbarkeit_details"] = ""
            else:
                availability_data["verfuegbarkeit_details"] = ""
        
        return availability_data
    
    def render_contact_section(self, personal_data: Dict[str, Any], key_prefix: str = "") -> Dict[str, Any]:
        """Render the contact information section"""
        st.markdown("### Kontaktinformationen")
        kontakt = personal_data.get("kontakt", {})
        
        # Get company-specific contacts
        company_key = st.session_state.get('selected_company', 'galdora')
        company_contacts = self.company_contacts.get_contacts_for_company(company_key)
        
        # Create contact options
        ansprechpartner_options = ["Kein Ansprechpartner"] + list(company_contacts.keys())
        
        # Pre-select current contact if available
        current_ansprechpartner = kontakt.get("ansprechpartner", "Kein Ansprechpartner")
        default_index = 0
        if current_ansprechpartner in ansprechpartner_options:
            default_index = ansprechpartner_options.index(current_ansprechpartner)
        
        col1, col2, col3 = st.columns(3)
        contact_data = {}
        
        with col1:
            selected_ansprechpartner = st.selectbox(
                "Ansprechpartner",
                options=ansprechpartner_options,
                index=default_index,
                key=f"{key_prefix}ansprechpartner"
            )
            contact_data["ansprechpartner"] = selected_ansprechpartner
        
        # Get contact details based on selection
        email = ""
        telefon = ""
        
        if selected_ansprechpartner != "Kein Ansprechpartner":
            contact_info = self.company_contacts.get_contact_info(company_key, selected_ansprechpartner)
            email = contact_info.get("email", "")
            telefon = contact_info.get("phone", "")
        
        contact_data["email"] = email
        contact_data["telefon"] = telefon
        
        with col2:
            st.text_input("Telefon", value=telefon, disabled=True, key=f"{key_prefix}telefon")
        with col3:
            st.text_input("E-Mail", value=email, disabled=True, key=f"{key_prefix}email")
        
        return contact_data
    
    def render_experience_editor(self) -> None:
        """Render the work experience editor with drag-and-drop functionality"""
        st.markdown("### 🏢 Berufserfahrung")
        
        # Add new entry button
        if st.button("➕ Neue Berufserfahrung hinzufügen", key="add_experience"):
            st.session_state.cv_berufserfahrung.append({
                "zeitraum": "",
                "unternehmen": "",
                "position": "",
                "aufgaben": []
            })
            st.rerun()
        
        # Render all experience entries
        if st.session_state.cv_berufserfahrung:
            self._render_experience_entries()
    
    def render_education_editor(self) -> None:
        """Render the education editor with drag-and-drop functionality"""
        st.markdown("### 🎓 Ausbildung")
        
        # Add new entry button
        if st.button("➕ Neue Ausbildung hinzufügen", key="add_education"):
            st.session_state.cv_ausbildung.append({
                "zeitraum": "",
                "institution": "",
                "abschluss": "",
                "note": "",
                "schwerpunkte": ""
            })
            st.rerun()
        
        # Render all education entries
        if st.session_state.cv_ausbildung:
            self._render_education_entries()
    
    def render_training_editor(self) -> None:
        """Render the training/continuing education editor"""
        st.markdown("### 📚 Weiterbildungen")
        
        # Add new entry button
        if st.button("➕ Neue Weiterbildung hinzufügen", key="add_training"):
            st.session_state.cv_weiterbildungen.append({
                "zeitraum": "",
                "bezeichnung": "",
                "abschluss": ""
            })
            st.rerun()
        
        # Render all training entries
        if st.session_state.cv_weiterbildungen:
            self._render_training_entries()
    
    def get_consolidated_data(self, personal_data: Dict[str, Any], 
                            contact_data: Dict[str, Any], 
                            availability_data: Dict[str, Any]) -> Dict[str, Any]:
        """Consolidate all edited data into a single structure"""
        return {
            "persönliche_daten": {
                "name": personal_data.get("name", ""),
                "wohnort": personal_data.get("wohnort", ""),
                "jahrgang": personal_data.get("jahrgang", ""),
                "führerschein": personal_data.get("führerschein", ""),
                "kontakt": {
                    "ansprechpartner": contact_data.get("ansprechpartner", ""),
                    "telefon": contact_data.get("telefon", ""),
                    "email": contact_data.get("email", "")
                },
                "profile_image": st.session_state.get("profile_image_path", None)
            },
            "berufserfahrung": st.session_state.get('cv_berufserfahrung', []),
            "ausbildung": st.session_state.get('cv_ausbildung', []),
            "weiterbildungen": st.session_state.get('cv_weiterbildungen', []),
            "wunschgehalt": personal_data.get("wunschgehalt", ""),
            "verfuegbarkeit_status": availability_data.get("verfuegbarkeit_status", "Sofort verfügbar"),
            "verfuegbarkeit_details": availability_data.get("verfuegbarkeit_details", "")
        }
    
    def validate_data(self, data: Dict[str, Any]) -> List[str]:
        """Validate the consolidated data and return list of errors"""
        errors = []
        
        # Validate personal data
        personal_errors = self.validation_rules.validate_personal_data(data.get("persönliche_daten", {}))
        errors.extend(personal_errors)
        
        # Validate contact data
        contact_data = data.get("persönliche_daten", {}).get("kontakt", {})
        contact_errors = self.validation_rules.validate_contact_data(contact_data)
        errors.extend(contact_errors)
        
        return errors
    
    # Private helper methods
    def _render_fuehrerschein_selector(self, personal_data: Dict[str, Any], key_prefix: str) -> str:
        """Render driver's license multi-select with smart defaults"""
        current_fuehrerschein = personal_data.get("führerschein", "")
        default_selected = []
        
        # Parse current value and match to options
        if current_fuehrerschein:
            for option in self.validation_rules.FUEHRERSCHEIN_OPTIONS:
                if option in current_fuehrerschein:
                    default_selected.append(option)
            
            # Smart fallback matching
            if not default_selected and "Klasse B" in current_fuehrerschein:
                default_selected.append("Klasse B")
                if "PKW vorhanden" in current_fuehrerschein or "Pkw vorhanden" in current_fuehrerschein:
                    default_selected.append("Klasse B + PKW vorhanden")
        
        selected_fuehrerschein = st.multiselect(
            "Führerschein",
            options=self.validation_rules.FUEHRERSCHEIN_OPTIONS,
            default=default_selected,
            help="Mehrfachauswahl möglich",
            key=f"{key_prefix}fuehrerschein"
        )
        
        return ", ".join(selected_fuehrerschein) if selected_fuehrerschein else ""
    
    def _render_experience_entries(self) -> None:
        """Render all work experience entries with navigation controls"""
        for i, entry in enumerate(st.session_state.cv_berufserfahrung):
            with st.container():
                col_nav, col_content = st.columns([1, 9])
                
                with col_nav:
                    self._render_navigation_buttons("be", i, len(st.session_state.cv_berufserfahrung))
                
                with col_content:
                    self._render_experience_form(entry, i)
                
                st.divider()
    
    def _render_education_entries(self) -> None:
        """Render all education entries with navigation controls"""
        for i, entry in enumerate(st.session_state.cv_ausbildung):
            with st.container():
                col_nav, col_content = st.columns([1, 9])
                
                with col_nav:
                    self._render_navigation_buttons("edu", i, len(st.session_state.cv_ausbildung))
                
                with col_content:
                    self._render_education_form(entry, i)
                
                st.divider()
    
    def _render_training_entries(self) -> None:
        """Render all training entries with navigation controls"""
        for i, entry in enumerate(st.session_state.cv_weiterbildungen):
            with st.container():
                col_nav, col_content = st.columns([1, 9])
                
                with col_nav:
                    self._render_navigation_buttons("wb", i, len(st.session_state.cv_weiterbildungen))
                
                with col_content:
                    self._render_training_form(entry, i)
                
                st.divider()
    
    def _render_navigation_buttons(self, prefix: str, index: int, total_count: int) -> None:
        """Render navigation and action buttons for list items"""
        session_key_map = {
            "be": "cv_berufserfahrung",
            "edu": "cv_ausbildung", 
            "wb": "cv_weiterbildungen"
        }
        session_key = session_key_map[prefix]
        
        # Up button
        if st.button("⬆️", key=f"{prefix}_up_{index}", 
                    disabled=(index == 0), 
                    help="Nach oben verschieben", 
                    use_container_width=True):
            self._move_item_up(session_key, index)
            st.rerun()
        
        # Down button
        if st.button("⬇️", key=f"{prefix}_down_{index}",
                    disabled=(index == total_count - 1),
                    help="Nach unten verschieben", 
                    use_container_width=True):
            self._move_item_down(session_key, index)
            st.rerun()
        
        # Delete button
        if st.button("🗑️", key=f"delete_{prefix}_{index}",
                    help="Eintrag löschen", 
                    use_container_width=True):
            st.session_state[session_key].pop(index)
            st.rerun()
    
    def _render_experience_form(self, entry: Dict[str, Any], index: int) -> None:
        """Render form fields for work experience entry"""
        col1, col2 = st.columns(2)
        
        with col1:
            entry["zeitraum"] = st.text_input(
                "Zeitraum", 
                value=entry.get("zeitraum", ""), 
                key=f"be_zeitraum_{index}"
            )
            entry["unternehmen"] = st.text_input(
                "Unternehmen", 
                value=entry.get("unternehmen", ""), 
                key=f"be_unternehmen_{index}"
            )
        
        with col2:
            entry["position"] = st.text_input(
                "Position", 
                value=entry.get("position", ""), 
                key=f"be_position_{index}"
            )
            
            # Tasks as multi-line text
            aufgaben_text = '\n'.join(entry.get("aufgaben", [])) if isinstance(entry.get("aufgaben"), list) else str(entry.get("aufgaben", ""))
            aufgaben_input = st.text_area(
                "Aufgaben (eine pro Zeile)", 
                value=aufgaben_text, 
                key=f"be_aufgaben_{index}", 
                height=150
            )
            entry["aufgaben"] = [a.strip() for a in aufgaben_input.split('\n') if a.strip()]
    
    def _render_education_form(self, entry: Dict[str, Any], index: int) -> None:
        """Render form fields for education entry"""
        col1, col2 = st.columns(2)
        
        with col1:
            entry["zeitraum"] = st.text_input(
                "Zeitraum", 
                value=entry.get("zeitraum", ""), 
                key=f"edu_zeitraum_{index}"
            )
            entry["institution"] = st.text_input(
                "Institution", 
                value=entry.get("institution", ""), 
                key=f"edu_institution_{index}"
            )
            entry["abschluss"] = st.text_input(
                "Abschluss", 
                value=entry.get("abschluss", ""), 
                key=f"edu_abschluss_{index}"
            )
        
        with col2:
            entry["note"] = st.text_input(
                "Note", 
                value=entry.get("note", ""), 
                key=f"edu_note_{index}"
            )
            entry["schwerpunkte"] = st.text_area(
                "Schwerpunkte", 
                value=entry.get("schwerpunkte", ""), 
                key=f"edu_schwerpunkte_{index}", 
                height=150
            )
    
    def _render_training_form(self, entry: Dict[str, Any], index: int) -> None:
        """Render form fields for training entry"""
        col1, col2 = st.columns(2)
        
        with col1:
            entry["zeitraum"] = st.text_input(
                "Zeitraum", 
                value=entry.get("zeitraum", ""), 
                key=f"wb_zeitraum_{index}"
            )
            entry["bezeichnung"] = st.text_input(
                "Bezeichnung", 
                value=entry.get("bezeichnung", ""), 
                key=f"wb_bezeichnung_{index}"
            )
        
        with col2:
            entry["abschluss"] = st.text_input(
                "Abschluss/Details", 
                value=entry.get("abschluss", ""), 
                key=f"wb_abschluss_{index}"
            )
    
    def _move_item_up(self, session_key: str, index: int) -> None:
        """Move an item up in the session state list"""
        items = st.session_state[session_key]
        if index > 0:
            items[index], items[index-1] = items[index-1], items[index]
            st.session_state[session_key] = items
    
    def _move_item_down(self, session_key: str, index: int) -> None:
        """Move an item down in the session state list"""
        items = st.session_state[session_key]
        if index < len(items) - 1:
            items[index], items[index+1] = items[index+1], items[index]
            st.session_state[session_key] = items