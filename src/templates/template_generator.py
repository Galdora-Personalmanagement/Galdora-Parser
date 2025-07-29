from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable, PageBreak, KeepTogether, Frame, PageTemplate, NextPageTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
import os
import docx
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from src.utils.image_utils import get_image_path, ensure_images_in_static
from src.utils.company_config import get_company_config, get_company_logo_path
import json

class ProfileGenerator:
    """Klasse zur Erstellung von PDF-Profilen im Classic Template Design"""
    
    def __init__(self, selected_company="galdora"):
        """Initialisiert den Profil-Generator mit Stilen und Unternehmen-Konfiguration"""
        self.styles = getSampleStyleSheet()
        self.custom_styles = self._create_custom_styles()
        self.selected_company = selected_company
        self.company_config = get_company_config(selected_company)
    
    def generate_profile(self, profile_data, output_path, template="classic", format="pdf"):
        """
        Generiert ein Profil aus den extrahierten Daten im Classic Template Format
        
        Args:
            profile_data: Dictionary mit Profildaten
            output_path: Pfad für die Ausgabedatei
            template: Art der Vorlage (nur "classic" verfügbar)
            format: Format der Ausgabedatei ("pdf" oder "docx")
        
        Returns:
            Pfad zur generierten Datei
        """
        # Prüfe, ob profile_data ein gültiges Dictionary ist
        if not isinstance(profile_data, dict):
            print(f"Warnung: profile_data ist kein Dictionary. Typ: {type(profile_data)}")
            profile_data = {}
        
        # Überprüfe, ob der Ausgabepfad gültig ist
        if not output_path:
            raise ValueError("Der Ausgabepfad darf nicht leer sein.")
            
        # Überprüfe, ob das Verzeichnis existiert, falls nicht, erstelle es
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        # Je nach Format unterschiedliche Generierungsmethode aufrufen
        if format.lower() == "pdf":
            return self._generate_pdf_profile(profile_data, output_path)
        elif format.lower() == "docx":
            # Sicherstellen, dass der Ausgabepfad auf .docx endet
            if not output_path.lower().endswith('.docx'):
                base_path = os.path.splitext(output_path)[0]
                output_path = base_path + '.docx'
            return self._generate_docx_profile(profile_data, output_path)
        else:
            raise ValueError(f"Ungültiges Format: {format}. Unterstützte Formate: 'pdf', 'docx'")
    
    def _generate_pdf_profile(self, profile_data, output_path):
        """
        Generiert ein PDF-Profil aus den extrahierten Daten im Classic Template Design
        
        Args:
            profile_data: Dictionary mit Profildaten
            output_path: Pfad für die Ausgabedatei
        
        Returns:
            Pfad zur generierten PDF-Datei
        """
        try:
            # Footer text basierend auf ausgewähltem Unternehmen
            if self.selected_company == "bejob":
                footer_text = "bejob – einfach besser bewerben | Volksgartenstr. 85–89, 41065 Mönchengladbach | 02161 / 65326-40 | info@bejob.de | www.bejob.de"
            else:
                footer_text = "GALDORA Personalmanagement GmbH Co.KG Volksgartenstr. 85-89, 41065 Mönchengladbach E-Mail: info@galdora.de / Web: www.galdora.de"
            
            # Erstelle das PDF-Dokument
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=20*mm, 
                leftMargin=20*mm,
                topMargin=20*mm, 
                bottomMargin=25*mm
            )
            
            # Erstelle die Dokumentelemente
            elements = self._create_document_elements(profile_data)
            
            # Erstelle einen Footer-Callback für jede Seite
            def footer_callback(canvas, doc):
                canvas.saveState()
                footer_style = self.custom_styles['Footer']
                
                # Fußzeile am unteren Rand der Seite platzieren
                y_position = 15*mm  # Abstand vom unteren Rand
                
                # Trennlinie über der Fußzeile
                canvas.setStrokeColor(colors.lightgrey)
                canvas.setLineWidth(1)
                canvas.line(20*mm, y_position + 5*mm, A4[0] - 20*mm, y_position + 5*mm)
                
                # Fußzeilentext
                footer_text = self._get_dynamic_footer_text()
                p = Paragraph(footer_text, footer_style)
                w, h = p.wrap(A4[0] - 40*mm, 20*mm)
                p.drawOn(canvas, 20*mm, y_position - h + 2*mm)
                
                # Seitennummer hinzufügen (optional)
                page_num = canvas.getPageNumber()
                canvas.setFont("Helvetica", 8)
                canvas.setFillColor(colors.grey)
                canvas.drawRightString(A4[0] - 20*mm, y_position - h - 3*mm, f"Seite {page_num}")
                
                canvas.restoreState()
            
            # Erstelle ein PageTemplate mit dem Footer-Callback für alle Seiten
            first_page_frame = Frame(
                doc.leftMargin, 
                doc.bottomMargin, 
                A4[0] - doc.leftMargin - doc.rightMargin, 
                A4[1] - doc.topMargin - doc.bottomMargin
            )
            
            # Erstelle Templates für die erste und alle weiteren Seiten
            first_page_template = PageTemplate(
                id='firstPage', 
                frames=[first_page_frame], 
                onPage=footer_callback
            )
            
            later_page_frame = Frame(
                doc.leftMargin, 
                doc.bottomMargin, 
                A4[0] - doc.leftMargin - doc.rightMargin, 
                A4[1] - doc.topMargin - doc.bottomMargin
            )
            
            later_pages_template = PageTemplate(
                id='laterPages', 
                frames=[later_page_frame], 
                onPage=footer_callback
            )
            
            # Füge beide Templates zum Dokument hinzu
            doc.addPageTemplates([first_page_template, later_pages_template])
            
            # Setze die erste Seite explizit
            elements.insert(0, NextPageTemplate('laterPages'))
            
            # Erstelle das PDF ohne die separate Fußzeile am Ende
            doc.build(elements)
            
            return output_path
        except Exception as e:
            print(f"Fehler bei der PDF-Generierung: {str(e)}")
            raise
    
    def _generate_docx_profile(self, profile_data, output_path):
        """
        Generiert ein Word-Dokument (DOCX) aus den extrahierten Daten im Classic Template Design
        
        Args:
            profile_data: Dictionary mit Profildaten
            output_path: Pfad für die Ausgabedatei
        
        Returns:
            Pfad zur generierten DOCX-Datei
        """
        try:
            # Erstelle ein neues Word-Dokument
            doc = docx.Document()
            
            # Seiteneinstellungen (A4)
            section = doc.sections[0]
            section.page_width = Cm(21)
            section.page_height = Cm(29.7)
            section.left_margin = Cm(2)
            section.right_margin = Cm(2)
            section.top_margin = Cm(2)
            section.bottom_margin = Cm(2)
            
            # Definiere Stile für das Word-Dokument
            logo_style = doc.styles.add_style('GaldoraLogo', docx.enum.style.WD_STYLE_TYPE.PARAGRAPH)
            logo_style.font.size = Pt(36)
            logo_style.font.bold = True
            logo_style.font.color.rgb = RGBColor(0, 0, 0)
            
            italic_style = doc.styles.add_style('ItalicStyle', docx.enum.style.WD_STYLE_TYPE.PARAGRAPH)
            italic_style.font.size = Pt(10)
            italic_style.font.italic = True
            
            # Stelle sicher, dass alle Bilder im static-Verzeichnis verfügbar sind
            ensure_images_in_static()
            
            # Verwende die Multi-Company-Logo-Logik
            logo_path = self._get_company_logo_path(use_static=True)
            
            # Logo einfügen, wenn verfügbar
            if logo_path and os.path.exists(logo_path) and os.path.isfile(logo_path):
                try:
                    print(f"DOCX: Logo wird geladen aus: {logo_path}")
                    paragraph = doc.add_paragraph()
                    paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
                    run = paragraph.add_run()
                    run.add_picture(logo_path, width=Cm(5))
                except Exception as e:
                    print(f"DOCX: Fehler beim Laden des Logos: {str(e)}")
                    company_name = self.company_config.get('name', 'GALDORA')
                    header = doc.add_paragraph(company_name, style='GaldoraLogo')
                    header.alignment = WD_ALIGN_PARAGRAPH.LEFT
            else:
                print(f"DOCX: Logo-Datei nicht gefunden: {logo_path}")
                company_name = self.company_config.get('name', 'GALDORA')
                header = doc.add_paragraph(company_name, style='GaldoraLogo')
                header.alignment = WD_ALIGN_PARAGRAPH.LEFT
            
            # Tagline entfernt - kein Slogan gewünscht
            
            # Füge Leerzeile hinzu
            doc.add_paragraph()
            
            # Überschrift "Profil"
            title_style = doc.styles.add_style('ProfilTitle', docx.enum.style.WD_STYLE_TYPE.PARAGRAPH)
            title_style.font.size = Pt(16)
            title_style.font.bold = True
            title_style.font.color.rgb = RGBColor(25, 115, 184)
            
            doc.add_paragraph("Profil", style='ProfilTitle')
            
            # Verwende Classic Template Content für DOCX
            self._create_classic_docx_content(doc, profile_data)
            
            # Dokument speichern
            doc.save(output_path)
            print(f"DOCX-Datei erfolgreich erstellt: {output_path}")
            
            return output_path
            
        except Exception as e:
            print(f"Fehler bei der DOCX-Generierung: {str(e)}")
            raise e
    
    def _create_document_elements(self, profile_data):
        """
        Erstellt die Dokumentelemente für das Classic Template
        
        Args:
            profile_data: Dictionary mit Profildaten
            
        Returns:
            Liste mit PDF-Elementen
        """
        elements = []
        
        try:
            # Stelle sicher, dass alle Bilder im static-Verzeichnis verfügbar sind
            ensure_images_in_static()
            use_https_compatible = True
            
            print(f"Erstelle PDF mit Classic Template, HTTPS-Kompatibel: {use_https_compatible}")
            
            # Classic Template Content
            personal_data = profile_data.get('persönliche_daten', {})
            
            # Logo über Company-Config laden
            logo_path = self._get_company_logo_path(use_static=use_https_compatible)
            
            if not logo_path:
                company_config = self.company_config
                logo_filename = company_config.get('logo_filename', 'galdoralogo.png')
                logo_path = get_image_path(logo_filename, use_static=use_https_compatible)
                
                if not logo_path or not os.path.exists(logo_path):
                    logo_path = get_image_path(logo_filename.capitalize(), use_static=use_https_compatible)
            
            print(f"Versuche Logo zu laden von: {logo_path}")
            
            # Direkter Zugriff auf die Bilddatei im static-Verzeichnis als Fallback
            if not logo_path or not os.path.exists(logo_path):
                fallback_paths = [
                    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'static', 'images', 'galdoralogo.png'),
                    './static/images/galdoralogo.png',
                    '../static/images/galdoralogo.png',
                    '../../static/images/galdoralogo.png',
                    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'static', 'images', 'Galdoralogo.png'),
                    './static/images/Galdoralogo.png',
                    '../static/images/Galdoralogo.png',
                    '../../static/images/Galdoralogo.png'
                ]
                
                for path in fallback_paths:
                    if os.path.exists(path):
                        logo_path = path
                        print(f"Fallback: Logo gefunden in: {logo_path}")
                        break
        
            # Logo einfügen - Unterschiedliches Layout je nach Unternehmen
            if logo_path and os.path.exists(logo_path) and os.path.isfile(logo_path):
                try:
                    from PIL import Image as PILImage
                    print(f"Lade Logo aus: {logo_path}")
                    img_pil = PILImage.open(logo_path)
                    img_width, img_height = img_pil.size
                    aspect_ratio = img_width / img_height
                    
                    # BeJob-Logo rechts oben platzieren, Galdora-Logo links oben
                    if self.selected_company == "bejob":
                        # BeJob-Logo: Rechts oben platzieren
                        target_width = 180  # Etwas größer für BeJob
                        target_height = target_width / aspect_ratio
                        img = Image(logo_path, width=target_width, height=target_height)
                        
                        # Logo-Tabelle mit BeJob-spezifischem Layout (Logo rechts)
                        logo_table = Table([["", img]], 
                                    colWidths=[A4[0] - target_width - 50*mm, target_width + 10])
                        
                        logo_table.setStyle(TableStyle([
                            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                            ('VALIGN', (0, 0), (1, 0), 'TOP'),
                        ]))
                        elements.append(logo_table)
                        # Weniger Abstand nach Logo für BeJob
                        elements.append(Spacer(1, 0.1*cm))
                    else:
                        # Galdora-Logo: Links oben platzieren (bisheriges Layout)
                        target_width = 160
                        target_height = target_width / aspect_ratio
                        img = Image(logo_path, width=target_width, height=target_height)
                        
                        # Logo-Tabelle mit Galdora-spezifischem Layout (Logo links)
                        logo_table = Table([[img, ""]], 
                                    colWidths=[target_width + 10, A4[0] - target_width - 50*mm])
                        
                        logo_table.setStyle(TableStyle([
                            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
                            ('VALIGN', (0, 0), (1, 0), 'TOP'),
                        ]))
                        elements.append(logo_table)
                        # Standard-Abstand nach Logo für Galdora
                        elements.append(Spacer(1, 0.2*cm))
                except Exception as e:
                    print(f"Fehler beim Laden des Logos: {str(e)}")
                    elements.append(Paragraph("GALDORA", self.custom_styles['GaldoraLogo']))
            else:
                print(f"Logo-Datei nicht gefunden oder ungültig: {logo_path}")
                elements.append(Paragraph("GALDORA", self.custom_styles['GaldoraLogo']))
            
            # Classic Template Content erstellen
            self._create_classic_content(elements, profile_data)
            
            return elements
            
        except Exception as e:
            print(f"Fehler beim Erstellen der Dokumentelemente: {str(e)}")
            raise
    
    def _create_classic_content(self, elements, profile_data):
        """Erstellt den Content für das Classic Template"""
        
        # Persönliche Daten
        personal_data = profile_data.get('persönliche_daten', {})
        
        # Profil Überschrift und Name - Unterschiedliches Layout je nach Unternehmen
        if self.selected_company == "bejob":
            # BeJob: Weniger Abstand vor dem Profil-Titel für kompakteres Layout
            elements.append(Spacer(1, -0.2*cm))  # Negativer Abstand rückt Text nach oben
        
        elements.append(Paragraph("Profil", self.custom_styles['ProfilTitle']))
        
        # Name
        name = personal_data.get('name', 'Profil')
        elements.append(Paragraph(name, self.custom_styles['Name']))
        
        # OPTIMIERT: Persönliche Informationen mit kompakterem Layout und ausgegraut
        # Erstelle einen neuen Stil für ausgegraute Informationen
        grayed_style = ParagraphStyle(
            'GrayedLabelInline',
            parent=self.custom_styles['LabelInline'],
            textColor=colors.grey
        )
        
        # Persönliche Daten ausgegraut
        if personal_data.get('wohnort'):
            elements.append(Paragraph(f"Wohnort: {personal_data.get('wohnort')}", grayed_style))

        # Kündigungsfrist direkt unter Wohnort platzieren, nur wenn vorhanden
        verfuegbarkeit_status = profile_data.get('verfuegbarkeit_status', '')
        verfuegbarkeit_details = profile_data.get('verfuegbarkeit_details', '')
        if verfuegbarkeit_status:
            if verfuegbarkeit_details:
                elements.append(Paragraph(f"ab {verfuegbarkeit_details}", grayed_style))
            else:
                elements.append(Paragraph(f"ab {verfuegbarkeit_status}", grayed_style))

        # Jahrgang nur anzeigen, wenn vorhanden
        if personal_data.get('jahrgang'):
            elements.append(Paragraph(f"Jahrgang: {personal_data.get('jahrgang')}", grayed_style))

        # Führerschein nur anzeigen, wenn das Feld ausgefüllt ist
        fuehrerschein = personal_data.get('führerschein', '')
        if fuehrerschein and fuehrerschein.strip():
            elements.append(Paragraph(f"Führerschein: {fuehrerschein}", grayed_style))

        # Wunschgehalt (auch ausgegraut), nur wenn vorhanden
        wunschgehalt = profile_data.get('wunschgehalt', '')
        if wunschgehalt:
            elements.append(Paragraph(f"Gehaltsvorstellung: {wunschgehalt}", grayed_style))

        # NEU: Vergrößerter Abstand nach Profilinfos
        elements.append(Spacer(1, 12))  # Erhöht von 6 auf 12

        # Ansprechpartner Block (jetzt nach dem Profil), nur wenn vorhanden
        kontakt = personal_data.get('kontakt', {})
        ansprechpartner = kontakt.get('ansprechpartner', '')

        # GEÄNDERT: Trennlinie nur anzeigen, wenn ein Ansprechpartner vorhanden ist und nicht "Kein Ansprechpartner"
        if ansprechpartner and ansprechpartner.strip() and ansprechpartner != "Kein Ansprechpartner":
            # Trennlinie vor dem Ansprechpartner
            elements.append(HRFlowable(
                width="100%",
                thickness=0.5,
                color=colors.lightgrey,
                spaceBefore=3,
                spaceAfter=12  # Erhöht für mehr Abstand vor Ansprechpartner
            ))
            
            elements.append(Paragraph("IHR ANSPRECHPARTNER", self.custom_styles['ContactHeader']))
            
            if ansprechpartner == "Melike Demirkol":
                anrede = f"Frau Demirkol"
            elif ansprechpartner == "Alessandro Böhm":
                anrede = f"Herr Böhm"
                email = kontakt.get('email', "boehm@galdora.de")
            else:
                nachname = ansprechpartner.split()[-1] if ansprechpartner else 'Fischer'
                anrede = f"Herr {nachname}"
            
            # Standard-Telefonnummer für alle außer Salim Alizai
            if ansprechpartner == "Salim Alizai":
                telefon = kontakt.get('telefon', '')
            else:
                telefon = "02161 62126-00"
            
            if ansprechpartner == "Alessandro Böhm":
                email = kontakt.get("email", "boehm@galdora.de")
            elif ansprechpartner == "Salim Alizai":
                email = kontakt.get("email", "gl@galdora.de")
            elif ansprechpartner == "Konrad Ruszczyk":
                email = kontakt.get("email", "konrad@galdora.de")
            else:
                if 'nachname' in locals():
                    email = kontakt.get("email", f"{nachname.lower()}@galdora.de")
            
            # Ansprechpartner-Daten ausgegraut darstellen
            grayed_contact_style = ParagraphStyle(
                'GrayedContactData',
                parent=self.custom_styles['ContactData'],
                textColor=colors.grey
            )
            
            elements.append(Paragraph(ansprechpartner, grayed_contact_style))
            
            if telefon:
                elements.append(Paragraph(f"Tel.: {telefon}", grayed_contact_style))
            
            if email:
                elements.append(Paragraph(f"E-Mail: {email}", grayed_contact_style))
            
            # NEU: Erhöhter Abstand nach Ansprechpartner
            elements.append(Spacer(1, 12))  # Erhöht von 6 auf 12
            
            # GEÄNDERT: Trennlinie nach dem Ansprechpartner
            elements.append(HRFlowable(
                width="100%",
                thickness=0.5,  # Angepasst auf 0.5 wie die obere Trennlinie
                color=colors.lightgrey,  # Angepasst auf lightgrey wie die obere Trennlinie
                spaceBefore=3,
                spaceAfter=12  # Erhöht für mehr Abstand vor Beruflicher Werdegang
            ))
        
        # Beruflicher Werdegang
        berufserfahrung = profile_data.get('berufserfahrung', [])
        if berufserfahrung:
            elements.append(Paragraph("Beruflicher Werdegang", self.custom_styles['Heading2']))
            
            # Verbesserte Platzberechnung und vorausschauende Seitenumbrüche
            berufserfahrung_gruppen = []
            aktuelle_gruppe = []
            aktueller_platz = A4[1] - 400  # Verfügbarer Platz auf erster Seite
            
            # Erste Phase: Berechne Höhen und plane Gruppen
            for i, erfahrung in enumerate(berufserfahrung):
                # Präzisere Höhenberechnung
                aufgaben_count = len(erfahrung.get('aufgaben', []))
                text_laenge = sum(len(aufgabe) for aufgabe in erfahrung.get('aufgaben', []))
                position_laenge = len(erfahrung.get('position', ''))
                unternehmen_laenge = len(erfahrung.get('unternehmen', ''))
                
                # Dynamischere Höhenberechnung basierend auf Textlänge
                basis_hoehe = 40  # Grundhöhe für Zeitraum, Unternehmen, Position
                aufgaben_hoehe = min(20 * aufgaben_count, 10 + (text_laenge / 50))  # Begrenzte Höhe pro Aufgabe
                zusatz_hoehe = (position_laenge + unternehmen_laenge) / 100  # Zusätzliche Höhe für lange Texte
                
                entry_height = basis_hoehe + aufgaben_hoehe + zusatz_hoehe
                
                # Prüfen, ob dieser Eintrag in die aktuelle Gruppe passt
                if entry_height <= aktueller_platz:
                    # Passt auf aktuelle Seite
                    aktuelle_gruppe.append((i, erfahrung, entry_height))
                    aktueller_platz -= entry_height
                else:
                    # Passt nicht mehr auf aktuelle Seite
                    if aktuelle_gruppe:  # Vorherige Gruppe speichern
                        berufserfahrung_gruppen.append(aktuelle_gruppe)
                    
                    # Neue Gruppe auf neuer Seite beginnen
                    aktuelle_gruppe = [(i, erfahrung, entry_height)]
                    aktueller_platz = A4[1] - 100 - entry_height  # Neue Seite mit weniger Header
            
            # Letzte Gruppe hinzufügen
            if aktuelle_gruppe:
                berufserfahrung_gruppen.append(aktuelle_gruppe)
            
            # Zweite Phase: Verarbeite die Gruppen
            for gruppen_index, gruppe in enumerate(berufserfahrung_gruppen):
                # Seitenumbruch zwischen Gruppen (außer vor der ersten)
                if gruppen_index > 0:
                    elements.append(PageBreak())
                    print(f"📄 Intelligenter Seitenumbruch vor Gruppe {gruppen_index+1} eingefügt")
                
                # Alle Einträge in dieser Gruppe verarbeiten
                gruppen_elemente = []
                
                for i, erfahrung, _ in gruppe:
                    zeitraum = erfahrung.get('zeitraum', '')
                    # Fallback-Ersetzung für Legacy-Daten
                    if "bis jetzt" in zeitraum.lower() or "bis heute" in zeitraum.lower():
                        print(f"⚠️  Legacy-Zeitraum erkannt: {zeitraum} - wird korrigiert")
                        zeitraum = zeitraum.replace("bis jetzt", "2025").replace("bis heute", "2025").replace("bis JETZT", "2025")
                    
                    unternehmen = erfahrung.get('unternehmen', '')
                    position = erfahrung.get('position', '')
                    
                    aufgaben = erfahrung.get('aufgaben', [])
                    
                    # Adaptive Aufgabenreduzierung basierend auf Gruppengröße
                    max_tasks = 6
                    if len(gruppe) > 2 and len(aufgaben) > 4:
                        # Bei größeren Gruppen: Maximal 4 Aufgaben pro Eintrag
                        aufgaben = aufgaben[:4]
                        print(f"📄 Aufgaben für Berufsstation {i+1} auf 4 reduziert (optimierte Gruppierung)")
                    elif len(aufgaben) > max_tasks:
                        # Standard: Maximal 6 Aufgaben
                        aufgaben = aufgaben[:max_tasks]
                        print(f"📄 Aufgaben für Berufsstation {i+1} auf {max_tasks} begrenzt")
                    
                    aufgaben_formatted = []
                    for aufgabe in aufgaben:
                        aufgaben_formatted.append(Paragraph(f"• {aufgabe}", self.custom_styles['Normal']))
                    
                    # Tausch von Unternehmen und Position - Unternehmen jetzt prominent oben
                    right_column_content = [
                        Paragraph(unternehmen, self.custom_styles['Position']),  # Unternehmen mit Position-Stil (fett)
                        Paragraph(position, self.custom_styles['Company'])      # Position mit Company-Stil (normal) - wird neben Enddatum platziert
                    ]
                    
                    right_column_content.extend(aufgaben_formatted)
                    
                    # Zeitraum ohne Zeilenumbruch für konsistente Positionierung
                    zeitraum_formatted = zeitraum
                    
                    # Erste Zeile: Zeitraum und Unternehmen
                    data = [[Paragraph(zeitraum_formatted, self.custom_styles['Period']), right_column_content[0]]]
                    
                    # Zweite Zeile: Position immer direkt unter dem Unternehmen
                    data.append([Paragraph('', self.custom_styles['Normal']), right_column_content[1]])
                    
                    # Spacer zwischen Position und Aufgaben
                    if len(right_column_content) > 2:
                        data.append([Paragraph('', self.custom_styles['Normal']), Spacer(1, 5)])  # Reduziert auf 5 Punkte Abstand für kompakteres Layout
                    
                    # Restliche Inhalte (Aufgaben)
                    for j in range(2, len(right_column_content)):
                        data.append([Paragraph('', self.custom_styles['Normal']), right_column_content[j]])
                    
                    col_widths = [A4[0] * 0.15, A4[0] * 0.65]
                    
                    table = Table(data, colWidths=col_widths)
                    table.setStyle(TableStyle([
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                        ('LEFTPADDING', (1, 0), (1, -1), 0.5*cm),  # Reduziert von 2cm auf 0.5cm
                        ('BOTTOMPADDING', (0, 0), (0, 0), 0),  # Kein unterer Abstand für das Datum
                        # Konsistenter Abstand für die Position (zweite Zeile)
                        ('TOPPADDING', (1, 1), (1, 1), 1),  # Minimaler Abstand für kompakteres Layout
                    ]))
                    
                    # Jede Berufsstation zur Gruppe hinzufügen
                    gruppen_elemente.extend([table, Spacer(1, 0.5*cm)])  # Reduziert auf 0.5cm für effizientere Platznutzung
                
                try:
                    # Die gesamte Gruppe mit KeepTogether umschließen, wenn sie nicht zu groß ist
                    if len(gruppe) <= 3:  # Maximal 3 Einträge pro KeepTogether-Block
                        elements.append(KeepTogether(gruppen_elemente))
                        print(f"📄 Gruppe mit {len(gruppe)} Berufsstationen zusammengehalten")
                    else:
                        # Bei größeren Gruppen: Einzeln hinzufügen, um Überlauf zu vermeiden
                        elements.extend(gruppen_elemente)
                        print(f"📄 Große Gruppe mit {len(gruppe)} Berufsstationen ohne KeepTogether hinzugefügt")
                except Exception as e:
                    print(f"Fehler beim Verarbeiten einer Berufsgruppe: {str(e)}")
                    elements.extend(gruppen_elemente)  # Fallback: Ohne KeepTogether hinzufügen
        
        # Trennlinie zwischen Berufserfahrung und Ausbildung
        elements.append(Spacer(1, 0.5*cm))
        elements.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=colors.lightgrey))
        elements.append(Spacer(1, 0.5*cm))
        
        # Ausbildung
        ausbildungen = profile_data.get('ausbildung', [])
        if ausbildungen:
            # Erstelle Ausbildungssektion-Elemente
            ausbildung_elements = []
            ausbildung_elements.append(Paragraph("Ausbildung", self.custom_styles['Heading2']))
            
            for i, ausbildung in enumerate(ausbildungen):
                try:
                    zeitraum = ausbildung.get('zeitraum', '')
                    # Strukturierte Extraktion sollte bereits korrekte MM/YYYY Formate liefern
                    if "bis jetzt" in zeitraum.lower() or "bis heute" in zeitraum.lower():
                        print(f"⚠️  Legacy-Ausbildungszeitraum erkannt: {zeitraum}")
                        zeitraum = zeitraum.replace("bis jetzt", "2025").replace("bis heute", "2025").replace("bis JETZT", "2025")
                    institution = ausbildung.get('institution', '')
                    abschluss = ausbildung.get('abschluss', '')
                    schwerpunkte = ausbildung.get('schwerpunkte', '')
                    
                    # Auch bei Ausbildung: Institution (wie Unternehmen) fett darstellen
                    right_column_content = []
                    right_column_content.append(Paragraph(institution, self.custom_styles['Position']))  # Institution mit Position-Stil (fett)
                    
                    # Abschluss als zweite Zeile (wie Position bei Berufserfahrung)
                    if abschluss:
                        right_column_content.append(Paragraph(f"{abschluss}", self.custom_styles['Company']))
                    
                    # Aufgaben/Schwerpunkte als Stichpunkte formatieren
                    aufgaben = []
                    if schwerpunkte:
                        schwerpunkte_liste = schwerpunkte.split(", ")
                        for schwerpunkt in schwerpunkte_liste:
                            aufgaben.append(f"• {schwerpunkt}")
                    
                    # Zusätzliche Aufgaben aus dem Aufgaben-Feld (falls vorhanden)
                    if 'aufgaben' in ausbildung and isinstance(ausbildung['aufgaben'], list):
                        for aufgabe in ausbildung['aufgaben']:
                            aufgaben.append(f"• {aufgabe}")
                    
                    # Aufgaben als formatierte Paragraphen hinzufügen
                    for aufgabe in aufgaben:
                        right_column_content.append(Paragraph(aufgabe, self.custom_styles['Normal']))
                    
                    # Zeitraum auf zwei Zeilen aufteilen falls Bindestrich vorhanden
                    if ' - ' in zeitraum:
                        start_date, end_date = zeitraum.split(' - ')
                        zeitraum_formatted = f"{start_date} -<br/>{end_date}"
                    else:
                        zeitraum_formatted = zeitraum
                    
                    # Zeitraum ohne Zeilenumbruch für konsistente Positionierung
                    zeitraum_formatted = zeitraum
                    
                    # Erste Zeile: Zeitraum und Institution
                    data = [[Paragraph(zeitraum_formatted, self.custom_styles['Period']), right_column_content[0]]]
                    
                    # Zweite Zeile: Abschluss immer direkt unter der Institution
                    if len(right_column_content) > 1:
                        data.append([Paragraph('', self.custom_styles['Normal']), right_column_content[1]])
                    
                    # Restliche Inhalte (Aufgaben/Schwerpunkte)
                    for j in range(2, len(right_column_content)):
                        data.append([Paragraph('', self.custom_styles['Normal']), right_column_content[j]])
                    
                    col_widths = [A4[0] * 0.15, A4[0] * 0.65]
                    
                    table = Table(data, colWidths=col_widths)
                    table.setStyle(TableStyle([
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                        ('LEFTPADDING', (1, 0), (1, -1), 0.5*cm),  # Reduziert von 2cm auf 0.5cm
                        ('BOTTOMPADDING', (0, 0), (0, 0), 0),  # Kein unterer Abstand für das Datum
                        # Konsistenter Abstand für den Abschluss (zweite Zeile)
                        ('TOPPADDING', (1, 1), (1, 1), 1),  # Minimaler Abstand für kompakteres Layout
                    ]))
                    
                    # Erste Ausbildung wird mit Überschrift zusammengehalten
                    if i == 0:
                        ausbildung_elements.extend([table, Spacer(1, 0.1*cm)])  # Reduziert von 0.3cm auf 0.1cm
                    else:
                        # Weitere Ausbildungen separat hinzufügen
                        elements.extend(ausbildung_elements)  # Erste Gruppe hinzufügen
                        ausbildung_elements = []  # Reset für weitere einzelne Elemente
                        entry_elements = [table, Spacer(1, 0.5*cm)]  # Reduziert auf 0.5cm für effizientere Platznutzung
                        elements.append(KeepTogether(entry_elements))
                        
                except Exception as e:
                    print(f"Fehler bei der Verarbeitung einer Ausbildung: {str(e)}")
                    fallback_element = Paragraph(f"{zeitraum} - {institution}", self.custom_styles['Normal'])
                    if i == 0:
                        ausbildung_elements.extend([fallback_element, Spacer(1, 0.1*cm)])  # Reduziert von 0.3cm auf 0.1cm
                    else:
                        elements.extend(ausbildung_elements)
                        ausbildung_elements = []
                        elements.append(fallback_element)
                        elements.append(Spacer(1, 0.1*cm))  # Reduziert von 0.3cm auf 0.1cm
            
            # Überschrift + erste Ausbildung zusammen mit KeepTogether hinzufügen
            if ausbildung_elements:
                elements.append(KeepTogether(ausbildung_elements))
                print("📄 Ausbildung-Überschrift mit erstem Element zusammengehalten")
        
        # Fort- und Weiterbildungen
        weiterbildungen = profile_data.get('weiterbildungen', [])
        if weiterbildungen:
            elements.append(Spacer(1, 0.5*cm))
            elements.append(HRFlowable(width="100%", thickness=0.5, lineCap='round', color=colors.lightgrey, spaceBefore=0.3*cm, spaceAfter=0.3*cm))
            elements.append(Spacer(1, 0.3*cm))
            
            # Erstelle Weiterbildungssektion-Elemente
            weiterbildung_elements = []
            weiterbildung_elements.append(Paragraph("Fort- und Weiterbildungen", self.custom_styles['Heading2']))
            
            for i, weiterbildung in enumerate(weiterbildungen):
                try:
                    zeitraum = weiterbildung.get('zeitraum', '')
                    # Strukturierte Extraktion sollte bereits korrekte MM/YYYY Formate liefern
                    if "bis jetzt" in zeitraum.lower() or "bis heute" in zeitraum.lower():
                        print(f"⚠️  Legacy-Weiterbildungszeitraum erkannt: {zeitraum}")
                        zeitraum = zeitraum.replace("bis jetzt", "2025").replace("bis heute", "2025").replace("bis JETZT", "2025")
                    bezeichnung = weiterbildung.get('bezeichnung', '')
                    abschluss = weiterbildung.get('abschluss', '')
                    
                    right_column_content = []
                    
                    # Auch bei Weiterbildungen: Bezeichnung fett darstellen und maskuline Form verwenden
                    # Entferne "zum" oder "zur" und verwende immer maskuline Form
                    bezeichnung_clean = bezeichnung.replace("zur ", "").replace("zum ", "")
                    right_column_content.append(Paragraph(f"Fortbildung zum {bezeichnung_clean}", self.custom_styles['Position']))  # Mit Position-Stil (fett)
                    
                    # Abschluss als zweite Zeile (wie Position bei Berufserfahrung)
                    if abschluss and abschluss not in bezeichnung:
                        right_column_content.append(Paragraph(f"{abschluss}", self.custom_styles['Company']))
                    
                    # Aufgaben/Inhalte als Stichpunkte formatieren
                    aufgaben = []
                    
                    # Inhalte aus dem Inhalte-Feld (falls vorhanden)
                    if 'inhalte' in weiterbildung and isinstance(weiterbildung['inhalte'], list):
                        for inhalt in weiterbildung['inhalte']:
                            aufgaben.append(f"• {inhalt}")
                    
                    # Aufgaben aus dem Aufgaben-Feld (falls vorhanden)
                    if 'aufgaben' in weiterbildung and isinstance(weiterbildung['aufgaben'], list):
                        for aufgabe in weiterbildung['aufgaben']:
                            aufgaben.append(f"• {aufgabe}")
                    
                    # Aufgaben als formatierte Paragraphen hinzufügen
                    for aufgabe in aufgaben:
                        right_column_content.append(Paragraph(aufgabe, self.custom_styles['Normal']))
                    
                    # Zeitraum auf zwei Zeilen aufteilen falls Bindestrich vorhanden
                    if ' - ' in zeitraum:
                        start_date, end_date = zeitraum.split(' - ')
                        zeitraum_formatted = f"{start_date} -<br/>{end_date}"
                    else:
                        zeitraum_formatted = zeitraum
                    
                    # Zeitraum ohne Zeilenumbruch für konsistente Positionierung
                    zeitraum_formatted = zeitraum
                    
                    # Erste Zeile: Zeitraum und Bezeichnung
                    data = [[Paragraph(zeitraum_formatted, self.custom_styles['Period']), right_column_content[0]]]
                    
                    # Zweite Zeile: Abschluss immer direkt unter der Bezeichnung
                    if len(right_column_content) > 1:
                        data.append([Paragraph('', self.custom_styles['Normal']), right_column_content[1]])
                    
                    # Restliche Inhalte (Aufgaben/Inhalte)
                    for j in range(2, len(right_column_content)):
                        data.append([Paragraph('', self.custom_styles['Normal']), right_column_content[j]])
                    
                    col_widths = [A4[0] * 0.15, A4[0] * 0.65]
                    
                    table = Table(data, colWidths=col_widths)
                    table.setStyle(TableStyle([
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                        ('LEFTPADDING', (1, 0), (1, -1), 0.5*cm),  # Reduziert von 2cm auf 0.5cm
                        ('BOTTOMPADDING', (0, 0), (0, 0), 0),  # Kein unterer Abstand für das Datum
                        # Konsistenter Abstand für den Abschluss (zweite Zeile)
                        ('TOPPADDING', (1, 1), (1, 1), 1),  # Minimaler Abstand für kompakteres Layout
                    ]))
                    
                    # Erste Weiterbildung wird mit Überschrift zusammengehalten
                    if i == 0:
                        weiterbildung_elements.extend([table, Spacer(1, 0.1*cm)])  # Reduziert von 0.3cm auf 0.1cm
                    else:
                        # Weitere Weiterbildungen separat hinzufügen
                        elements.extend(weiterbildung_elements)  # Erste Gruppe hinzufügen  
                        weiterbildung_elements = []  # Reset für weitere einzelne Elemente
                        entry_elements = [table, Spacer(1, 0.5*cm)]  # Reduziert auf 0.5cm für effizientere Platznutzung
                        elements.append(KeepTogether(entry_elements))
                        
                except Exception as e:
                    print(f"Fehler bei der Verarbeitung einer Weiterbildung: {str(e)}")
                    fallback_element = Paragraph(f"{zeitraum} - {bezeichnung}", self.custom_styles['Normal'])
                    if i == 0:
                        weiterbildung_elements.extend([fallback_element, Spacer(1, 0.1*cm)])  # Reduziert von 0.3cm auf 0.1cm
                    else:
                        elements.extend(weiterbildung_elements)
                        weiterbildung_elements = []
                        elements.append(fallback_element)
                        elements.append(Spacer(1, 0.1*cm))  # Reduziert von 0.3cm auf 0.1cm
            
            # Überschrift + erste Weiterbildung zusammen mit KeepTogether hinzufügen
            if weiterbildung_elements:
                elements.append(KeepTogether(weiterbildung_elements))
                print("📄 Fort- und Weiterbildungen-Überschrift mit erstem Element zusammengehalten")
        
        # Die alte Footer-Implementierung wird entfernt, da sie jetzt durch den PageTemplate ersetzt wird
    
    def _create_classic_docx_content(self, doc, profile_data):
        """Erstellt den Content für das Classic Template im DOCX Format"""
        
        # Persönliche Daten
        personal_data = profile_data.get("persönliche_daten", {})
        
        # Name (in Profil-Abschnitt)
        name = personal_data.get("name", "")
        doc.add_paragraph(name).bold = True
        
        # Erstelle eine 2-spaltige Tabelle für persönliche Daten
        table = doc.add_table(rows=0, cols=2)
        table.autofit = True
        
        # Wohnort
        if personal_data.get("wohnort"):
            row_cells = table.add_row().cells
            row_cells[0].text = "Wohnort:"
            row_cells[0].paragraphs[0].runs[0].bold = True
            row_cells[1].text = personal_data.get("wohnort", "")
        
        # Jahrgang
        if personal_data.get("jahrgang"):
            row_cells = table.add_row().cells
            row_cells[0].text = "Jahrgang:"
            row_cells[0].paragraphs[0].runs[0].bold = True
            row_cells[1].text = personal_data.get("jahrgang", "")
        
        # Führerschein
        if personal_data.get("führerschein"):
            row_cells = table.add_row().cells
            row_cells[0].text = "Führerschein:"
            row_cells[0].paragraphs[0].runs[0].bold = True
            row_cells[1].text = personal_data.get("führerschein", "")
        
        # Ansprechpartner-Abschnitt hinzufügen (nach dem Profil)
        kontakt = personal_data.get('kontakt', {})
        ansprechpartner = kontakt.get('ansprechpartner', '')
        
        if ansprechpartner and ansprechpartner != "Kein Ansprechpartner":
            doc.add_paragraph().add_run().add_break()
            ansprechpartner_heading = doc.add_paragraph("IHR ANSPRECHPARTNER")
            ansprechpartner_heading.runs[0].bold = True
            ansprechpartner_heading.runs[0].font.size = Pt(9)
            
            # Ansprechpartner-Details
            doc.add_paragraph(ansprechpartner)
            
            # Standard-Telefonnummer für alle außer Salim Alizai
            if ansprechpartner == "Salim Alizai":
                telefon = kontakt.get('telefon', '')
            else:
                telefon = "02161 62126-00"
                
            if telefon:
                doc.add_paragraph(f"Tel.: {telefon}")
            
            email = kontakt.get('email', '')
            if email:
                doc.add_paragraph(f"E-Mail: {email}")
        
        # Berufserfahrung
        doc.add_paragraph().add_run().add_break()
        heading_style = doc.styles.add_style('Heading2', docx.enum.style.WD_STYLE_TYPE.PARAGRAPH)
        heading_style.font.size = Pt(12)
        heading_style.font.bold = True
        
        doc.add_paragraph("Beruflicher Werdegang", style='Heading2')
        
        # Füge Berufserfahrung hinzu
        for experience in profile_data.get("berufserfahrung", []):
            exp_table = doc.add_table(rows=0, cols=2)
            exp_table.autofit = True
            
            # Zeitraum
            row_cells = exp_table.add_row().cells
            row_cells[0].text = experience.get("zeitraum", "")
            row_cells[0].paragraphs[0].runs[0].bold = True
            
            # Position und Firma (neue Reihenfolge)
            row_cells[1].text = experience.get("position", "")
            row_cells[1].paragraphs[0].runs[0].bold = True
            row_cells[1].add_paragraph(experience.get("unternehmen", experience.get("firma", ""))).italic = False
            
            # Beschreibung (wenn vorhanden)
            if experience.get("beschreibung"):
                row_cells = exp_table.add_row().cells
                row_cells[0].merge(row_cells[1])
                row_cells[0].text = experience.get("beschreibung", "")
            
            doc.add_paragraph()
        
        # Ausbildung
        doc.add_paragraph("Ausbildung", style='Heading2')
        
        # Füge Ausbildung hinzu
        for education in profile_data.get("ausbildung", []):
            edu_table = doc.add_table(rows=0, cols=2)
            edu_table.autofit = True
            
            # Zeitraum
            row_cells = edu_table.add_row().cells
            row_cells[0].text = education.get("zeitraum", "")
            row_cells[0].paragraphs[0].runs[0].bold = True
            
            # Institution und Abschluss (wie bei PDF)
            row_cells[1].text = education.get("institution", "")
            row_cells[1].paragraphs[0].runs[0].bold = True
            row_cells[1].add_paragraph(education.get("abschluss", "")).italic = False
            
            # Schwerpunkte und Aufgaben als Stichpunkte formatieren
            schwerpunkte = education.get("schwerpunkte", "")
            if schwerpunkte:
                schwerpunkte_liste = schwerpunkte.split(", ")
                for schwerpunkt in schwerpunkte_liste:
                    row_cells[1].add_paragraph(f"• {schwerpunkt}")
            
            # Aufgaben aus dem Aufgaben-Feld (falls vorhanden)
            if 'aufgaben' in education and isinstance(education['aufgaben'], list):
                for aufgabe in education['aufgaben']:
                    row_cells[1].add_paragraph(f"• {aufgabe}")
            
            doc.add_paragraph()
        
        # Weiterbildungen
        doc.add_paragraph()
        doc.add_paragraph("Weiterbildungen", style='Heading2')
        
        if profile_data.get("weiterbildungen"):
            for training in profile_data.get("weiterbildungen", []):
                train_table = doc.add_table(rows=0, cols=2)
                train_table.autofit = True
                
                # Zeitraum
                row_cells = train_table.add_row().cells
                row_cells[0].text = training.get("zeitraum", "")
                row_cells[0].paragraphs[0].runs[0].bold = True
                
                # Bezeichnung und Abschluss (wie bei PDF)
                row_cells[1].text = training.get("bezeichnung", "")
                row_cells[1].paragraphs[0].runs[0].bold = True
                if training.get("abschluss"):
                    row_cells[1].add_paragraph(training.get("abschluss", "")).italic = False
                
                # Inhalte und Aufgaben als Stichpunkte formatieren
                if 'inhalte' in training and isinstance(training['inhalte'], list):
                    for inhalt in training['inhalte']:
                        row_cells[1].add_paragraph(f"• {inhalt}")
                
                # Aufgaben aus dem Aufgaben-Feld (falls vorhanden)
                if 'aufgaben' in training and isinstance(training['aufgaben'], list):
                    for aufgabe in training['aufgaben']:
                        row_cells[1].add_paragraph(f"• {aufgabe}")
                
                doc.add_paragraph()
        
        # Footer
        doc.add_paragraph().add_run().add_break()
        footer_style = doc.styles.add_style('FooterStyle', docx.enum.style.WD_STYLE_TYPE.PARAGRAPH)
        footer_style.font.size = Pt(8)
        footer_style.font.color.rgb = RGBColor(128, 128, 128)
        
        footer_text = self._get_dynamic_footer_text()
        doc.add_paragraph(footer_text, style='FooterStyle')
    
    def _create_custom_styles(self):
        """Erstellt benutzerdefinierte Stile für das Classic Template"""
        custom_styles = {}
        
        # GALDORA Überschrift-Stil
        custom_styles['GaldoraLogo'] = ParagraphStyle(
            'GaldoraLogo',
            parent=self.styles['Normal'],
            fontSize=36,
            fontName='Helvetica-Bold',
            textColor=colors.black,
            spaceAfter=0.1*cm
        )

        # Tagline unter dem Logo
        custom_styles['Tagline'] = ParagraphStyle(
            'Tagline',
            parent=self.styles['Italic'],
            fontSize=10,
            fontName='Helvetica-Oblique',
            textColor=colors.black,
            spaceAfter=1.5*cm
        )
        
        # GEÄNDERT: Profil Überschrift dünner und größer
        custom_styles['ProfilTitle'] = ParagraphStyle(
            'ProfilTitle',
            parent=self.styles['Heading1'],
            fontSize=16,  # Erhöht von 14 auf 16
            fontName='Helvetica',  # Geändert von Helvetica-Bold zu Helvetica (dünner)
            textColor=colors.HexColor('#1973B8'),
            spaceBefore=0.2*cm,
            spaceAfter=0.3*cm,
            alignment=0,
            underline=0
        )
        
        # OPTIMIERT: Name mit verbessertem Spacing
        custom_styles['Name'] = ParagraphStyle(
            'Name',
            parent=self.styles['Normal'],
            fontSize=13,  # Reduziert von 14 für bessere Balance
            fontName='Helvetica',
            spaceBefore=0.1*cm,  # Reduziert von 0.2cm
            spaceAfter=0.6*cm,   # Reduziert von 0.8cm
            alignment=0
        )
        
        # OPTIMIERT: Überschrift für Abschnitte mit verbessertem Spacing
        custom_styles['Heading2'] = ParagraphStyle(
            'Heading2',
            parent=self.styles['Heading2'],
            fontSize=11,  # Reduziert von 12 für bessere Hierarchie
            fontName='Helvetica-Bold',
            textColor=colors.black,
            spaceBefore=0.5*cm,  # Reduziert von 0.7cm
            spaceAfter=0.2*cm,   # Reduziert von 0.3cm
            underline=0
        )
        
        # OPTIMIERT: Ansprechpartner Überschrift
        custom_styles['ContactHeader'] = ParagraphStyle(
            'ContactHeader',
            parent=self.styles['Normal'],
            fontSize=8,   # Reduziert von 9 für subtilere Wirkung
            fontName='Helvetica-Bold',
            spaceBefore=0.1*cm,  # Reduziert von 0.2cm
            spaceAfter=0.05*cm,  # Reduziert von 0.1cm
            underline=0
        )
        
        # OPTIMIERT: Ansprechpartner Daten
        custom_styles['ContactData'] = ParagraphStyle(
            'ContactData',
            parent=self.styles['Normal'],
            fontSize=8,   # Reduziert von 9 für bessere Proportionen
            textColor=colors.grey,
            spaceAfter=0.05*cm,  # Reduziert von 0.1cm
            leftIndent=0*cm
        )
        
        # OPTIMIERT: Normaler Text mit tighterem Spacing
        custom_styles['Normal'] = ParagraphStyle(
            'Normal',
            parent=self.styles['Normal'],
            fontSize=9,
            spaceAfter=0.01*cm  # Reduziert von 0.02cm für kompakteres Layout
        )
        
        # OPTIMIERT: Label-Text mit verbessertem Spacing
        custom_styles['LabelInline'] = ParagraphStyle(
            'LabelInline',
            parent=self.styles['Normal'],
            fontSize=9,
            fontName='Helvetica-Bold',
            spaceAfter=0.05*cm  # Reduziert von 0.1cm
        )
        
        # OPTIMIERT: Firmenname mit verbessertem Styling
        custom_styles['Company'] = ParagraphStyle(
            'Company',
            parent=self.styles['Normal'],
            fontSize=9,
            fontName='Helvetica',
            spaceAfter=0.01*cm  # Minimal reduziert für tighteres Layout
        )
        
        # OPTIMIERT: Position/Rolle mit verbessertem Styling
        custom_styles['Position'] = ParagraphStyle(
            'Position',
            parent=self.styles['Normal'],
            fontSize=9,
            fontName='Helvetica-Bold',
            spaceAfter=0.01*cm  # Minimal reduziert für tighteres Layout
        )
        
        # OPTIMIERT: Zeitraum-Stil mit verbessertem Spacing
        custom_styles['Period'] = ParagraphStyle(
            'Period',
            parent=self.styles['Normal'],
            fontSize=9,
            fontName='Helvetica-Bold',
            spaceAfter=0.05*cm  # Reduziert von 0.1cm
        )
        
        # Footer-Stil bleibt unverändert
        custom_styles['Footer'] = ParagraphStyle(
            'Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            fontName='Helvetica',
            textColor=colors.grey,
            alignment=1,
            spaceAfter=0,
            spaceBefore=0
        )
        
        return custom_styles
    
    def _get_company_logo_path(self, use_static=False):
        """
        Gibt den Pfad zum Unternehmenslogo zurück
        
        Args:
            use_static: Verwende static-Verzeichnis für HTTPS-Kompatibilität
        
        Returns:
            Pfad zum Logo oder None
        """
        try:
            # Verwende die company_config Hilfsfunktion
            logo_path = get_company_logo_path(self.selected_company)
            
            if logo_path and os.path.exists(logo_path):
                return logo_path
            
            # Fallback auf image_utils für HTTPS-Kompatibilität
            company_config = self.company_config
            logo_filename = company_config.get('logo_filename', 'galdoralogo.png')
            
            fallback_path = get_image_path(logo_filename, use_static=use_static)
            if fallback_path and os.path.exists(fallback_path):
                return fallback_path
            
            # Weitere Fallback-Pfade
            fallback_paths = [
                f"./static/images/{logo_filename}",
                f"../static/images/{logo_filename}"
            ]
            
            for path in fallback_paths:
                if os.path.exists(path):
                    print(f"Logo gefunden in Fallback-Pfad: {path}")
                    return path
            
            print(f"Warnung: Logo nicht gefunden für Unternehmen: {self.selected_company}")
            return None
            
        except Exception as e:
            print(f"Fehler beim Laden des Logos: {str(e)}")
            return None
    
    def _get_dynamic_footer_text(self):
        """
        Gibt den dynamischen Footer-Text basierend auf dem ausgewählten Unternehmen zurück
        
        Returns:
            Footer-Text als String
        """
        if self.selected_company == "bejob":
            return "bejob – einfach besser bewerben | Volksgartenstr. 85–89, 41065 Mönchengladbach | 02161 / 65326-40 | info@bejob.de | www.bejob.de"
        else:
            return "GALDORA Personalmanagement GmbH Co.KG\nVolksgartenstr. 85-89, 41065 Mönchengladbach\nE-Mail: info@galdora.de / Web: www.galdora.de"

def check_missing_profile_data(profile_data):
    """
    Überprüft, ob wichtige Felder in den Profildaten fehlen
    
    Args:
        profile_data: Dictionary mit Profildaten
    
    Returns:
        Liste mit fehlenden oder leeren Feldern
    """
    missing_fields = []
    
    # Überprüfe persönliche Daten
    personal_data = profile_data.get('persönliche_daten', {})
    if not personal_data.get('name'):
        missing_fields.append('Name')
    if not personal_data.get('wohnort'):
        missing_fields.append('Wohnort')
    if not personal_data.get('jahrgang'):
        missing_fields.append('Jahrgang/Geburtsdatum')
    
    # Überprüfe Berufserfahrung
    berufserfahrung = profile_data.get('berufserfahrung', [])
    if not berufserfahrung:
        missing_fields.append('Berufserfahrung')
    
    # Überprüfe Ausbildung
    ausbildung = profile_data.get('ausbildung', [])
    if not ausbildung:
        missing_fields.append('Ausbildung')
    
    return missing_fields
