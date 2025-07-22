# CV2Profile Parser-40 - Projektstruktur

```
parser-40/
├── .streamlit/                     # Streamlit-Konfiguration
│   ├── config.toml                 # UI-Einstellungen
│   ├── secrets.toml                # API-Keys (nicht in Git)
│   └── secrets_template.toml       # Vorlage für secrets.toml
│
├── context/                        # Projektdokumentation (BEREINIGT)
│   ├── Projektkontext.md           # Konsolidierte Projektübersicht
│   ├── Projektstruktur.md          # Diese Datei - Strukturbaum
│   └── Progress.md                 # Erledigte und offene Aufgaben
│
├── src/                           # Quellcode-Verzeichnis
│   ├── core/                      # Kernfunktionalität
│   │   ├── __init__.py            # Package-Initialisierung
│   │   ├── document_processor.py  # Dokumentenverarbeitung (PDF, DOCX, Bilder)
│   │   ├── ai_extractor.py        # KI-gestützte Informationsextraktion (OpenAI)
│   │   └── combined_processor.py  # Kombinierte Verarbeitungslogik
│   │
│   ├── templates/                 # Template-Generierung
│   │   ├── __init__.py            # Package-Initialisierung
│   │   ├── template_generator.py  # PDF-Profilgenerierung (ReportLab)
│   │   └── designs/               # Design-Vorlagen
│   │       ├── README.md          # Design-Dokumentation
│   │       ├── classic/           # Klassisches Design
│   │       │   ├── config.json    # Design-Konfiguration
│   │       │   └── README.md      # Design-Beschreibung
│   │       ├── modern/            # Modernes Design (zweispaltig, weinrot/weiß)
│   │       │   ├── config.json    # Design-Konfiguration
│   │       │   ├── README.md      # Design-Beschreibung
│   │       │   ├── modern-preview.png      # Vorschaubild
│   │       │   └── profilvorlage-modern.pdf # Beispiel-PDF
│   │       ├── professional/      # Professionelles Design
│   │       │   ├── config.json    # Design-Konfiguration
│   │       │   ├── README.md      # Design-Beschreibung
│   │       │   ├── professional-preview-1.png # Vorschaubild Seite 1
│   │       │   ├── professional-preview-2.png # Vorschaubild Seite 2
│   │       │   └── profilvorlage-professional.pdf # Beispiel-PDF
│   │       ├── elegant/           # Elegantes Design
│   │       │   ├── config.json    # Design-Konfiguration
│   │       │   └── README.md      # Design-Beschreibung
│   │       └── minimalist/        # Minimalistisches Design
│   │           ├── config.json    # Design-Konfiguration
│   │           └── README.md      # Design-Beschreibung
│   │
│   ├── ui/                        # Benutzeroberfläche
│   │   ├── __init__.py            # Package-Initialisierung
│   │   ├── Home.py                # Homepage der Anwendung
│   │   ├── app.py                 # Hauptanwendung (1415 Zeilen)
│   │   ├── pages/                 # Zusätzliche Seiten
│   │   │   ├── README.md          # Seiten-Dokumentation
│   │   │   ├── 01_Konverter.py    # Hauptkonverter-Seite
│   │   │   └── 01_⚙️_Einstellungen.py # Einstellungen-Seite
│   │   ├── styles/                # CSS und Styling
│   │   │   └── global_css.py      # Zentrale CSS-Definitionen (Glasmorphismus)
│   │   └── utils/                 # UI-Hilfsfunktionen
│   │       └── ui_helpers.py      # UI-Hilfsfunktionen (geplant)
│   │
│   ├── utils/                     # Hilfsfunktionen
│   │   ├── __init__.py            # Package-Initialisierung
│   │   ├── config.py              # Konfigurationsmanagement (API-Keys, Settings)
│   │   └── image_utils.py         # Bild-Utilities für HTTPS-Kompatibilität
│   │
│   └── __init__.py               # Hauptpackage-Initialisierung
│
├── static/                        # Statische Dateien
│   └── images/                    # HTTPS-kompatible Bilder
│       ├── galdoralogo.png        # Firmenlogo für PDFs
│       ├── cv2profile-logo.png    # Anwendungslogo
│       ├── Profilvorlage Seite 1.png # Design-Vorschau
│       └── Profilvorlage Seite 2.png # Design-Vorschau
│
├── sources/                       # Original-Ressourcen
│   ├── galdoralogo.png           # Original-Firmenlogo
│   ├── cv2profile-logo.png       # Original-Anwendungslogo
│   ├── Profilvorlage Seite 1.png # Original-Designvorlagen
│   └── Profilvorlage Seite 2.png # Original-Designvorlagen
│
├── docs/                          # Zusätzliche Dokumentation
│
├── venv/                          # Virtuelle Python-Umgebung
│
├── .gitignore                     # Git-Ausschlüsse
├── streamlit_app.py               # Streamlit Cloud Entry Point
├── main.py                        # Lokaler Einstiegspunkt (1415 Zeilen)
├── run.sh                         # Startskript für lokale Entwicklung
├── pre_deploy.sh                  # Deployment-Vorbereitung
├── requirements.txt               # Python-Abhängigkeiten
├── packages.txt                   # Linux-Systemabhängigkeiten (Tesseract, Poppler)
├── README.md                      # Projekt-Readme
└── LICENSE                        # Lizenzinformationen
```

## Aktuelle Konfiguration

### Entry Points
- **Lokal**: `main.py` via `run.sh` → http://localhost:8501
- **Streamlit Cloud**: `streamlit_app.py` → Automatisches Deployment

### Hauptabhängigkeiten
- **Python**: streamlit, openai, PyPDF2, python-docx, pytesseract, reportlab, Pillow
- **System**: tesseract-ocr, tesseract-ocr-deu, poppler-utils, libgl1-mesa-glx

### Designkonfiguration
Jedes Template-Design in `src/templates/designs/` enthält:
- `config.json`: Farbschema, Schriftarten, Versionsinfo
- `README.md`: Implementierungsdetails und Verwendung
- Vorschaubilder und Beispiel-PDFs (bei verfügbaren Designs)

### Aktuelle Template-Status
- ✅ **Classic**: Vollständig implementiert, einspaltig
- ✅ **Modern**: Vollständig implementiert, zweispaltig weinrot/weiß
- ✅ **Professional**: Neu optimiert (v4), ohne Firmenkopf, vergrößertes Logo
- ✅ **Elegant**: Basis implementiert
- ✅ **Minimalist**: Basis implementiert

## Deployment-Bereitschaft
- **GitHub Repository**: https://github.com/jjokkln/Parser-Streamlit-Host.git
- **Branch**: new-v4 (deployment-ready)
- **Cloud-Kompatibilität**: HTTPS-ready, dependency-complete
- **Secrets Management**: Template für OpenAI API-Key vorhanden 