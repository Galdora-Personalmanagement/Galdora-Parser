"""
CV2Profile Konverter - Refactored Version
Verbesserte Architektur mit modularen Komponenten
"""
import streamlit as st
import os
from pathlib import Path

# Optimierte Imports
from utils.session_manager import SessionManager
from utils.file_validator import FileValidator
from utils.error_handler import safe_streamlit_component, log_info
from ui.components.cv_editor import CVEditorComponents, CV_FIELD_CONFIGS
from ui.styles.global_css import load_custom_css
from core.combined_processor import CombinedProcessor
from templates.template_generator import ProfileGenerator

class ConversaoKonverter:
    """Hauptklasse für den CV2Profile Konverter"""
    
    def __init__(self):
        self.session_manager = SessionManager()
        self.file_validator = FileValidator()
        self._initialize_app()
    
    def _initialize_app(self):
        """Initialisiert die Streamlit-App"""
        st.set_page_config(
            page_title="CV2Profile Konverter",
            layout="wide",
            initial_sidebar_state="collapsed"
        )
        
        # Session State initialisieren
        self.session_manager.init_session_defaults()
        
        # Validiere Session-Integrität
        if not self.session_manager.validate_session_integrity():
            st.error("Session beschädigt. Bitte laden Sie die Seite neu.")
            st.stop()
        
        # CSS laden
        load_custom_css()
        
        # Header rendern
        self._render_header()
    
    @safe_streamlit_component("Header Rendering")
    def _render_header(self):
        """Rendert den App-Header"""
        st.markdown("""
        <div class="app-header">
            <h1>🚀 CV2Profile Konverter</h1>
            <p>Konvertiere deinen Lebenslauf in ein professionelles Profil</p>
        </div>
        """, unsafe_allow_html=True)
    
    @safe_streamlit_component("Company Selection")
    def _render_company_selection(self):
        """Rendert die Unternehmens-Auswahl"""
        st.markdown("### 🏢 Unternehmen auswählen")
        
        from utils.company_config import get_available_companies
        companies = get_available_companies()
        
        selected_company = st.selectbox(
            "Unternehmen:",
            options=list(companies.keys()),
            format_func=lambda x: companies[x],
            key="company_selector"
        )
        
        # Session State aktualisieren
        self.session_manager.safe_set('selected_company', selected_company)
        
        return selected_company
    
    @safe_streamlit_component("File Upload")
    def _render_file_upload(self):
        """Rendert den Datei-Upload-Bereich"""
        st.subheader("1. 📄 Lebenslauf hochladen")
        
        # Mode-Auswahl
        mode = st.radio(
            "Wie möchten Sie vorgehen?",
            options=["📄 Lebenslauf hochladen", "📝 Leere Profilvorlage"],
            horizontal=True,
            key="mode_selection"
        )
        
        if mode == "📄 Lebenslauf hochladen":
            uploaded_file = st.file_uploader(
                "Datei hochladen (PDF, JPG, PNG, DOCX)",
                help="Unterstützte Dateiformate"
            )
            
            if uploaded_file:
                # Validierung und sichere Verarbeitung
                temp_path = self.file_validator.create_secure_temp_file(uploaded_file)
                if temp_path:
                    return self._process_uploaded_file(temp_path)
            
        else:
            # Leere Vorlage
            if st.button("🚀 Leere Vorlage erstellen", type="primary"):
                self._create_empty_template()
                st.rerun()
        
        return None
    
    @safe_streamlit_component("File Processing")
    def _process_uploaded_file(self, file_path: str):
        """Verarbeitet die hochgeladene Datei"""
        try:
            # API-Key aus Session holen
            api_key = self.session_manager.safe_get('saved_api_key')
            if not api_key:
                st.warning("OpenAI API-Key fehlt. Bitte in den Einstellungen eingeben.")
                return None
            
            with st.spinner("Datei wird verarbeitet..."):
                processor = CombinedProcessor(api_key)
                
                # Datei verarbeiten
                extracted_text, profile_data = processor.process_and_extract(
                    file_path, 
                    os.path.splitext(file_path)[1]
                )
                
                # Session State aktualisieren
                updates = {
                    'extracted_text': extracted_text,
                    'profile_data': profile_data,
                    'step': 2
                }
                self.session_manager.batch_update(updates)
                
                log_info("Datei erfolgreich verarbeitet")
                st.success("✅ Lebenslauf erfolgreich analysiert!")
                
                return profile_data
                
        except Exception as e:
            st.error(f"Fehler bei der Verarbeitung: {str(e)}")
            return None
    
    def _create_empty_template(self):
        """Erstellt eine leere Profilvorlage"""
        empty_data = {
            "persönliche_daten": {
                "name": "",
                "wohnort": "",
                "jahrgang": "",
                "führerschein": ""
            },
            "berufserfahrung": [],
            "ausbildung": [],
            "weiterbildungen": []
        }
        
        updates = {
            'profile_data': empty_data,
            'empty_template_mode': True,
            'step': 2
        }
        self.session_manager.batch_update(updates)
        log_info("Leere Vorlage erstellt")
    
    @safe_streamlit_component("Profile Editor")
    def _render_profile_editor(self):
        """Rendert den Profil-Editor"""
        st.subheader("2. ✏️ Profil bearbeiten")
        
        profile_data = self.session_manager.safe_get('profile_data', {})
        
        # Tabs für Editor und Export
        tab1, tab2 = st.tabs(["📝 Bearbeiten", "📤 Exportieren"])
        
        with tab1:
            self._render_edit_tab(profile_data)
        
        with tab2:
            self._render_export_tab()
    
    def _render_edit_tab(self, profile_data: dict):
        """Rendert den Bearbeitungs-Tab"""
        # Persönliche Daten
        personal_data = CVEditorComponents.render_personal_data_editor(profile_data)
        
        # Kontaktinformationen
        contact_data = CVEditorComponents.render_contact_editor()
        
        # CV-Abschnitte
        berufserfahrung = CVEditorComponents.render_cv_section_editor(
            "Berufserfahrung",
            "cv_berufserfahrung",
            CV_FIELD_CONFIGS["berufserfahrung"],
            "🏢"
        )
        
        ausbildung = CVEditorComponents.render_cv_section_editor(
            "Ausbildung",
            "cv_ausbildung",
            CV_FIELD_CONFIGS["ausbildung"],
            "🎓"
        )
        
        weiterbildungen = CVEditorComponents.render_cv_section_editor(
            "Weiterbildungen",
            "cv_weiterbildungen",
            CV_FIELD_CONFIGS["weiterbildungen"],
            "📚"
        )
        
        # Daten zusammenführen und speichern
        complete_data = {
            "persönliche_daten": {**personal_data, "kontakt": contact_data},
            "berufserfahrung": berufserfahrung,
            "ausbildung": ausbildung,
            "weiterbildungen": weiterbildungen
        }
        
        self.session_manager.safe_set('edited_data', complete_data)
    
    @safe_streamlit_component("Export Tab")
    def _render_export_tab(self):
        """Rendert den Export-Tab"""
        st.markdown("### 📤 Profil exportieren")
        
        edited_data = self.session_manager.safe_get('edited_data', {})
        if not edited_data:
            st.warning("Bitte bearbeiten Sie zuerst Ihre Profildaten.")
            return
        
        # Profil generieren
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 PDF generieren", type="primary", use_container_width=True):
                self._generate_profile(edited_data, "pdf")
        
        with col2:
            if st.button("📝 Word generieren", type="primary", use_container_width=True):
                self._generate_profile(edited_data, "docx")
    
    @safe_streamlit_component("Profile Generation")
    def _generate_profile(self, data: dict, format_type: str):
        """Generiert das Profil im gewünschten Format"""
        try:
            selected_company = self.session_manager.safe_get('selected_company', 'galdora')
            generator = ProfileGenerator(selected_company=selected_company)
            
            with st.spinner(f"{format_type.upper()} wird generiert..."):
                import tempfile
                
                suffix = f".{format_type}"
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    output_path = tmp.name
                
                # Profil generieren
                result_path = generator.generate_profile(
                    data, 
                    output_path, 
                    template="classic",
                    format=format_type
                )
                
                # Download anbieten
                with open(result_path, "rb") as file:
                    file_data = file.read()
                
                name = data.get("persönliche_daten", {}).get("name", "Unbekannt")
                filename = f"Profilvorlage-{name}.{format_type}"
                
                mime_types = {
                    "pdf": "application/pdf",
                    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                }
                
                st.download_button(
                    label=f"📥 {format_type.upper()} herunterladen",
                    data=file_data,
                    file_name=filename,
                    mime=mime_types.get(format_type, "application/octet-stream"),
                    use_container_width=True
                )
                
                st.success(f"✅ {format_type.upper()} erfolgreich erstellt!")
                
        except Exception as e:
            st.error(f"Fehler bei der {format_type.upper()}-Generierung: {str(e)}")
    
    def run(self):
        """Hauptausführung der App"""
        try:
            # Unternehmens-Auswahl
            self._render_company_selection()
            st.divider()
            
            # Aktueller Schritt bestimmen
            current_step = self.session_manager.safe_get('step', 1)
            
            if current_step == 1:
                # Schritt 1: Datei-Upload
                self._render_file_upload()
            
            elif current_step == 2:
                # Schritt 2: Profil-Editor
                self._render_profile_editor()
                
                # Zurück-Button
                if st.button("🔙 Zurück zu Schritt 1"):
                    self.session_manager.safe_set('step', 1)
                    st.rerun()
            
            # Footer
            self._render_footer()
            
        except Exception as e:
            st.error(f"Unerwarteter Fehler: {str(e)}")
            st.info("Bitte laden Sie die Seite neu.")
    
    def _render_footer(self):
        """Rendert den Footer"""
        st.divider()
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <p>CV2Profile Konverter © 2025 | 
            <a href="#" style="color: white;">Datenschutz</a> | 
            <a href="#" style="color: white;">Impressum</a></p>
        </div>
        """, unsafe_allow_html=True)

# App-Instanz und Ausführung
if __name__ == "__main__":
    app = ConversaoKonverter()
    app.run() 