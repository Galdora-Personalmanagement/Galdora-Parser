# CV2Profile Parser 📄

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://galdora-converter.streamlit.app)

Ein KI-gestützter CV-Parser, der Lebensläufe automatisch analysiert und in standardisierte Profile umwandelt.

## 🚀 Features

- **Dokumentverarbeitung**: Unterstützung für PDF, DOCX, JPG und PNG
- **KI-gestützte Analyse**: Nutzung von OpenAI zur intelligenten Datenextraktion
- **5 Template-Designs**: Classic, Modern, Professional, Elegant, Minimalist
- **Multi-Company-Support**: Galdora & BeJob mit dynamischem Logo-Switching
- **Benutzerfreundliche UI**: Moderne Streamlit-Oberfläche im Glasmorphismus-Design
- **Feature-Parität**: Manuelle Eingabe und KI-Extraktion vollständig unterstützt
- **Word & PDF Export**: Hochwertige Ausgabe in beiden Formaten

## 🎯 Live Demo

Die Anwendung ist live auf Streamlit Community Cloud verfügbar: [CV2Profile Parser](https://galdora-converter.streamlit.app)

## 🛠️ Lokale Installation

1. Repository klonen:
```bash
git clone https://github.com/jjokkln/galdora-converter.git
cd galdora-converter
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
CV2Profile Parser-40/
├── .streamlit/           # Streamlit-Konfiguration & Secrets
├── context/              # Projekt-Dokumentation 
├── src/                  # Quellcode (modularer Aufbau)
│   ├── core/            # Dokumentverarbeitung & KI-Extraktion
│   ├── templates/       # PDF-Template-Generator
│   ├── ui/              # Streamlit UI mit Glasmorphismus
│   └── utils/           # Konfiguration & Bildverwaltung
├── static/              # HTTPS-kompatible Bilder
├── main.py              # Hauptanwendung (Entry Point)
├── streamlit_app.py     # Streamlit Cloud Deployment Entry Point
├── requirements.txt     # Python-Dependencies
└── packages.txt         # System-Dependencies für Streamlit Cloud
```

## 🔧 Streamlit Cloud Deployment

Das Projekt ist deployment-ready für Streamlit Cloud:

1. **Repository verknüpfen**: https://github.com/jjokkln/galdora-converter.git
2. **Entry Point**: `streamlit_app.py` 
3. **Python Version**: 3.9+
4. **Secrets konfigurieren**: OpenAI API-Key in den App-Secrets hinzufügen

### Benötigte Secrets in Streamlit Cloud:
```toml
openai_api_key = "sk-your-openai-api-key-here"
```

## 🎨 Template-Designs

- **Classic**: Klassisches einspaltige Layout
- **Modern**: Zweispaltige Darstellung in weinrot/weiß
- **Professional**: Optimiertes Layout ohne Firmenkopf
- **Elegant**: Moderne, elegante Darstellung
- **Minimalist**: Schlankes, reduziertes Design

## 🏢 Multi-Company-Support

- **Galdora**: Vollständige Ansprechpartner-Integration
- **BeJob**: Dynamische Logo- und Kontakt-Verwaltung

## 📊 Projekt-Status

- **Gesamtfortschritt**: 94% ✅
- **Kernfunktionalitäten**: 100% ✅  
- **Template-System**: 97% ✅
- **UI/UX-Optimierungen**: 100% ✅
- **System-Stabilität**: 100% ✅
- **Deployment-Bereitschaft**: 100% ✅

## 📄 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe [LICENSE](LICENSE) Datei für Details.

## 🤝 Entwicklung

Für Entwicklungsrichtlinien siehe [CONTRIBUTING.md](context/CONTRIBUTING.md) 