"""
Centralized Configuration Management
Replaces scattered hardcoded values and magic numbers throughout the codebase.
"""

from pathlib import Path
from typing import Dict, List, Any


class LayoutConstants:
    """Layout and styling constants for PDF generation"""
    
    # Logo dimensions
    LOGO_WIDTH_BEJOB = 180
    LOGO_WIDTH_DEFAULT = 160
    
    # PDF layout
    BASE_HEIGHT = 40
    MAX_TASKS_PER_ENTRY = 6
    A4_WIDTH_FACTOR_LEFT = 0.15
    A4_WIDTH_FACTOR_RIGHT = 0.65
    
    # Spacing
    SECTION_SPACING = 0.5  # cm
    ENTRY_SPACING = 0.1    # cm
    HEADER_SPACING = 0.2   # cm
    
    # Font sizes
    TITLE_FONT_SIZE = 16
    NAME_FONT_SIZE = 13
    HEADING_FONT_SIZE = 11
    NORMAL_FONT_SIZE = 9
    CONTACT_FONT_SIZE = 8


class CompanyContactConfig:
    """Centralized company contact information"""
    
    GALDORA_CONTACTS = {
        "Alessandro Böhm": {
            "email": "boehm@galdora.de",
            "phone": "02161 62126-00",
            "gender": "male"
        },
        "Kai Fischer": {
            "email": "fischer@galdora.de", 
            "phone": "02161 62126-00",
            "gender": "male"
        },
        "Melike Demirkol": {
            "email": "demirkol@galdora.de",
            "phone": "02161 62126-00", 
            "gender": "female"
        },
        "Konrad Ruszczyk": {
            "email": "konrad@galdora.de",
            "phone": "02161 62126-00",
            "gender": "male"
        },
        "Lennard Kuss": {
            "email": "kuss@galdora.de",
            "phone": "02161 62126-00",
            "gender": "male"
        },
        "Salim Alizai": {
            "email": "gl@galdora.de",
            "phone": "02161 62126-00",
            "gender": "male"
        }
    }
    
    BEJOB_CONTACTS = {
        "Dirk Keulertz": {
            "email": "keulertz@bejob.de",
            "phone": "02161 94 99 072",
            "gender": "male"
        },
        "Esra Karakus": {
            "email": "karakus@bejob.de", 
            "phone": "02161 94 99 080",
            "gender": "female"
        },
        "Seyla Saltimis": {
            "email": "satilmis@bejob.de",
            "phone": "02161 94 99 081", 
            "gender": "female"
        },
        "Hemat Shor": {
            "email": "shor@bejob.de",
            "phone": "02161 94 99 069",
            "gender": "male"
        },
        "Daniel Fischer": {
            "email": "Fischer@bejob.de",
            "phone": "02161 94 99 077",
            "gender": "male"
        },
        "Sude Savaci": {
            "email": "Savasci@bejob.de", 
            "phone": "02161 94 99 082",
            "gender": "female"
        },
        "Baran Gündogdu": {
            "email": "gündogdu@bejob.de",
            "phone": "02161 94 99 069",
            "gender": "male"
        }
    }
    
    @classmethod
    def get_contacts_for_company(cls, company_key: str) -> Dict[str, Dict[str, str]]:
        """Get all contacts for a specific company"""
        if company_key == "bejob":
            return cls.BEJOB_CONTACTS
        else:
            return cls.GALDORA_CONTACTS
    
    @classmethod
    def get_contact_info(cls, company_key: str, contact_name: str) -> Dict[str, str]:
        """Get contact information for a specific person"""
        contacts = cls.get_contacts_for_company(company_key)
        return contacts.get(contact_name, {})


class ValidationRules:
    """Data validation rules and constraints"""
    
    REQUIRED_PERSONAL_FIELDS = ["name"]
    REQUIRED_CONTACT_FIELDS = ["email", "telefon"]  # At least one required
    
    FUEHRERSCHEIN_OPTIONS = [
        "Klasse B",
        "Klasse B + PKW vorhanden", 
        "Kein Führerschein",
        "LKW-Führerschein",
        "Staplerschein"
    ]
    
    VERFUEGBARKEIT_OPTIONS = [
        "Sofort verfügbar",
        "Verfügbar ab bestimmtem Datum",
        "Kündigungsfrist 1 Monat", 
        "Kündigungsfrist 2 Monate",
        "Kündigungsfrist 3 Monate",
        "Derzeit nicht verfügbar",
        "Verfügbar mit Einschränkungen"
    ]
    
    @classmethod
    def validate_personal_data(cls, data: Dict[str, Any]) -> List[str]:
        """Validate personal data and return list of errors"""
        errors = []
        
        if not data.get("name"):
            errors.append("Name fehlt")
            
        return errors
    
    @classmethod 
    def validate_contact_data(cls, data: Dict[str, Any]) -> List[str]:
        """Validate contact data and return list of errors"""
        errors = []
        
        if not data.get("email") and not data.get("telefon"):
            errors.append("Mindestens eine Kontaktmöglichkeit (E-Mail oder Telefon) wird benötigt")
            
        return errors


class PathManager:
    """Secure path management utilities"""
    
    @staticmethod
    def get_safe_path(base_path: str, *path_parts: str) -> Path:
        """Create a safe path ensuring it stays within base directory"""
        base = Path(base_path).resolve()
        full_path = base
        
        for part in path_parts:
            # Sanitize each path part
            safe_part = Path(part).name  # Only take filename, no directory traversal
            full_path = full_path / safe_part
            
        # Ensure the result is still within base directory
        try:
            full_path.resolve().relative_to(base)
            return full_path
        except ValueError:
            raise ValueError(f"Path traversal attempt detected: {full_path}")
    
    @staticmethod
    def validate_file_extension(file_path: Path, allowed_extensions: List[str]) -> bool:
        """Validate file extension against whitelist"""
        return file_path.suffix.lower() in [ext.lower() for ext in allowed_extensions]


class AppConfig:
    """Main application configuration"""
    
    # Supported file types
    SUPPORTED_EXTENSIONS = ['.pdf', '.docx', '.jpg', '.jpeg', '.png']
    
    # Template types
    AVAILABLE_TEMPLATES = ['classic', 'modern', 'professional', 'elegant', 'minimalist']
    DEFAULT_TEMPLATE = 'classic'
    
    # Export formats
    EXPORT_FORMATS = ['pdf', 'docx']
    
    # Company configurations
    SUPPORTED_COMPANIES = ['galdora', 'bejob']
    DEFAULT_COMPANY = 'galdora'
    
    # Footer texts
    COMPANY_FOOTERS = {
        'galdora': "GALDORA Personalmanagement GmbH Co.KG\nVolksgartenstr. 85-89, 41065 Mönchengladbach\nE-Mail: info@galdora.de / Web: www.galdora.de",
        'bejob': "bejob – einfach besser bewerben | Volksgartenstr. 85–89, 41065 Mönchengladbach | 02161 / 65326-40 | info@bejob.de | www.bejob.de"
    }
    
    @classmethod
    def get_footer_text(cls, company_key: str) -> str:
        """Get footer text for specific company"""
        return cls.COMPANY_FOOTERS.get(company_key, cls.COMPANY_FOOTERS['galdora'])