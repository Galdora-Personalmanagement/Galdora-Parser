"""
Sicherer File-Upload und Validierungs-Utility
"""
import os
import tempfile
import hashlib
from typing import Optional, Tuple
import streamlit as st

class FileValidator:
    """Sichere Datei-Validierung und -Verarbeitung"""
    
    ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.jpg', '.jpeg', '.png'}
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    
    @staticmethod
    def validate_file(uploaded_file) -> Tuple[bool, str]:
        """
        Validiert eine hochgeladene Datei
        
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not uploaded_file:
            return False, "Keine Datei ausgewählt"
        
        # Dateigröße prüfen
        file_size = len(uploaded_file.getvalue())
        if file_size > FileValidator.MAX_FILE_SIZE:
            return False, f"Datei zu groß. Maximum: {FileValidator.MAX_FILE_SIZE // 1024 // 1024}MB"
        
        # Dateiextension prüfen
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        if file_extension not in FileValidator.ALLOWED_EXTENSIONS:
            return False, f"Dateityp nicht erlaubt. Erlaubt: {', '.join(FileValidator.ALLOWED_EXTENSIONS)}"
        
        # Dateiname sanitizen
        if len(uploaded_file.name) > 255:
            return False, "Dateiname zu lang"
        
        # Prüfe auf gefährliche Zeichen
        dangerous_chars = ['..', '/', '\\', '<', '>', '|', ':', '*', '?', '"']
        if any(char in uploaded_file.name for char in dangerous_chars):
            return False, "Dateiname enthält ungültige Zeichen"
        
        return True, ""
    
    @staticmethod
    def create_secure_temp_file(uploaded_file) -> Optional[str]:
        """
        Erstellt eine sichere temporäre Datei
        
        Returns:
            str: Pfad zur temporären Datei oder None bei Fehler
        """
        is_valid, error = FileValidator.validate_file(uploaded_file)
        if not is_valid:
            st.error(f"Datei-Validierung fehlgeschlagen: {error}")
            return None
        
        try:
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()
            
            # Sichere temporäre Datei erstellen
            with tempfile.NamedTemporaryFile(
                delete=False, 
                suffix=file_extension,
                prefix="cv2profile_",
                dir=tempfile.gettempdir()
            ) as tmp_file:
                tmp_file.write(uploaded_file.getbuffer())
                temp_path = tmp_file.name
            
            # Registriere für Cleanup
            if 'temp_files' not in st.session_state:
                st.session_state.temp_files = []
            st.session_state.temp_files.append(temp_path)
            
            return temp_path
            
        except Exception as e:
            st.error(f"Fehler beim Erstellen der temporären Datei: {str(e)}")
            return None
    
    @staticmethod
    def cleanup_temp_files():
        """Räumt alle temporären Dateien auf"""
        if 'temp_files' in st.session_state:
            for temp_file in st.session_state.temp_files:
                try:
                    if os.path.exists(temp_file):
                        os.unlink(temp_file)
                except Exception as e:
                    print(f"Fehler beim Löschen von {temp_file}: {e}")
            st.session_state.temp_files = [] 