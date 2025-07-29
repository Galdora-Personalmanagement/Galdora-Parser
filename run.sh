#!/bin/bash

# CV2Profile Starter-Skript - Vereinfacht

# Aktiviere die virtuelle Umgebung, falls sie existiert
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Python-Pfad festlegen, damit Module korrekt gefunden werden
export PYTHONPATH="$PWD:$PYTHONPATH"

# Starte die Hauptanwendung
echo "Starte CV2Profile..."
streamlit run main.py

# Deaktiviere die virtuelle Umgebung, falls aktiviert
if [ -n "$VIRTUAL_ENV" ]; then
    deactivate
fi 