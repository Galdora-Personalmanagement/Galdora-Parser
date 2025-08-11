"""
Standardized Error Handling
Centralizes error handling patterns used throughout the application.
"""

import logging
import streamlit as st
from typing import Optional, Any, Callable
from functools import wraps
import traceback


class ErrorHandler:
    """Centralized error handling with consistent user feedback"""
    
    @staticmethod
    def setup_logging() -> None:
        """Setup application logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/cv_parser.log'),
                logging.StreamHandler()
            ]
        )
    
    @staticmethod
    def handle_file_error(e: Exception, file_path: str, operation: str = "verarbeiten") -> None:
        """Handle file-related errors with user-friendly messages"""
        error_msg = f"Fehler beim {operation} der Datei {file_path}: {str(e)}"
        st.error(error_msg)
        logging.error(f"File error: {error_msg}", exc_info=True)
    
    @staticmethod
    def handle_template_error(e: Exception, template_type: str) -> None:
        """Handle template generation errors"""
        error_msg = f"Fehler bei der Generierung des {template_type}-Templates: {str(e)}"
        st.error(error_msg)
        logging.error(f"Template error: {error_msg}", exc_info=True)
    
    @staticmethod
    def handle_api_error(e: Exception, service: str = "OpenAI") -> None:
        """Handle API-related errors"""
        error_msg = f"Fehler bei der {service}-API-Anfrage: {str(e)}"
        st.error(error_msg)
        logging.error(f"API error: {error_msg}", exc_info=True)
    
    @staticmethod
    def handle_validation_error(errors: list, context: str = "Datenvalidierung") -> None:
        """Handle validation errors with detailed feedback"""
        if errors:
            st.error(f"Fehler bei der {context}:")
            for error in errors:
                st.error(f"• {error}")
            logging.warning(f"Validation errors in {context}: {errors}")
    
    @staticmethod
    def handle_session_error(e: Exception, operation: str) -> None:
        """Handle session state related errors"""
        error_msg = f"Fehler bei der Session-Verwaltung ({operation}): {str(e)}"
        st.error(error_msg)
        logging.error(f"Session error: {error_msg}", exc_info=True)
    
    @staticmethod
    def handle_unexpected_error(e: Exception, context: str = "Anwendung") -> None:
        """Handle unexpected errors with fallback behavior"""
        error_msg = f"Unerwarteter Fehler in {context}: {str(e)}"
        st.error(f"Ein unerwarteter Fehler ist aufgetreten. Bitte versuchen Sie es erneut.")
        st.error(f"Technische Details: {error_msg}")
        logging.error(f"Unexpected error: {error_msg}", exc_info=True)


class SafeExecutor:
    """Safe execution wrapper with error handling"""
    
    @staticmethod
    def safe_file_operation(operation: Callable, file_path: str, 
                          fallback_value: Any = None, 
                          operation_name: str = "verarbeiten") -> Any:
        """Safely execute file operations with error handling"""
        try:
            return operation()
        except FileNotFoundError:
            ErrorHandler.handle_file_error(
                Exception(f"Datei nicht gefunden: {file_path}"), 
                file_path, 
                operation_name
            )
            return fallback_value
        except PermissionError:
            ErrorHandler.handle_file_error(
                Exception(f"Keine Berechtigung für Datei: {file_path}"), 
                file_path, 
                operation_name
            )
            return fallback_value
        except Exception as e:
            ErrorHandler.handle_file_error(e, file_path, operation_name)
            return fallback_value
    
    @staticmethod
    def safe_template_operation(operation: Callable, template_type: str, 
                              fallback_value: Any = None) -> Any:
        """Safely execute template operations with error handling"""
        try:
            return operation()
        except Exception as e:
            ErrorHandler.handle_template_error(e, template_type)
            return fallback_value
    
    @staticmethod
    def safe_api_call(operation: Callable, service: str = "OpenAI", 
                     fallback_value: Any = None) -> Any:
        """Safely execute API calls with error handling"""
        try:
            return operation()
        except Exception as e:
            ErrorHandler.handle_api_error(e, service)
            return fallback_value
    
    @staticmethod
    def safe_session_operation(operation: Callable, operation_name: str,
                             fallback_value: Any = None) -> Any:
        """Safely execute session state operations"""
        try:
            return operation()
        except Exception as e:
            ErrorHandler.handle_session_error(e, operation_name)
            return fallback_value


def safe_streamlit_operation(operation_name: str = "Operation"):
    """Decorator for safe Streamlit operations with error handling"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                ErrorHandler.handle_unexpected_error(e, operation_name)
                return None
        return wrapper
    return decorator


class ResourceManager:
    """Manages resource cleanup and prevents memory leaks"""
    
    def __init__(self):
        self._resources = []
    
    def add_resource(self, resource: Any, cleanup_func: Optional[Callable] = None) -> None:
        """Add a resource to be managed"""
        self._resources.append((resource, cleanup_func))
    
    def cleanup_all(self) -> None:
        """Clean up all managed resources"""
        for resource, cleanup_func in self._resources:
            try:
                if cleanup_func:
                    cleanup_func(resource)
                elif hasattr(resource, 'close'):
                    resource.close()
                elif hasattr(resource, '__del__'):
                    del resource
            except Exception as e:
                logging.warning(f"Error during resource cleanup: {e}")
        
        self._resources.clear()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup_all()


# Global error handler instance
error_handler = ErrorHandler()
safe_executor = SafeExecutor()