"""
Globale CSS-Stile für die CV2Profile-Anwendung.

Diese Datei enthält alle CSS-Definitionen, die in der gesamten Anwendung verwendet werden.
Der CSS-Code wurde aus app.py und 01_Konverter.py extrahiert, um Redundanz zu vermeiden.
"""

# CSS für Farbverlaufshintergrund und weiße Schaltflächen
custom_css = """
<style>
    /* Farbverlaufshintergrund für die gesamte Seite */
    .main, .stApp {
        background: linear-gradient(135deg, #4527A0, #7B1FA2) !important;
        background-size: cover !important;
        background-attachment: fixed !important;
    }
    
    /* Transparente Container */
    .css-18e3th9, .css-1d391kg, .css-12oz5g7 {
        background: transparent !important;
    }
    
    /* Glasmorphismus-Schaltflächen im Apple-Stil */
    button, .stButton > button, .stDownloadButton > button {
        background: rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
    }
    
    /* Hover-Effekt für Glasmorphismus-Schaltflächen */
    button:hover, .stButton > button:hover {
        background: rgba(255, 255, 255, 0.3) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15) !important;
    }
    
    /* Hervorhebung des Buttontexts für bessere Lesbarkeit */
    .stButton > button p, button p, .stDownloadButton > button p {
        color: white !important;
        font-weight: 600 !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* File Uploader gestalten */
    .stFileUploader > div {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        color: white !important;
        border: 2px dashed rgba(255, 255, 255, 0.3) !important;
        backdrop-filter: blur(5px) !important;
        -webkit-backdrop-filter: blur(5px) !important;
    }
    
    /* Browse-Files Button */
    .stFileUploader button, button.css-1aumxhk, .css-1aumxhk {
        background: rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1rem !important;
        text-transform: none !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        margin-left: auto !important;
        margin-right: auto !important;
        display: block !important;
    }
    
    /* Browse files Button Hover-Effekt */
    button.css-1aumxhk:hover, .css-1aumxhk:hover {
        background: rgba(255, 255, 255, 0.3) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15) !important;
    }
    
    /* Textfarbe für die Hauptseite auf weiß setzen */
    .stMarkdown, .stText, h1, h2, h3, p, span, div {
        color: white !important;
    }
    
    /* Textfarbe für interaktive Elemente anpassen */
    button span, .stButton span, .stDownloadButton span, 
    button div, .stButton div, .stDownloadButton div {
        color: white !important;
        font-weight: 600 !important;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* Fix für Button-Text-Farbe */
    .stButton > button:hover span, .stButton > button:hover p, 
    button:hover span, button:hover p {
        color: white !important;
    }
    
    /* Sidebar dunkler gestalten */
    [data-testid="stSidebar"] {
        background-color: rgba(20, 20, 26, 0.8) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
    }
    
    /* Sidebar Elemente */
    .sidebar .sidebar-content {
        background-color: transparent !important;
    }
    
    /* Selectboxen im Glasdesign */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
    }
    
    /* Inputs im Glasdesign */
    input, textarea, [data-baseweb="input"], [data-baseweb="textarea"] {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        backdrop-filter: blur(5px) !important;
        -webkit-backdrop-filter: blur(5px) !important;
    }
    
    /* Platzhalter-Text für Inputs */
    input::placeholder, textarea::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
    }
    
    /* Schatten für Cards/Container mit Glaseffekt */
    .element-container {
        margin-bottom: 1em !important;
    }
    
    /* Footer-Bereich */
    footer {
        color: white !important;
        visibility: visible !important;
    }
    
    /* Footer-Links */
    footer a {
        color: white !important;
        text-decoration: underline !important;
    }
    
    /* Weißer Text für Labels */
    label {
        color: white !important;
    }
    
    /* Drop-Zone */
    .css-1n543e5, .css-183lzff {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        backdrop-filter: blur(5px) !important;
        -webkit-backdrop-filter: blur(5px) !important;
    }
    
    /* Fix für selectbox drop-down menu */
    .stSelectbox div[data-baseweb="select"] ul {
        background: rgba(69, 39, 160, 0.9) !important;
        color: white !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
    }
    
    /* Verbesserte Dropdown-Menüs */
    /* Dropdown-Hauptcontainer */
    .stSelectbox div[data-baseweb="select"] {
        background: rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.3s ease !important;
    }
    
    /* Dropdown wenn aktiv/hover */
    .stSelectbox div[data-baseweb="select"]:hover, 
    .stSelectbox div[data-baseweb="select"]:focus {
        background: rgba(255, 255, 255, 0.2) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15) !important;
    }
    
    /* Dropdown-Liste */
    .stSelectbox div[data-baseweb="select"] ul {
        background: rgba(45, 25, 100, 0.95) !important;
        border-radius: 12px !important;
        padding: 8px !important;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* Dropdown-Listenelemente */
    .stSelectbox div[data-baseweb="select"] ul li {
        color: white !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
    }
    
    /* Dropdown-Listenelemente Hover */
    .stSelectbox div[data-baseweb="select"] ul li:hover {
        background: rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Dropdown-Listenelemente Aktiv */
    .stSelectbox div[data-baseweb="select"] ul li[aria-selected="true"] {
        background: rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Textareas im Glasdesign */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-radius: 12px !important;
        backdrop-filter: blur(5px) !important;
        -webkit-backdrop-filter: blur(5px) !important;
        border: none !important;
        padding: 15px !important;
    }
    
    /* Checkbox-Container im Glasdesign */
    .stCheckbox {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        padding: 15px !important;
        backdrop-filter: blur(5px) !important;
        -webkit-backdrop-filter: blur(5px) !important;
    }
    
    /* Checkbox im Glasdesign */
    .stCheckbox div[role="checkbox"] {
        background: rgba(255, 255, 255, 0.2) !important;
        border: none !important;
    }
    
    /* Radiobutton-Container im Glasdesign */
    .stRadio {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        padding: 15px !important;
        backdrop-filter: blur(5px) !important;
        -webkit-backdrop-filter: blur(5px) !important;
    }
    
    /* Texte in Tabs */
    .stTabs [data-baseweb="tab"] {
        color: white !important;
    }
    
    /* Tab-Container */
    .stTabs {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(5px) !important;
        -webkit-backdrop-filter: blur(5px) !important;
        padding: 5px !important;
    }
    
    /* Active Tab */
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
    }
    
    /* Container für Widgets mit Glaseffekt */
    .widget-container {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        backdrop-filter: blur(5px) !important;
        -webkit-backdrop-filter: blur(5px) !important;
        margin-bottom: 20px !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
    }
    
    /* Container für Profile */
    .profile-container {
        background: rgba(255, 255, 255, 0.05) !important;
        border-radius: 20px !important;
        padding: 25px !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Hervorgehobene Informationen */
    .highlight-info {
        background: rgba(255, 255, 255, 0.15) !important;
        border-left: 4px solid rgba(255, 255, 255, 0.3) !important;
        padding: 15px !important;
        border-radius: 0 12px 12px 0 !important;
        margin: 15px 0 !important;
    }
    
    /* Animierter Button für wichtige Aktionen */
    .primary-action-btn {
        background: linear-gradient(45deg, #6200EA, #BA68C8) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 4px 15px rgba(98, 0, 234, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    /* Hover-Effekt für animierten Button */
    .primary-action-btn:hover {
        background: linear-gradient(45deg, #7C4DFF, #D1C4E9) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 7px 20px rgba(124, 77, 255, 0.4) !important;
    }
    
    /* Expander im Glasdesign */
    .stExpander {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        border: none !important;
        overflow: hidden !important;
        backdrop-filter: blur(5px) !important;
        -webkit-backdrop-filter: blur(5px) !important;
    }
    
    /* Expander-Header */
    .stExpander > div:first-child {
        background: rgba(255, 255, 255, 0.05) !important;
        border: none !important;
    }
    
    /* Data-Editor im Glasdesign */
    .stDataFrame {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(5px) !important;
        -webkit-backdrop-filter: blur(5px) !important;
        overflow: hidden !important;
    }
    
    /* Tabellen-Header */
    .stDataFrame th {
        background: rgba(255, 255, 255, 0.2) !important;
        color: white !important;
    }
    
    /* Tabellen-Zellen */
    .stDataFrame td {
        background: transparent !important;
        color: white !important;
        border-color: rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Slider im Glasdesign */
    .stSlider {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        padding: 20px !important;
        backdrop-filter: blur(5px) !important;
        -webkit-backdrop-filter: blur(5px) !important;
    }
    
    /* Slider-Thumb */
    .stSlider div[role="slider"] {
        background: white !important;
        border: 2px solid rgba(255, 255, 255, 0.8) !important;
    }
    
    /* Fix für Download-Button */
    .stDownloadButton button {
        width: auto !important;
        background: rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1rem !important;
        text-transform: none !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
    }
    
    /* Fix für Download-Button Hover */
    .stDownloadButton button:hover {
        background: rgba(255, 255, 255, 0.3) !important;
        color: white !important;
    }
    
    /* Fix für Streamlit-Debug-Fehler-Box */
    .element-container .stException {
        background: rgba(255, 0, 0, 0.1) !important;
        border-radius: 12px !important;
        padding: 15px !important;
        backdrop-filter: blur(5px) !important;
        -webkit-backdrop-filter: blur(5px) !important;
        color: white !important;
    }
    
    .stSidebar {
        width: 336px !important;
        min-width: 336px !important;
        transition: none !important;
    }
    
    .stFileUploader {
        min-height: 100px;
        transition: none;
    }
</style>
"""

def apply_css():
    """
    Wendet den globalen CSS-Stil auf die Streamlit-Anwendung an.
    """
    import streamlit as st
    st.markdown(custom_css, unsafe_allow_html=True) 