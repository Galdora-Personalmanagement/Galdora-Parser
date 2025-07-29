# CV2Profile Parser-40 - Projektstruktur (Bereinigt)

```
parser-40/
├── .streamlit/                     # Streamlit-Konfiguration
│   ├── config.toml                 # UI-Einstellungen
│   └── secrets.toml                # API-Keys (nicht in Git)
│
├── context/                        # Projektdokumentation
│   ├── Archivierte_Summaries.md    # Alle alten Summaries in einer Datei
│   ├── Projektkontext.md           # Konsolidierte Projektübersicht
│   ├── Projektstruktur.md          # Diese Datei - Strukturbaum
│   └── Progress.md                 # Erledigte und offene Aufgaben
│
├── src/                           # Quellcode-Verzeichnis
│   ├── core/                      # Kernfunktionalität
│   │   ├── document_processor.py  # Dokumentenverarbeitung (PDF, DOCX, Bilder)
│   │   ├── ai_extractor.py        # KI-gestützte Informationsextraktion (OpenAI)
│   │   └── combined_processor.py  # Kombinierte Verarbeitungslogik
│   │
│   ├── templates/                 # Template-Generierung
│   │   ├── template_generator.py  # PDF-Profilgenerierung (ReportLab)
│   │   └── designs/               # Design-Vorlagen
│   │       ├── classic/           # Klassisches Design
│   │       │   └── config.json    # Design-Konfiguration
│   │       ├── modern/            # Modernes Design
│   │       │   └── config.json    # Design-Konfiguration
│   │       └── professional/      # Professionelles Design
│   │           └── config.json    # Design-Konfiguration
│   │
│   ├── ui/                        # Benutzeroberfläche
│   │   └── styles/                # CSS und Styling
│   │       ├── global_css.py      # Ältere CSS-Definitionen (zu prüfen)
│   │       └── main_styles.py     # Zentrale CSS-Definitionen für main.py
│   │
│   └── utils/                     # Hilfsfunktionen
│       ├── config.py              # Konfigurationsmanagement
│       ├── company_config.py      # Multi-Firmen-Konfiguration
│       ├── image_utils.py         # Bild-Utilities
│       └── pdf_viewer.py          # PDF.js Viewer Logik
│
├── static/                        # Statische Dateien
│   └── images/                    # HTTPS-kompatible Bilder (Logos, etc.)
│
├── .gitignore                     # Git-Ausschlüsse
├── main.py                        # Hauptanwendung & zentraler Entry Point
├── streamlit_app.py               # Streamlit Cloud Entry Point (vereinfacht)
├── run.sh                         # Startskript für lokale Entwicklung (vereinfacht)
├── requirements.txt               # Python-Abhängigkeiten (bereinigt)
├── packages.txt                   # Linux-Systemabhängigkeiten
├── README.md                      # Projekt-Readme
├── CONTRIBUTING.md                # Entwickler-Leitfaden
└── LICENSE                        # Lizenzinformationen
```

## Aktuelle Konfiguration

### Entry Points
- **Lokal**: `main.py` via `run.sh` → http://localhost:8501
- **Streamlit Cloud**: `streamlit_app.py` → `main.py`

### Hauptabhängigkeiten
- **Python**: streamlit, openai, PyPDF2, python-docx, pytesseract, reportlab, Pillow
- **System**: tesseract-ocr, tesseract-ocr-deu, poppler-utils, libgl1-mesa-glx 