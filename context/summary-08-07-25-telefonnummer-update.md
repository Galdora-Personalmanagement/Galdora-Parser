# CV2Profile Parser-40 - Telefonnummer-Update (25.07.2025)

## Durchgeführte Änderungen

### Standardisierung der Telefonnummern

- **Änderung**: Für alle Ansprechpartner außer Salim Alizai wurde die Telefonnummer auf "02161 62126-00" standardisiert
- **Betroffene Dateien**: `src/templates/template_generator.py`
- **Betroffene Funktionen**:
  - `_create_classic_content`: PDF-Generierung
  - `_create_classic_docx_content`: DOCX-Generierung

### Technische Implementierung

In beiden Funktionen wurde die Logik für die Telefonnummer-Zuweisung wie folgt angepasst:

```python
# Standard-Telefonnummer für alle außer Salim Alizai
if ansprechpartner == "Salim Alizai":
    telefon = kontakt.get('telefon', '')
else:
    telefon = "02161 62126-00"
```

### Vorteile der Änderung

- **Konsistenz**: Einheitliche Telefonnummer für die meisten Ansprechpartner
- **Aktualität**: Sicherstellung, dass die neueste Kontaktnummer verwendet wird
- **Ausnahmebehandlung**: Spezielle Behandlung für Salim Alizai, der seine individuelle Nummer behält
- **Wartbarkeit**: Zentralisierte Änderung an zwei Stellen statt verstreuter Telefonnummern

### Betroffene Ausgabeformate

- **PDF-Dokumente**: Alle generierten PDF-Profile zeigen die aktualisierte Telefonnummer
- **DOCX-Dokumente**: Alle generierten Word-Dokumente zeigen die aktualisierte Telefonnummer

### Nächste Schritte

- Überprüfung der generierten Dokumente zur Bestätigung der korrekten Anzeige
- Information der Benutzer über die Standardisierung der Kontaktdaten
- Erwägung einer zentralisierten Konfigurationsdatei für Kontaktinformationen für zukünftige Änderungen 