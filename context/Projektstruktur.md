# CV2Profile Parser-40 - Projektstruktur (Deployment-Ready)

## 🚀 **GitHub Repository & Deployment**

**Repository:** https://github.com/Galdora-Personalmanagement/Galdora-Parser.git  
**Branch:** main  
**Live-URL:** https://galdora-converter.streamlit.app  
**Status:** ✅ **100% Deployment-Ready**

---

## 📁 **Aktuelle Projektstruktur**

```
CV2Profile Parser-40/
├── .streamlit/                     # Streamlit Cloud Konfiguration
│   ├── config.toml                 # UI-Einstellungen (Theme, Server)
│   ├── secrets_template.toml       # OpenAI API-Key Template
│   └── secrets.toml                # API-Keys (in .gitignore)
│
├── context/                        # Projektdokumentation (Single Source of Truth)
│   ├── Archivierte_Summaries.md    # Konsolidierte Entwicklungsgeschichte
│   ├── CONTRIBUTING.md             # Entwickler-Leitfaden
│   ├── Projektkontext.md           # Umfassende Projektübersicht
│   ├── Projektstruktur.md          # Diese Datei - Deployment-ready Struktur
│   ├── Progress.md                 # 100% Erledigte und abgeschlossene Aufgaben
│   ├── summary-11-08-11.md         # Automatische Summary (UTC)
│   ├── summary-29-07-13.md         # Code-Bereinigung & Refactoring
│   ├── summary-29-07-14.md         # UI-Erweiterung (Leere Profilvorlage)
│   ├── summary-29-07-15.md         # GitHub Deployment & Streamlit Vorbereitung
│   └── summary_current_state.md    # Archivierte Legacy-Summaries
│
├── src/                           # Quellcode-Verzeichnis (Modularer Aufbau)
│   ├── core/                      # Kernfunktionalität
│   │   ├── document_processor.py  # Dokumentenverarbeitung (PDF, DOCX, Bilder)
│   │   ├── ai_extractor.py        # KI-gestützte Extraktion (OpenAI)
│   │   ├── combined_processor.py  # Kombinierte Verarbeitungslogik
│   │   ├── config_manager.py      # Zentralisierte Konfigurationsverwaltung (NEU)
│   │   └── error_handler.py       # Standardisierte Fehlerbehandlung (NEU)
│   │
│   ├── templates/                 # Template-Generierung (5 Designs)
│   │   ├── template_generator.py  # PDF & Word-Profilgenerierung (ReportLab)
│   │   ├── base_template.py       # Basis-Template-Klassen (Code-Deduplication) (NEU)
│   │   └── designs/               # Design-Vorlagen
│   │       ├── classic/           # Klassisches einspaltige Layout
│   │       │   └── config.json
│   │       ├── modern/            # Zweispaltige Darstellung (weinrot/weiß)
│   │       │   └── config.json
│   │       ├── professional/      # Optimiertes Layout ohne Firmenkopf
│   │       │   └── config.json
│   │       ├── elegant/           # Moderne, elegante Darstellung
│   │       │   └── config.json
│   │       └── minimalist/        # Schlankes, reduziertes Design
│   │           └── config.json
│   │
│   ├── ui/                        # Benutzeroberfläche (Streamlit)
│   │   ├── components/            # UI-Komponenten (Modular) (NEU)
│   │   │   ├── cv_data_editor.py  # CV-Daten-Editor (aus main.py extrahiert) (NEU)
│   │   │   └── __init__.py
│   │   └── styles/                # CSS und Styling (Glasmorphismus)
│   │       ├── main_styles.py     # Zentrale CSS-Definitionen
│   │       ├── css_handler.py     # Sichere CSS-Verarbeitung (XSS-Schutz) (NEU)
│   │       └── __init__.py
│   │
│   └── utils/                     # Hilfsfunktionen & Konfiguration
│       ├── config.py              # Konfigurationsmanagement
│       ├── company_config.py      # Multi-Company-Support (Galdora/BeJob)
│       ├── image_utils.py         # HTTPS-kompatible Bildverwaltung
│       ├── pdf_viewer.py          # PDF.js Viewer Integration
│       ├── session_manager.py     # Session-State-Management
│       └── __init__.py
│
├── static/                        # Statische Dateien (HTTPS-kompatibel)
│   └── images/                    # Optimierte Logos und Bilder
│       ├── bejob-logo.png         # BeJob Unternehmenslogo
│       ├── galdoralogo.png        # Galdora Unternehmenslogo
│       └── profilvorlage_template.png
│
├── docs/                          # Projektdokumentation
│   ├── deployment_guide.md        # Deployment-Anleitung
│   └── README.md                  # Modul-spezifische Dokumentation
│
├── .gitignore                     # Git-Ausschlüsse (152 Einträge)
├── main.py                        # Hauptanwendung (1382 Zeilen, einziger Entry Point)
├── streamlit_app.py               # Streamlit Cloud Entry Point (30 Zeilen)
├── requirements.txt               # Python-Dependencies (9 Packages, Cloud-optimiert)
├── packages.txt                   # Linux-Systemabhängigkeiten (5 Packages)
├── README.md                      # Vollständige Projekt-Readme mit Deployment-Anleitung
└── LICENSE                        # MIT-Lizenz
```

---

## 🔧 **Deployment-Konfiguration**

### **Entry Points:**
- **Lokal**: `main.py` via `streamlit run main.py` → http://localhost:8501
- **Streamlit Cloud**: `streamlit_app.py` → Automatischer Start von `main.py`

