"""
Zentrales Error Handling und Logging für CV2Profile
"""
import logging
import streamlit as st
import traceback
from typing import Optional, Callable, Any
from functools import wraps
import sys
from pathlib import Path

class ErrorHandler:
    """Zentraler Error Handler mit Logging und User-Feedback"""
    
    def __init__(self):
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """Konfiguriert den Logger"""
        logger = logging.getLogger('cv2profile')
        logger.setLevel(logging.INFO)
        
        # Formatierung
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console Handler
        if not logger.handlers:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
            
            # File Handler (optional)
            try:
                log_dir = Path("logs")
                log_dir.mkdir(exist_ok=True)
                file_handler = logging.FileHandler(log_dir / "cv2profile.log")
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
            except Exception:
                pass  # Fallback: nur Console-Logging
        
        return logger
    
    def handle_error(self, 
                    error: Exception, 
                    context: str = "",
                    show_user: bool = True,
                    user_message: Optional[str] = None) -> None:
        """
        Zentrale Fehlerbehandlung
        
        Args:
            error: Die aufgetretene Exception
            context: Kontext in dem der Fehler auftrat
            show_user: Ob dem User eine Meldung gezeigt werden soll
            user_message: Benutzerdefinierte Fehlermeldung
        """
        # Logging
        error_msg = f"{context}: {str(error)}" if context else str(error)
        self.logger.error(error_msg, exc_info=True)
        
        # User Feedback
        if show_user:
            if user_message:
                st.error(user_message)
            else:
                st.error(f"Ein Fehler ist aufgetreten: {str(error)}")
    
    def safe_execute(self, 
                    func: Callable, 
                    *args, 
                    context: str = "",
                    default_return: Any = None,
                    show_user: bool = True,
                    **kwargs) -> Any:
        """
        Führt eine Funktion sicher aus
        
        Args:
            func: Auszuführende Funktion
            *args: Funktionsargumente
            context: Kontext für Fehlerbehandlung
            default_return: Rückgabewert bei Fehler
            show_user: Ob User-Feedback gezeigt werden soll
            **kwargs: Funktions-Keyword-Argumente
            
        Returns:
            Funktionsergebnis oder default_return bei Fehler
        """
        try:
            return func(*args, **kwargs)
        except Exception as e:
            self.handle_error(e, context, show_user)
            return default_return
    
    def log_info(self, message: str, context: str = "") -> None:
        """Info-Logging"""
        log_msg = f"{context}: {message}" if context else message
        self.logger.info(log_msg)
    
    def log_warning(self, message: str, context: str = "") -> None:
        """Warning-Logging"""
        log_msg = f"{context}: {message}" if context else message
        self.logger.warning(log_msg)

# Decorator für automatisches Error Handling
def safe_streamlit_component(context: str = "", show_errors: bool = True):
    """
    Decorator für sichere Streamlit-Komponenten
    
    Args:
        context: Beschreibung der Komponente
        show_errors: Ob Fehler dem User gezeigt werden sollen
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            error_handler = ErrorHandler()
            return error_handler.safe_execute(
                func, 
                *args, 
                context=context or func.__name__,
                show_user=show_errors,
                **kwargs
            )
        return wrapper
    return decorator

# Globaler Error Handler
global_error_handler = ErrorHandler()

# Convenience Functions
def log_error(error: Exception, context: str = "", show_user: bool = True):
    """Convenience function für Error-Logging"""
    global_error_handler.handle_error(error, context, show_user)

def log_info(message: str, context: str = ""):
    """Convenience function für Info-Logging"""
    global_error_handler.log_info(message, context)

def log_warning(message: str, context: str = ""):
    """Convenience function für Warning-Logging"""
    global_error_handler.log_warning(message, context) 