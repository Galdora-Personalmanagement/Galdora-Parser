"""
Unternehmen-Konfiguration für Multi-Company Support
"""
import os
from typing import Dict, Any, List

# Basis-Pfad für Assets
STATIC_PATH = "static/images"

# Ansprechpartner-Definitionen
CONTACTS = {
    "bejob": [
        {"name": "Dirk Keulertz", "phone": "02161 94 99 072", "email": "keulertz@bejob.de"},
        {"name": "Esra Karakus", "phone": "02161 94 99 080", "email": "karakus@bejob.de"},
        {"name": "Sevla Saltimis", "phone": "02161 94 99 081", "email": "satilmis@bejob.de"},
        {"name": "Hemat Shor", "phone": "02161 94 99 069", "email": "shor@bejob.de"},
        {"name": "Daniel Fischer", "phone": "02161 94 99 077", "email": "Fischer@bejob.de"},
        {"name": "Sude Savaci", "phone": "02161 94 99 082", "email": "Savasci@bejob.de"},
        {"name": "Baran Gündogdu", "phone": "02161 94 99 069", "email": "gündogdu@bejob.de"}
    ],
    "galdora": [
        {"name": "Max Mustermann", "phone": "0123 456789", "email": "mustermann@galdora.de"},
        {"name": "Erika Musterfrau", "phone": "0123 456780", "email": "musterfrau@galdora.de"}
    ]
}

# Unternehmen-Definitionen
COMPANIES = {
    "galdora": {
        "name": "GALDORA",
        "display_name": "Galdora",
        "logo_filename": "galdoralogo.png",
        "logo_path": os.path.join(STATIC_PATH, "galdoralogo.png"),
        "colors": {
            "primary": "#1f4e79",  # Dunkelblau
            "secondary": "#2d5aa0",  # Mittelblau  
            "accent": "#4a90e2"     # Hellblau
        },
        "description": "Personalberatung & Executive Search"
    },
    "bejob": {
        "name": "BEJOB",
        "display_name": "BeJob",
        "logo_filename": "bejob-logo.png", 
        "logo_path": os.path.join(STATIC_PATH, "bejob-logo.png"),
        "colors": {
            "primary": "#e74c3c",   # Rot
            "secondary": "#c0392b",  # Dunkelrot
            "accent": "#f39c12"      # Orange
        },
        "description": "Moderne Recruiting-Lösungen"
    }
}

def get_company_config(company_key: str) -> Dict[str, Any]:
    """
    Gibt die Konfiguration für ein Unternehmen zurück
    
    Args:
        company_key: Unternehmen-Schlüssel ('galdora' oder 'bejob')
    
    Returns:
        Dictionary mit Unternehmensdaten
    """
    if company_key not in COMPANIES:
        raise ValueError(f"Unbekanntes Unternehmen: {company_key}")
    
    return COMPANIES[company_key]

def get_available_companies() -> Dict[str, str]:
    """
    Gibt alle verfügbaren Unternehmen für die Auswahl zurück
    
    Returns:
        Dictionary mit company_key: display_name Mapping
    """
    return {key: config["display_name"] for key, config in COMPANIES.items()}

def get_company_logo_path(company_key: str) -> str:
    """
    Gibt den Pfad zum Unternehmens-Logo zurück
    
    Args:
        company_key: Unternehmen-Schlüssel
    
    Returns:
        Absoluter Pfad zum Logo
    """
    config = get_company_config(company_key)
    logo_path = config["logo_path"]
    
    # Prüfe ob Logo-Datei existiert
    if not os.path.exists(logo_path):
        print(f"Warnung: Logo-Datei nicht gefunden: {logo_path}")
        # Fallback auf alternatives Logo
        alt_logo = config["logo_filename"]
        fallback_paths = [
            f"static/images/{alt_logo}",
            alt_logo
        ]
        
        for fallback in fallback_paths:
            if os.path.exists(fallback):
                print(f"Verwende Fallback-Logo: {fallback}")
                return fallback
        
        print(f"Kein Logo gefunden für {company_key}")
        return ""
    
    return logo_path

def get_company_contacts(company_key: str) -> List[Dict[str, str]]:
    """
    Gibt die Ansprechpartner für ein Unternehmen zurück
    
    Args:
        company_key: Unternehmen-Schlüssel ('galdora' oder 'bejob')
    
    Returns:
        Liste mit Ansprechpartnern (Name, Telefon, E-Mail)
    """
    if company_key not in CONTACTS:
        return []
    
    return CONTACTS[company_key]

def validate_company_assets():
    """
    Validiert ob alle Unternehmen-Assets (Logos) verfügbar sind
    
    Returns:
        Dict mit Validierungsergebnissen
    """
    results = {}
    
    for company_key, config in COMPANIES.items():
        logo_path = get_company_logo_path(company_key)
        results[company_key] = {
            "logo_exists": os.path.exists(logo_path) if logo_path else False,
            "logo_path": logo_path,
            "config_valid": True
        }
    
    return results 