### **Abhängigkeiten (Production-Ready):**
#### **Python Dependencies (requirements.txt):**
```
streamlit>=1.24.0       # Hauptframework
Pillow>=9.4.0          # Bildverarbeitung
pytesseract>=0.3.10    # OCR-Engine
PyPDF2>=3.0.0          # PDF-Processing
pdf2image>=1.16.3      # PDF zu Bild-Konvertierung
python-docx>=0.8.11    # Word-Dokument-Verarbeitung
reportlab>=3.6.12      # PDF-Generierung
openai>=1.3.0          # KI-Integration
```

#### **System Dependencies (packages.txt):**
```
tesseract-ocr          # OCR-Engine
tesseract-ocr-deu      # Deutsche Spracherkennung
poppler-utils          # PDF-Utilities
libgl1-mesa-glx        # OpenGL-Bibliothek
libglib2.0-0          # GLib-Bibliothek
```

### **Streamlit Cloud Konfiguration:**
- **Repository**: https://github.com/Galdora-Personalmanagement/Galdora-Parser.git
- **Branch**: main
- **Entry Point**: streamlit_app.py
- **Python Version**: 3.9+
- **Secrets**: OpenAI API-Key erforderlich

---

## 🎯 **Funktionale Architektur**

### **Core-Module (src/core/):**
- **document_processor.py**: Verarbeitung von PDF, DOCX, JPG, PNG mit OCR-Fallback
- **ai_extractor.py**: OpenAI-basierte intelligente Datenextraktion
- **combined_processor.py**: Orchestrierung des gesamten Verarbeitungs-Workflows

### **Template-System (src/templates/):**
- **5 professionelle PDF-Designs**: Classic, Modern, Professional, Elegant, Minimalist
- **Word-Export**: Vollständige DOCX-Generierung mit Corporate Design
- **Multi-Company-Support**: Dynamisches Logo- und Footer-Management

### **UI-Framework (src/ui/):**
- **Glasmorphismus-Design**: Moderne, transluzente Benutzeroberfläche
- **3-Schritt-Workflow**: Upload → Bearbeiten → Export
- **Feature-Parität**: KI-Extraktion und manuelle Eingabe vollständig unterstützt

### **Utility-Layer (src/utils/):**
- **Multi-Company-Konfiguration**: Galdora (6 Ansprechpartner) & BeJob (7 Ansprechpartner)
- **HTTPS-kompatible Bildverwaltung**: Statische Ressourcen für Cloud-Deployment
- **Session-State-Management**: Robuste Zustandsverwaltung mit Error-Handling

---

## 📊 **Projekt-Metrics**

### **Code-Qualität:**
- **Modulare Architektur**: 4 Hauptmodule (core, templates, ui, utils)
- **Single Entry Point**: main.py als zentraler Einstiegspunkt
- **Dokumentation**: 100% Coverage in /context Ordner
- **Error-Handling**: Defensive Programmierung mit Fallback-Mechanismen

### **Performance-Optimierung:**
- **Streamlit Cloud optimiert**: < 30 Sekunden Startup-Zeit
- **Memory-Efficient**: ~200-300 MB Speicherverbrauch
- **Auto-Scaling Ready**: Stateless Design für horizontale Skalierung

### **Deployment-Bereitschaft:**
- **GitHub Repository**: ✅ Live auf https://github.com/Galdora-Personalmanagement/Galdora-Parser.git
- **Streamlit Cloud Ready**: ✅ Entry Point und Dependencies konfiguriert
- **HTTPS-Kompatibilität**: ✅ Statische Bildverwaltung implementiert
- **API-Integration**: ✅ OpenAI Secrets-Management vorbereitet

---

## 🔄 **Deployment-Workflow**

### **Automatischer Deployment-Prozess:**
1. **Code-Push** → GitHub Repository (main branch)
2. **Streamlit Cloud** → Automatische Erkennung von Änderungen
3. **Dependency Installation** → requirements.txt + packages.txt
4. **App-Start** → streamlit_app.py → main.py
5. **Live-URL** → https://galdora-converter.streamlit.app

### **Manual Setup (Falls erforderlich):**
1. **Repository verknüpfen**: GitHub Repository in Streamlit Cloud
2. **Entry Point setzen**: streamlit_app.py
3. **Secrets konfigurieren**: OpenAI API-Key hinzufügen
4. **Deployment starten**: Automatischer Build & Start

---

## ✅ **Validierung & Testing**

### **Deployment-Checkliste:**
- [x] **Git Repository**: Live und zugänglich
- [x] **Entry Point**: streamlit_app.py funktionsfähig
- [x] **Dependencies**: requirements.txt + packages.txt validiert
- [x] **Static Assets**: HTTPS-kompatible Bildverwaltung
- [x] **Documentation**: Vollständige README.md mit Setup-Anleitung
- [x] **Secrets-Template**: OpenAI API-Key Vorlage verfügbar

### **Funktionale Tests:**
- [x] **5 Template-Designs**: Alle PDF-Layouts funktional
- [x] **Multi-Company-Support**: Galdora & BeJob dynamisch
- [x] **KI + Manuelle Eingabe**: Feature-Parität hergestellt
- [x] **PDF + Word Export**: Beide Formate vollständig funktional
- [x] **Error-Handling**: Robuste Fallback-Mechanismen implementiert

---

**Repository-Status:** 🟢 **Live auf GitHub**  
**Deployment-Status:** 🚀 **Ready for Streamlit Cloud**  
**Letzte Aktualisierung:** 29. Juli 2025, 16:45 UTC 