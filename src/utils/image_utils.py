import os
import shutil
import streamlit as st
from pathlib import Path
import base64

# Definiert den absoluten Pfad zum Projekt-Root
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
STATIC_DIR = os.path.join(BASE_DIR, 'static', 'images')
SOURCES_DIR = os.path.join(BASE_DIR, 'sources')

def get_image_path(image_name, use_static=False):
    """
    Gibt den Pfad zu einem Bild zurück.
    
    Args:
        image_name: Name der Bilddatei
        use_static: Bei True wird das Bild aus dem static-Verzeichnis geladen (für HTTPS-Kompatibilität)
    
    Returns:
        String mit dem Pfad zum Bild
    """
    if use_static:
        static_path = os.path.join(STATIC_DIR, image_name)
        if os.path.exists(static_path):
            return static_path
    
    source_path = os.path.join(SOURCES_DIR, image_name)
    if os.path.exists(source_path):
        return source_path
    
    return ""

def ensure_images_in_static():
    """
    Stellt sicher, dass alle Bilder aus dem sources-Verzeichnis auch im static/images-Verzeichnis vorhanden sind.
    Dies ist wichtig für die HTTPS-Kompatibilität.
    """
    os.makedirs(STATIC_DIR, exist_ok=True)
    
    if os.path.exists(SOURCES_DIR):
        for filename in os.listdir(SOURCES_DIR):
            file_path = os.path.join(SOURCES_DIR, filename)
            if os.path.isfile(file_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                dest_path = os.path.join(STATIC_DIR, filename)
                if not os.path.exists(dest_path) or os.path.getmtime(file_path) > os.path.getmtime(dest_path):
                    shutil.copy2(file_path, dest_path)
                    print(f"Kopiert: {filename} nach static/images/")

def get_image_as_bytes(image_name):
    """
    Get an image as bytes, useful for embedding in Streamlit
    
    Args:
        image_name: The name of the image file (e.g., 'galdoralogo.png')
        
    Returns:
        bytes: The image as bytes or None if not found
    """
    image_path = get_image_path(image_name, use_static=True)
    
    if image_path and os.path.exists(image_path):
        try:
            with open(image_path, "rb") as f:
                return f.read()
        except Exception as e:
            print(f"Error reading image {image_name}: {e}")
    
    return None

def get_logo_as_base64():
    """Load and convert the logo to base64 for embedding in HTML"""
    try:
        ensure_images_in_static()
        
        logo_path = get_image_path('cv2profile-loho.png', use_static=True)
        
        if not os.path.exists(logo_path):
            logo_path = get_image_path('Galdoralogo.png', use_static=True)
        
        if not os.path.exists(logo_path):
            return ""
        
        with open(logo_path, "rb") as f:
            logo_data = f.read()
            return base64.b64encode(logo_data).decode("utf-8")
    except Exception as e:
        print(f"Error loading logo: {e}")
        return ""
