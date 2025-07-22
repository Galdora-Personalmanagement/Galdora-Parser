# CV2Profile Parser 📄

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

Ein KI-gestützter CV-Parser, der Lebensläufe automatisch analysiert und in standardisierte Profile umwandelt.

## 🚀 Features

- **Dokumentverarbeitung**: Unterstützung für PDF, DOCX, JPG und PNG
- **KI-gestützte Analyse**: Nutzung von OpenAI zur intelligenten Datenextraktion
- **Template-Generierung**: Professionelle PDF-Profile in verschiedenen Designs
- **Benutzerfreundliche UI**: Moderne Streamlit-Oberfläche im Glasmorphismus-Design
- **Anonymisierung**: Option zur Anonymisierung persönlicher Daten

## 🎯 Live Demo

Die Anwendung ist live auf Streamlit Community Cloud verfügbar: [CV2Profile Parser](https://your-app-url.streamlit.app)

## 🛠️ Lokale Installation

1. Repository klonen:
```bash
git clone https://github.com/jjokkln/Parser-Streamlit-Host.git
cd Parser-Streamlit-Host
```

2. Virtuelle Umgebung erstellen:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# oder venv\Scripts\activate  # Windows
```

3. Dependencies installieren:
```bash
pip install -r requirements.txt
```

4. OpenAI API-Key einrichten:
   - Erstelle `.streamlit/secrets.toml` basierend auf `secrets_template.toml`
   - Füge deinen OpenAI API-Key hinzu

5. App starten:
```bash
streamlit run streamlit_app.py
```

## 📁 Projektstruktur

```
CV2Profile/
├── src/
│   ├── core/           # Kernfunktionalität
│   ├── templates/      # PDF-Template-Generator
│   ├── ui/            # Streamlit UI
│   └── utils/         # Hilfsfunktionen
├── static/            # Statische Dateien
├── .streamlit/        # Streamlit-Konfiguration
├── streamlit_app.py   # Haupteinstiegspunkt
├── requirements.txt   # Python-Dependencies
└── packages.txt       # Linux-Dependencies
```

## 🔧 Konfiguration

### OpenAI API-Key

Erstelle `.streamlit/secrets.toml`:
```toml
openai_api_key = "your-openai-api-key-here"

[general]
default_template = "Klassisch"
show_extracted_text = false
```

### Templates

Verfügbare Design-Vorlagen:
- **Klassisch**: Einspaltige Standardvorlage
- **Modern**: Zweispaltiges Design in weinrot/weiß
- **Professionell**: Business-Design mit subtiler Farbgebung
- **Minimalistisch**: Reduziertes, klares Layout

## 📧 Support

Bei Fragen oder Problemen erstelle bitte ein Issue auf GitHub.

## 📄 Lizenz

Siehe [LICENSE](LICENSE) Datei für Details. 