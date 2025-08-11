"""
PDF Viewer-Komponente mit PDF.js für bessere Web-Kompatibilität
"""
import streamlit as st
import streamlit.components.v1 as components
import base64
import os

def create_pdfjs_viewer(pdf_path: str, height: int = 600) -> str:
    """
    Erstellt einen PDF.js-basierten Viewer für bessere Web-Kompatibilität
    Optimiert für A4-Format mit korrektem Seitenverhältnis
    
    Args:
        pdf_path: Pfad zur PDF-Datei
        height: Höhe des Viewers in Pixeln (wird automatisch für A4 angepasst)
    
    Returns:
        HTML-String für den PDF-Viewer
    """
    
    if not os.path.exists(pdf_path):
        return f"""
        <div style="text-align: center; padding: 20px; background-color: #f8d7da; color: #721c24; border-radius: 5px;">
            <h4>PDF-Datei nicht gefunden</h4>
            <p>Bitte generieren Sie zuerst eine Vorschau.</p>
        </div>
        """
    
    # Leichtgewichtige Vorschau ohne PDF.js/BASE64 (speicherschonend)
    a4_ratio = 297 / 210
    viewer_width = 595
    viewer_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>PDF Vorschau (leicht)</title>
        <style>
            body { margin:0; padding:0; background:#f5f5f5; font-family: Arial, sans-serif; }
            #container { width:{viewer_width}px; margin: 20px auto; }
            #notice { background:white; padding:16px; border-radius:8px; text-align:center; }
        </style>
    </head>
    <body>
        <div id="container">
            <div id="notice">
                <h4>Vorschau deaktiviert (speicherschonend)</h4>
                <p>Bitte nutzen Sie den Download-Button in der App, um die PDF zu öffnen.</p>
            </div>
        </div>
    </body>
    </html>
    """
    return viewer_html

    # PDF-Datei als Base64 einlesen
    try:
        # Streamlit Cloud has tight RAM; avoid loading entire PDF when large.
        # Cap embedded preview to first ~10MB; if larger, show iframe fallback without base64.
        file_size = os.path.getsize(pdf_path)
        if file_size > 10 * 1024 * 1024:
            pdf_base64 = None
        else:
            with open(pdf_path, "rb") as pdf_file:
                pdf_base64 = base64.b64encode(pdf_file.read()).decode()
    except Exception as e:
        return f"""
        <div style="text-align: center; padding: 20px; background-color: #f8d7da; color: #721c24; border-radius: 5px;">
            <h4>Fehler beim Laden der PDF-Datei</h4>
            <p>{str(e)}</p>
        </div>
        """
    
    # A4-Seitenverhältnis: 210mm x 297mm = 1:1.414
    # Optimale Darstellung für A4-Format
    a4_ratio = 297 / 210  # Höhe/Breite = 1.414
    viewer_width = 595  # Optimale Breite für A4-Darstellung
    viewer_height = int(viewer_width * a4_ratio) + 80  # +80 für Controls
    
    # PDF.js-basierter Viewer mit A4-optimierten Dimensionen
    viewer_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>PDF Viewer - A4 Format</title>
        <style>
            body {{
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
                background-color: #f5f5f5;
                display: flex;
                flex-direction: column;
                align-items: center;
            }}
            #pdfViewer {{
                width: {viewer_width}px;
                height: {viewer_height - 80}px;
                border: none;
                border-radius: 0;
                background-color: transparent;
                box-shadow: none;
                display: flex;
                justify-content: center;
                align-items: center;
                overflow: hidden;
                padding: 0;
                margin: 0;
            }}
            #controls {{
                width: {viewer_width}px;
                margin-bottom: 5px;
                padding: 8px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 0;
                color: white;
                display: flex;
                justify-content: space-between;
                align-items: center;
                box-sizing: border-box;
            }}
            button {{
                background: rgba(255,255,255,0.2);
                border: 1px solid rgba(255,255,255,0.3);
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                cursor: pointer;
                transition: background 0.3s;
                font-size: 12px;
            }}
            button:hover {{
                background: rgba(255,255,255,0.3);
            }}
            button:disabled {{
                opacity: 0.5;
                cursor: not-allowed;
            }}
            #pageInfo {{
                font-weight: bold;
                font-size: 14px;
            }}
            #downloadBtn {{
                background: rgba(40, 167, 69, 0.8);
                border: 1px solid rgba(40, 167, 69, 1);
            }}
            #downloadBtn:hover {{
                background: rgba(40, 167, 69, 1);
            }}
                         #canvas {{
                 width: 100%;
                 height: 100%;
                 box-shadow: none;
                 background: white;
                 display: block;
             }}
            #zoomLevel {{
                font-weight: bold;
                margin: 0 10px;
                min-width: 50px;
                text-align: center;
            }}
            .control-group {{
                display: flex;
                align-items: center;
                gap: 5px;
            }}
            #formatInfo {{
                position: absolute;
                top: 5px;
                right: 10px;
                background: rgba(0,0,0,0.7);
                color: white;
                padding: 3px 8px;
                border-radius: 3px;
                font-size: 10px;
                z-index: 10;
            }}
        </style>
    </head>
    <body>
        <div id="controls">
            <div class="control-group">
                <button id="prevBtn" onclick="prevPage()">← Vorherige</button>
                <span id="pageInfo">Lade PDF...</span>
                <button id="nextBtn" onclick="nextPage()">Nächste →</button>
            </div>
            <div class="control-group">
                <button id="zoomOut" onclick="zoomOut()">−</button>
                <span id="zoomLevel">100%</span>
                <button id="zoomIn" onclick="zoomIn()">+</button>
                <button id="fitPage" onclick="fitToPage()">📐 A4</button>
                <button id="downloadBtn" onclick="downloadPDF()">📥 Download</button>
            </div>
        </div>
        
        <div id="pdfViewer">
            <div id="formatInfo">A4-Format</div>
            <canvas id="canvas"></canvas>
        </div>

        <!-- PDF.js from CDN mit Fallback -->
        <script>
            // Fallback für Streamlit Cloud: Einfachere PDF-Darstellung ohne externe CDNs
            if (typeof pdfjsLib === 'undefined' || {str(pdf_base64 is None).lower()}) {{
                // Direkter Iframe-Fallback für bessere Kompatibilität
                document.addEventListener('DOMContentLoaded', function() {{
                    const pdfViewer = document.getElementById('pdfViewer');
                    pdfViewer.innerHTML = `
                        <iframe 
                            src={"'data:application/pdf;base64," + pdf_base64 + "'" if pdf_base64 else f"'file://{pdf_path}'"} 
                            width="100%" 
                            height="100%" 
                            style="border: none; background: white;"
                            title="PDF-Vorschau A4-Format">
                            <div style="text-align: center; padding: 20px;">
                                <h4>PDF-Vorschau</h4>
                                <p>Ihr Browser unterstützt keine eingebettete PDF-Anzeige.</p>
                                <button onclick="downloadPDF()" style="background: #28a745; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">
                                    📥 PDF herunterladen
                                </button>
                            </div>
                        </iframe>
                    `;
                    // Controls verstecken bei Fallback
                    document.getElementById('controls').style.display = 'none';
                }});
                return;
            }}
        </script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js" 
                onerror="console.log('PDF.js CDN failed, using fallback')"></script>
        
        <script>
            // PDF.js Konfiguration mit Fallback
            if (typeof pdfjsLib !== 'undefined' && {str(pdf_base64 is not None).lower()}) {{
                pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
            }}
            
            let pdfDoc = null;
            let currentPage = 1;
            let scale = 1.0;
            const canvas = document.getElementById('canvas');
            const ctx = canvas.getContext('2d');
            
            // A4-Dimensionen für optimale Darstellung
            const A4_WIDTH = 595;   // Punkte
            const A4_HEIGHT = 842;  // Punkte
            const VIEWER_WIDTH = {viewer_width - 40};  // Container-Breite minus Padding
            const VIEWER_HEIGHT = {viewer_height - 120}; // Container-Höhe minus Controls und Padding
            
            // Base64 PDF-Daten
            const pdfData = { 'null' if pdf_base64 is None else "atob('" + pdf_base64 + "')" };
            
            // PDF laden mit Fallback
            async function loadPDF() {{
                if (typeof pdfjsLib === 'undefined' || pdfData === null) {{
                    // Aktiviere den iframe-Fallback
                    activateIframeFallback();
                    return;
                }}
                
                try {{
                    pdfDoc = await pdfjsLib.getDocument({{ data: pdfData }}).promise;
                    document.getElementById('pageInfo').textContent = `Seite ${{currentPage}} von ${{pdfDoc.numPages}}`;
                    fitToPage(); // Automatisch an A4-Format anpassen
                    updateButtons();
                }} catch (error) {{
                    console.error('Fehler beim Laden der PDF:', error);
                    // Fallback bei PDF.js-Fehlern
                    activateIframeFallback();
                }}
            }}
            
            // Aktiviere iframe-basierten Fallback
            function activateIframeFallback() {{
                const pdfViewer = document.getElementById('pdfViewer');
                pdfViewer.innerHTML = `
                    <iframe 
                        src="data:application/pdf;base64,{pdf_base64}" 
                        width="100%" 
                        height="100%" 
                        style="border: none; background: white; border-radius: 8px;"
                        title="PDF-Vorschau A4-Format">
                        <div style="text-align: center; padding: 20px; background: #f8f9fa;">
                            <h4>📄 PDF-Vorschau</h4>
                            <p>Ihr Browser unterstützt keine eingebettete PDF-Anzeige.</p>
                            <button onclick="downloadPDF()" 
                                    style="background: #28a745; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-size: 14px;">
                                📥 PDF herunterladen
                            </button>
                        </div>
                    </iframe>
                `;
                // Controls für Download anpassen
                document.getElementById('controls').innerHTML = `
                    <div class="control-group">
                        <span>📄 A4-Format PDF-Vorschau</span>
                    </div>
                    <div class="control-group">
                        <button onclick="downloadPDF()" id="downloadBtn">📥 PDF herunterladen</button>
                    </div>
                `;
            }}
            
            // Seite optimal für A4-Format skalieren
            function fitToPage() {{
                // Berechne optimale Skalierung für A4-Darstellung
                const scaleX = VIEWER_WIDTH / A4_WIDTH;
                const scaleY = VIEWER_HEIGHT / A4_HEIGHT;
                scale = Math.min(scaleX, scaleY, 1.5); // Max 150% für Lesbarkeit
                renderPage(currentPage);
            }}
            
            // Seite rendern mit A4-optimierter Darstellung
            async function renderPage(pageNum) {{
                try {{
                    const page = await pdfDoc.getPage(pageNum);
                    const viewport = page.getViewport({{ scale: scale }});
                    
                    // Canvas-Dimensionen für HiDPI-Unterstützung
                    const outputScale = window.devicePixelRatio || 1;
                    canvas.width = Math.floor(viewport.width * outputScale);
                    canvas.height = Math.floor(viewport.height * outputScale);
                    canvas.style.width = Math.floor(viewport.width) + "px";
                    canvas.style.height = Math.floor(viewport.height) + "px";
                    
                    const transform = outputScale !== 1 ? [outputScale, 0, 0, outputScale, 0, 0] : null;
                    
                    const renderContext = {{
                        canvasContext: ctx,
                        transform: transform,
                        viewport: viewport
                    }};
                    
                    await page.render(renderContext).promise;
                    document.getElementById('pageInfo').textContent = `Seite ${{currentPage}} von ${{pdfDoc.numPages}}`;
                    document.getElementById('zoomLevel').textContent = Math.round(scale * 100) + '%';
                }} catch (error) {{
                    console.error('Fehler beim Rendern:', error);
                }}
            }}
            
            // Navigation
            function prevPage() {{
                if (currentPage <= 1) return;
                currentPage--;
                renderPage(currentPage);
                updateButtons();
            }}
            
            function nextPage() {{
                if (currentPage >= pdfDoc.numPages) return;
                currentPage++;
                renderPage(currentPage);
                updateButtons();
            }}
            
            // Zoom-Funktionen
            function zoomIn() {{
                scale = Math.min(scale * 1.2, 3.0);
                renderPage(currentPage);
            }}
            
            function zoomOut() {{
                scale = Math.max(scale / 1.2, 0.3);
                renderPage(currentPage);
            }}
            
            // Button-Status aktualisieren
            function updateButtons() {{
                document.getElementById('prevBtn').disabled = currentPage <= 1;
                document.getElementById('nextBtn').disabled = currentPage >= pdfDoc.numPages;
            }}
            
            // Download-Funktion
            function downloadPDF() {{
                const link = document.createElement('a');
                link.href = 'data:application/pdf;base64,{pdf_base64}';
                link.download = 'profil_vorschau.pdf';
                link.click();
            }}

            
            // PDF beim Laden initialisieren
            window.onload = function() {{
                loadPDF();
            }};
        </script>
    </body>
    </html>
    """
    
    return viewer_html


def display_pdf_with_pdfjs(pdf_path: str, height: int = 700):
    """
    Zeigt PDF mit PDF.js-basiertem Viewer an (mit A4-optimierter Darstellung)
    
    Args:
        pdf_path: Pfad zur PDF-Datei
        height: Höhe des Viewers in Pixeln (wird für A4-Optimierung angepasst)
    """
    try:
        # PDF.js-Viewer mit A4-Optimierung
        viewer_html = create_pdfjs_viewer(pdf_path, height)
        # A4-optimierte Höhe: 595px Breite * 1.414 (A4-Ratio) + 100px für Controls
        a4_height = int(595 * 1.414) + 100
        components.html(viewer_html, height=a4_height, scrolling=False)
        
    except Exception as e:
        st.error(f"Fehler beim Laden der PDF-Vorschau: {str(e)}")
        # Fallback zur Basis-Anzeige
        st.markdown("Fallback zur Standard-PDF-Anzeige...") 