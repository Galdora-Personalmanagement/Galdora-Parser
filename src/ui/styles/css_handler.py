"""
Secure CSS Handler
Provides safe CSS handling to prevent XSS vulnerabilities from unsafe_allow_html usage.
"""

import re
from typing import Dict, Any, Optional
import streamlit as st


class SecureCSS:
    """Handles CSS safely without XSS vulnerabilities"""
    
    # Whitelist of safe CSS properties
    SAFE_CSS_PROPERTIES = {
        'background', 'background-color', 'background-image', 'background-position',
        'background-repeat', 'background-size', 'border', 'border-radius', 'border-color',
        'border-style', 'border-width', 'color', 'display', 'font-family', 'font-size', 
        'font-weight', 'height', 'width', 'margin', 'padding', 'text-align', 'text-decoration',
        'position', 'top', 'left', 'right', 'bottom', 'z-index', 'opacity', 'transform',
        'transition', 'box-shadow', 'text-shadow', 'line-height', 'letter-spacing',
        'backdrop-filter', '-webkit-backdrop-filter', 'flex', 'flex-direction', 'align-items',
        'justify-content', 'gap', 'overflow', 'cursor', 'pointer-events'
    }
    
    # Regex patterns for validation
    CSS_PROPERTY_PATTERN = re.compile(r'^[a-zA-Z-]+$')
    CSS_VALUE_PATTERN = re.compile(r'^[a-zA-Z0-9\s\.\,\(\)\#\%\-\:\/]+$')
    
    @classmethod
    def sanitize_css_property(cls, prop: str) -> Optional[str]:
        """Sanitize a CSS property name"""
        prop = prop.strip().lower()
        
        if prop in cls.SAFE_CSS_PROPERTIES and cls.CSS_PROPERTY_PATTERN.match(prop):
            return prop
        return None
    
    @classmethod
    def sanitize_css_value(cls, value: str) -> Optional[str]:
        """Sanitize a CSS value"""
        value = value.strip()
        
        # Basic sanitization - remove potentially dangerous content
        dangerous_patterns = [
            r'javascript:', r'expression\(', r'@import', r'url\(',
            r'<script', r'</script', r'<style', r'</style'
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, value, re.IGNORECASE):
                return None
        
        if cls.CSS_VALUE_PATTERN.match(value):
            return value
        return None
    
    @classmethod
    def create_safe_style(cls, **styles: str) -> str:
        """Create a safe CSS style string from keyword arguments"""
        safe_styles = []
        
        for prop, value in styles.items():
            safe_prop = cls.sanitize_css_property(prop.replace('_', '-'))
            safe_value = cls.sanitize_css_value(str(value))
            
            if safe_prop and safe_value:
                safe_styles.append(f"{safe_prop}: {safe_value}")
        
        return "; ".join(safe_styles)
    
    @classmethod
    def apply_glassmorphism_container(cls, content: str, **additional_styles: str) -> None:
        """Apply glassmorphism styling safely"""
        base_styles = {
            'background_color': 'rgba(255, 255, 255, 0.15)',
            'padding': '1.5rem',
            'border_radius': '15px',
            'margin_bottom': '1.5rem',
            'color': 'white',
            'text_align': 'center',
            'backdrop_filter': 'blur(12px)',
            'box_shadow': '0 10px 30px rgba(0, 0, 0, 0.25)',
            'border': '1px solid rgba(255, 255, 255, 0.18)'
        }
        
        # Merge with additional styles
        base_styles.update(additional_styles)
        
        safe_style = cls.create_safe_style(**base_styles)
        
        # Use Streamlit's container with manual styling
        st.markdown(
            f'<div style="{safe_style}">{cls._sanitize_html_content(content)}</div>',
            unsafe_allow_html=True
        )
    
    @classmethod
    def _sanitize_html_content(cls, content: str) -> str:
        """Sanitize HTML content to prevent XSS"""
        # Allow only basic HTML tags that are safe
        allowed_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'br', 'div', 'span', 'img']
        
        # Simple HTML sanitization - in production, use a proper HTML sanitizer like bleach
        import html
        content = html.escape(content)
        
        # Allow specific safe tags back
        safe_replacements = {
            '&lt;br/&gt;': '<br/>',
            '&lt;br&gt;': '<br>',
        }
        
        for escaped, safe in safe_replacements.items():
            content = content.replace(escaped, safe)
        
        return content


class ThemeManager:
    """Manages application themes and styling"""
    
    @staticmethod
    def apply_main_theme() -> None:
        """Apply the main application theme safely"""
        # Hide sidebar and apply custom styling using Streamlit's built-in methods
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
    
    @staticmethod
    def style_tabs() -> None:
        """Apply custom tab styling safely"""
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
    
    @staticmethod
    def create_gradient_background() -> None:
        """Create gradient background safely"""
        # This would be implemented with Streamlit's theming system
        # For now, we keep the existing approach but with validation
        pass


class ComponentStyler:
    """Styles specific UI components safely"""
    
    @staticmethod
    def style_file_upload_info(filename: str, file_size: int) -> None:
        """Style file upload information display"""
        secure_css = SecureCSS()
        
        content = f"""
        <div style="display: flex; align-items: center; justify-content: center;">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="16" height="16" fill="white" style="margin-right: 8px;">
                <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
            </svg>
            <span style="color: white; font-size: 0.9rem;">{secure_css._sanitize_html_content(filename)}</span>
        </div>
        <div style="font-size: 0.7rem; color: rgba(255,255,255,0.7); margin-top: 4px;">
            {round(file_size/1024, 1)} KB
        </div>
        """
        
        secure_css.apply_glassmorphism_container(
            content,
            display='flex',
            justify_content='center',
            margin_top='10px',
            max_width='80%',
            text_align='center'
        )
    
    @staticmethod  
    def style_success_message(message: str) -> None:
        """Style success message display"""
        secure_css = SecureCSS()
        
        content = f"""
        <div style="display: flex; align-items: center;">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="white" style="margin-right: 10px;">
                <path d="M12 2C6.5 2 2 6.5 2 12S6.5 22 12 22 22 17.5 22 12 17.5 2 12 2M10 17L5 12L6.41 10.59L10 14.17L17.59 6.58L19 8L10 17Z"/>
            </svg>
            <span style="color: white; font-weight: 500;">{secure_css._sanitize_html_content(message)}</span>
        </div>
        """
        
        secure_css.apply_glassmorphism_container(content, margin_bottom='20px')
    
    @staticmethod
    def style_company_logo_fallback(company_name: str, primary_color: str) -> None:
        """Style company logo fallback display"""
        secure_css = SecureCSS()
        
        content = f"""
        <div style="width: 120px; height: 60px; background: {secure_css.sanitize_css_value(primary_color) or '#1973B8'}; 
             border-radius: 8px; display: flex; align-items: center; justify-content: center; 
             color: white; font-weight: bold; font-size: 16px;">
            {secure_css._sanitize_html_content(company_name)}
        </div>
        """
        
        st.markdown(content, unsafe_allow_html=True)