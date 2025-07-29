# Contributing to CV2Profile Parser

Vielen Dank für dein Interesse, an diesem Projekt mitzuwirken! Diese Anleitung hilft dir dabei, den Code zu verstehen, Änderungen sicher vorzunehmen und die Projektstruktur beizubehalten.

## 🚀 Projektphilosophie

Das Projekt folgt klaren Prinzipien, um es wartbar und erweiterbar zu halten:

1.  **Zentraler Entry Point:** Die gesamte Anwendungslogik wird über `main.py` gesteuert. Es gibt keine versteckten oder alternativen Startpunkte.
2.  **Klare Modultrennung:** Der Code ist streng nach Verantwortlichkeiten getrennt (`core`, `templates`, `ui`, `utils`).
3.  **Konfiguration vor Code:** Einstellungen (wie API-Keys oder Firmen-spezifische Daten) werden in den `utils`-Modulen zentral verwaltet und nicht hart im Code verankert.
4.  **Dokumentation als Teil des Codes:** Der `context`-Ordner ist die "Single Source of Truth" für das Projektverständnis. Jede größere Änderung muss dort dokumentiert werden.

---

## 🏗️ Architektur-Überblick

Die Projektstruktur ist wie folgt aufgeteilt:

-   **`main.py`**: Der einzige Einstiegspunkt der Anwendung. Diese Datei enthält die gesamte Streamlit-UI-Logik, steuert den Workflow und ruft die Backend-Module auf.
-   **`src/core/`**: Das "Gehirn" der Anwendung. Hier findet die gesamte Datenverarbeitung statt, von der Textextraktion aus Dokumenten (`document_processor.py`) bis zur KI-gestützten Analyse (`ai_extractor.py`).
-   **`src/templates/`**: Verantwortlich für die Erstellung der finalen PDF-Profile. `template_generator.py` ist die zentrale Logik, die auf die Konfigurationen im `designs/`-Ordner zugreift, um unterschiedliche Layouts zu erzeugen.
-   **`src/ui/`**: Enthält ausschließlich UI-bezogene Elemente, hauptsächlich die ausgelagerten CSS-Stile in `styles/`.
-   **`src/utils/`**: Beinhaltet Hilfsmodule für Konfiguration (`config.py`), firmenspezifische Anpassungen (`company_config.py`), Bildverarbeitung (`image_utils.py`) und die PDF-Vorschau (`pdf_viewer.py`).
-   **`context/`**: Das Dokumentationszentrum. Änderungen an der Codebasis müssen hier in `Projektstruktur.md` und `Progress.md` nachvollzogen werden.

---

## 🛠️ Wie man Änderungen vornimmt (Workflow)

Folge diesen Schritten, um sicherzustellen, dass deine Änderungen konsistent und sicher sind.

### 1. Lokales Setup

1.  **Aktiviere die Umgebung:** Führe immer `./run.sh` im Terminal aus. Das Skript aktiviert die `venv` und startet die Streamlit-Anwendung.
2.  **Analysiere den Kontext:** Lies die drei Kerndateien in `context/`, um den aktuellen Stand des Projekts vollständig zu verstehen.

### 2. Typische Änderungen

-   **Du möchtest die Benutzeroberfläche ändern?**
    -   Alle UI-Elemente (Knöpfe, Tabs, Uploader) sind in `main.py` definiert.
    -   Styling-Anpassungen (Farben, Layout, Schriftarten) gehören in `src/ui/styles/main_styles.py`.

-   **Du möchtest die KI-Extraktion verbessern?**
    -   Die Logik dafür befindet sich ausschließlich in `src/core/ai_extractor.py`.
    -   Die Prompts und die Interaktion mit der OpenAI-API werden hier gesteuert.

-   **Du möchtest ein PDF-Template anpassen oder hinzufügen?**
    -   Die Logik zur PDF-Generierung liegt in `src/templates/template_generator.py`.
    -   Für Design-Anpassungen (z.B. Farben, Schriftarten für ein bestimmtes Template) ändere die entsprechende `config.json` im `src/templates/designs/`-Unterordner.
    -   Um ein neues Template hinzuzufügen, erstelle einen neuen Ordner mit `config.json` und implementiere die zugehörige Logik in `template_generator.py`.

-   **Du möchtest eine Abhängigkeit hinzufügen?**
    -   Füge das Paket zur `requirements.txt` hinzu. Teste gründlich, ob die neue Abhängigkeit keine Konflikte verursacht.

### 3. Goldene Regeln (Um nichts kaputtzumachen)

-   **ÄNDERE NICHT** den Startmechanismus. `run.sh` und `streamlit_app.py` müssen auf `main.py` verweisen.
-   **ERSTELLE KEINE** neuen `.py`-Dateien im Hauptverzeichnis. Neue Logik gehört in die `src/`-Module.
-   **VERMEIDE** monolithische Dateien. Wenn eine Funktion in `main.py` zu groß wird, lagere sie in ein passendes Modul in `src/utils/` oder ein neues UI-Komponenten-Modul aus.
-   **AKTUALISIERE IMMER** die `context/`-Dateien nach deinen Änderungen (Summary, Progress, Projektstruktur).

---

## ✅ Testen

Bevor du deine Änderungen als abgeschlossen betrachtest, teste den gesamten Workflow lokal:

1.  Starte die App mit `./run.sh`.
2.  Lade ein Test-Dokument hoch.
3.  Überprüfe die KI-Extraktion und die Bearbeitungsfunktionen.
4.  Generiere eine PDF-Vorschau und lade die Datei herunter.
5.  Stelle sicher, dass keine Fehler in der Terminal-Konsole auftreten.

Indem du diesem Leitfaden folgst, stellst du sicher, dass das Projekt stabil, sauber und für alle Beteiligten verständlich bleibt. 