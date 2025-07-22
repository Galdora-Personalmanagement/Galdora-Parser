"""
Optimierter Session State Manager für bessere Performance
"""
import streamlit as st
from typing import Any, Dict, Optional
import copy

class SessionManager:
    """Zentraler Manager für Session State mit Performance-Optimierungen"""
    
    # Cache für häufig verwendete Daten
    _data_cache: Dict[str, Any] = {}
    
    @staticmethod
    def init_session_defaults():
        """Initialisiert alle Session State Defaults nur einmal"""
        defaults = {
            'step': 1,
            'extracted_text': '',
            'profile_data': {},
            'edited_data': {},
            'preview_pdf': None,
            'temp_files': [],
            'cv_berufserfahrung': [],
            'cv_ausbildung': [],
            'cv_weiterbildungen': [],
            'selected_company': 'galdora',
            'empty_template_mode': False,
            'update_preview': False,
            'selected_template': 'classic'
        }
        
        for key, default_value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = copy.deepcopy(default_value)
    
    @staticmethod
    @st.cache_data(ttl=300)  # Cache für 5 Minuten
    def get_company_config(company: str) -> Dict:
        """Cached Company-Konfiguration"""
        from utils.company_config import get_company_config
        return get_company_config(company)
    
    @staticmethod
    def safe_get(key: str, default: Any = None) -> Any:
        """Sicherer Zugriff auf Session State mit Fallback"""
        return st.session_state.get(key, default)
    
    @staticmethod
    def safe_set(key: str, value: Any, force_update: bool = False) -> bool:
        """
        Sicheres Setzen von Session State-Werten
        
        Args:
            key: Session State Key
            value: Zu setzender Wert
            force_update: Erzwingt Update auch bei gleichem Wert
            
        Returns:
            bool: True wenn Wert geändert wurde
        """
        current_value = st.session_state.get(key)
        
        # Nur updaten wenn Wert sich geändert hat (Performance-Optimierung)
        if not force_update and current_value == value:
            return False
        
        st.session_state[key] = copy.deepcopy(value)
        return True
    
    @staticmethod
    def batch_update(updates: Dict[str, Any]) -> int:
        """
        Batch-Update für mehrere Session State-Werte
        
        Args:
            updates: Dictionary mit Key-Value-Paaren
            
        Returns:
            int: Anzahl der tatsächlich geänderten Werte
        """
        changed_count = 0
        for key, value in updates.items():
            if SessionManager.safe_set(key, value):
                changed_count += 1
        return changed_count
    
    @staticmethod
    def reset_cv_data():
        """Reset nur der CV-spezifischen Daten"""
        cv_keys = ['cv_berufserfahrung', 'cv_ausbildung', 'cv_weiterbildungen']
        for key in cv_keys:
            st.session_state[key] = []
    
    @staticmethod
    def get_cv_data() -> Dict[str, list]:
        """Optimierter Zugriff auf CV-Daten"""
        return {
            'berufserfahrung': SessionManager.safe_get('cv_berufserfahrung', []),
            'ausbildung': SessionManager.safe_get('cv_ausbildung', []),
            'weiterbildungen': SessionManager.safe_get('cv_weiterbildungen', [])
        }
    
    @staticmethod
    def validate_session_integrity() -> bool:
        """Prüft die Integrität der Session State-Daten"""
        required_keys = ['step', 'profile_data', 'selected_company']
        
        for key in required_keys:
            if key not in st.session_state:
                st.error(f"Session State korrupt: {key} fehlt")
                return False
        
        # Typ-Validierung
        if not isinstance(st.session_state.get('step'), int):
            st.session_state['step'] = 1
        
        if not isinstance(st.session_state.get('temp_files'), list):
            st.session_state['temp_files'] = []
        
        return True 