# CV2Profile Parser-40 - Projektkontext

## Projektübersicht

Der CV2Profile Parser-40 ist ein leistungsstarkes KI-gestütztes Tool zur automatisierten Analyse von Lebensläufen und deren Umwandlung in standardisierte, professionelle PDF-Profile. Die Anwendung nutzt OpenAI-Technologie zur intelligenten Extraktion und Strukturierung von Informationen aus verschiedenen Dokumenttypen.

## Kernfunktionalitäten

### Dokumentenverarbeitung
- **Unterstützte Formate**: PDF, DOCX, JPG, PNG
- **Textextraktion**: Direkte Extraktion mit OCR-Fallback für Bilder
- **KI-gestützte Analyse**: OpenAI-basierte Datenstrukturierung
- **Intelligente Sortierung**: Chronologische Ordnung von Berufserfahrung und Ausbildung

### Template-System
- **5 Professionelle Designs**: Classic, Modern, Professional, Minimalist, Elegant
- **PDF-Generierung**: ReportLab-basierte hochwertige Ausgabe
- **KeepTogether-Funktionalität**: Verhindert Seitenumbrüche in zusammengehörigen Blöcken
- **Geschlechtsspezifische Anrede**: KI-gestützte Pronomen-Anpassung
- **Profilbild-Integration**: Automatische Größenanpassung und Positionierung

### Benutzeroberfläche
- **Streamlit-basiert**: Deutsche Lokalisierung mit modernem Glasmorphismus-Design
- **3-Schritt-Workflow**: Datei hochladen → Daten bearbeiten → Profil exportieren

### Technische Architektur
- **Modularer Aufbau**: Klare Trennung von Core, UI, Templates, Utils
- **Session-State-Management**: Streamlit-basierte Zustandsverwaltung
- **API-Key-Verwaltung**: Sichere Speicherung mit mehreren Fallback-Optionen
- **HTTPS-Kompatibilität**: Automatische Bildverwaltung für Cloud-Deployment

## Entwicklungsgeschichte (Konsolidiert aus allen Summary-Dateien)

### Version 1-2 (Mai 2025)
- **Grundinfrastruktur**: Dokumentenverarbeitung, KI-Extraktion, PDF-Generierung
- **UI-Entwicklung**: Streamlit-Oberfläche mit Glasmorphismus-Design
- **API-Integration**: OpenAI-Anbindung mit sicherer Key-Verwaltung
- **Template-Basis**: Klassisches und modernes Design implementiert

### Version 3 (Juni 2025)
- **Template-Erweiterung**: Professional, Minimalist, Elegant Designs hinzugefügt
- **UI-Optimierung**: Seitenleisten-Design, Statusanzeigen, verbesserte Navigation
- **Funktionalitätserweiterung**: Profilbilder, Anonymisierung, Demo-Modus
- **Code-Bereinigung**: Redundanz-Entfernung, modulare Struktur

### Version 4 (Juni 2025 - Aktuell)
- **Professional Template Optimierung**: Logo-Repositionierung, Firmenkopf-Entfernung
- **KI-Verbesserungen**: Geschlechtserkennung, zeitraum-Korrektur ("bis jetzt" → "2025")
- **Layout-Verbesserungen**: KeepTogether-Implementierung, Name-Positionierung
- **Deployment-Vorbereitung**: Streamlit Cloud ready, GitHub Repository setup
- **Drag & Drop UI-Modernisierung**: Button-System durch natives HTML5 Drag & Drop ersetzt
- **A4-PDF-Vorschau**: Konsistente Vollseiten-Darstellung mit festen A4-Dimensionen

## Aktuelle Technische Details

### Hauptmodule
- **src/core/**: document_processor.py, ai_extractor.py, combined_processor.py
- **src/templates/**: template_generator.py mit 5 Design-Varianten
- **src/ui/**: Streamlit-Anwendung (Home.py, pages/01_Konverter.py, pages/01_⚙️_Einstellungen.py)
- **src/utils/**: config.py, image_utils.py für Konfiguration und Bildverwaltung

### Deployment-Status
- **GitHub Repository**: https://github.com/jjokkln/Parser-Streamlit-Host.git
- **Branch**: new-v4 (deployment-ready)
- **Streamlit Cloud**: Vorbereitet mit streamlit_app.py Entry Point
- **Dependencies**: requirements.txt + packages.txt für Linux-Umgebung

### Bekannte Optimierungen (Zuletzt implementiert)
- **Professional Template**: Firmenkopf entfernt, Logo vergrößert (200px), geschlechtsspezifische Pronomen
- **KeepTogether**: Berufserfahrungsblöcke werden nicht mehr zwischen Seiten getrennt
- **Debug-Integration**: Erweiterte Logging-Funktionen für bessere Fehlerdiagnose
- **UI-Minimierung**: Entfernung redundanter Statusanzeigen, fokussierte Seitenleiste

## Aktuelle Herausforderungen
- **PDF-Vorschau**: Browser-Sicherheitsbeschränkungen bei HTTPS-Umgebungen
- **Performance**: OpenAI-Token-Optimierung für große Dokumente
- **Cross-Browser-Kompatibilität**: Konsistente Darstellung in verschiedenen Browsern
- **Template-Konsistenz**: Einheitliche Formatierung zwischen allen 5 Designs

## Projektphilosophie
- **Deutsche Lokalisierung**: Vollständig deutschsprachige Benutzerführung
- **Benutzerfreundlichkeit**: Intuitive 3-Schritt-Bedienung ohne technische Hürden
- **Professioneller Output**: Hochwertige PDF-Profile für Personalvermittlung
- **Modulare Architektur**: Einfache Erweiterbarkeit und Wartbarkeit
- **Datenschutz**: Lokale Verarbeitung, sichere API-Key-Speicherung, Anonymisierungsoptionen 


Ansprechpartner Galdora:

Name    Nummer  Mail

Regeln: 
Nummer ist immer: 02161 6212600
Mail ist immer: [Name]@galdora.de
Umlaute immer ausschreiben: ö=oe, ä=ae, etc. 

Namen:

Alessandro Böhm
Kai Fischer
Melike Demirkol
Konrad Rusczyk
Lennard Kuss
Salim Alizai

Ausnahmen:

Email von konrad ist konrad@galdora.de

---




Ansprechpartner BeJob:

Name	Nummer 	Mail
Dirk Keulertz	02161 94 99 072	keulertz@bejob.de
Esra Karakus	02161 94 99 080	karakus@bejob.de
Seyla Saltimis	02161 94 99 081	satilmis@bejob.de
Hemat Shor	02161 94 99 069	shor@bejob.de
Daniel Fischer	02161 94 99 077	Fischer@bejob.de
Sude Savaci	02161 94 99 082	Savasci@bejob.de
Baran Gündogdu	02161 94 99 069	gündogdu@bejob.de
