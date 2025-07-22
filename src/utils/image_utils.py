import os
import shutil
import streamlit as st
from pathlib import Path

def get_image_path(image_name, use_static=False):
    """
    Gibt den Pfad zu einem Bild zurück.
    
    Args:
        image_name: Name der Bilddatei
        use_static: Bei True wird das Bild aus dem static-Verzeichnis geladen (für HTTPS-Kompatibilität)
    
    Returns:
        String mit dem Pfad zum Bild
    """
    # Prüfe, ob das Bild im static-Verzeichnis verwendet werden soll
    if use_static:
        static_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'static', 'images', image_name)
        if os.path.exists(static_path):
            return static_path
    
    # Versuche das Bild im sources-Verzeichnis zu finden
    source_path = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'sources', image_name)
    if os.path.exists(source_path):
        return source_path
    
    # Wenn kein Pfad gefunden wurde, gib einen leeren String zurück
    return ""

def ensure_images_in_static():
    """
    Stellt sicher, dass alle Bilder aus dem sources-Verzeichnis auch im static/images-Verzeichnis vorhanden sind.
    Dies ist wichtig für die HTTPS-Kompatibilität.
    """
    # Definiere die Verzeichnispfade
    base_dir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    sources_dir = os.path.join(base_dir, 'sources')
    static_images_dir = os.path.join(base_dir, 'static', 'images')
    
    # Stelle sicher, dass das Zielverzeichnis existiert
    os.makedirs(static_images_dir, exist_ok=True)
    
    # Kopiere alle Bilder aus dem sources-Verzeichnis in das static/images-Verzeichnis
    if os.path.exists(sources_dir):
        for filename in os.listdir(sources_dir):
            file_path = os.path.join(sources_dir, filename)
            if os.path.isfile(file_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                dest_path = os.path.join(static_images_dir, filename)
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