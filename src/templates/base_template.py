"""
Base Template Generator
Eliminates code duplication in template generation by providing common functionality.
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from typing import Dict, List, Any, Tuple
from src.core.config_manager import LayoutConstants
from src.core.error_handler import safe_streamlit_operation, ErrorHandler


class BaseTableGenerator:
    """Base class for generating tables in PDF templates"""
    
    def __init__(self, custom_styles: Dict[str, ParagraphStyle]):
        self.styles = custom_styles
        self.layout = LayoutConstants()
    
    def create_generic_table(self, data: Dict[str, Any], table_type: str) -> Tuple[Table, List]:
        """Create a generic table for experience, education, or training entries"""
        try:
            if table_type == "experience":
                return self._create_experience_table(data)
            elif table_type == "education":
                return self._create_education_table(data)
            elif table_type == "training":
                return self._create_training_table(data)
            else:
                raise ValueError(f"Unknown table type: {table_type}")
        except Exception as e:
            ErrorHandler.handle_template_error(e, f"{table_type}_table")
            return None, []
    
    def _create_experience_table(self, entry: Dict[str, Any]) -> Tuple[Table, List]:
        """Create table for work experience entry"""
        zeitraum = self._sanitize_zeitraum(entry.get('zeitraum', ''))
        unternehmen = entry.get('unternehmen', '')
        position = entry.get('position', '')
        aufgaben = entry.get('aufgaben', [])
        
        # Limit tasks for layout optimization
        max_tasks = self.layout.MAX_TASKS_PER_ENTRY
        if len(aufgaben) > max_tasks:
            aufgaben = aufgaben[:max_tasks]
        
        # Format tasks as paragraphs
        aufgaben_formatted = [
            Paragraph(f"• {aufgabe}", self.styles['Normal']) 
            for aufgabe in aufgaben
        ]
        
        # Build right column content
        right_column_content = [
            Paragraph(unternehmen, self.styles['Position']),
            Paragraph(position, self.styles['Company'])
        ]
        right_column_content.extend(aufgaben_formatted)
        
        # Create table data
        table_data = self._build_table_data(zeitraum, right_column_content)
        
        # Create and style table
        table = self._create_styled_table(table_data)
        
        return table, [Spacer(1, self.layout.ENTRY_SPACING*cm)]
    
    def _create_education_table(self, entry: Dict[str, Any]) -> Tuple[Table, List]:
        """Create table for education entry"""
        zeitraum = self._sanitize_zeitraum(entry.get('zeitraum', ''))
        institution = entry.get('institution', '')
        abschluss = entry.get('abschluss', '')
        schwerpunkte = entry.get('schwerpunkte', '')
        
        # Build right column content
        right_column_content = [Paragraph(institution, self.styles['Position'])]
        
        if abschluss:
            right_column_content.append(Paragraph(abschluss, self.styles['Company']))
        
        # Add focus areas as bullet points
        if schwerpunkte:
            schwerpunkte_liste = schwerpunkte.split(", ")
            for schwerpunkt in schwerpunkte_liste:
                right_column_content.append(
                    Paragraph(f"• {schwerpunkt}", self.styles['Normal'])
                )
        
        # Handle additional tasks if present
        if 'aufgaben' in entry and isinstance(entry['aufgaben'], list):
            for aufgabe in entry['aufgaben']:
                right_column_content.append(
                    Paragraph(f"• {aufgabe}", self.styles['Normal'])
                )
        
        # Create table data
        table_data = self._build_table_data(zeitraum, right_column_content)
        
        # Create and style table
        table = self._create_styled_table(table_data)
        
        return table, [Spacer(1, self.layout.ENTRY_SPACING*cm)]
    
    def _create_training_table(self, entry: Dict[str, Any]) -> Tuple[Table, List]:
        """Create table for training/continuing education entry"""
        zeitraum = self._sanitize_zeitraum(entry.get('zeitraum', ''))
        bezeichnung = entry.get('bezeichnung', '')
        abschluss = entry.get('abschluss', '')
        
        # Build right column content
        bezeichnung_clean = bezeichnung.replace("zur ", "").replace("zum ", "")
        right_column_content = [
            Paragraph(f"Fortbildung zum {bezeichnung_clean}", self.styles['Position'])
        ]
        
        if abschluss and abschluss not in bezeichnung:
            right_column_content.append(Paragraph(abschluss, self.styles['Company']))
        
        # Add content/tasks if present
        for field in ['inhalte', 'aufgaben']:
            if field in entry and isinstance(entry[field], list):
                for item in entry[field]:
                    right_column_content.append(
                        Paragraph(f"• {item}", self.styles['Normal'])
                    )
        
        # Create table data
        table_data = self._build_table_data(zeitraum, right_column_content)
        
        # Create and style table
        table = self._create_styled_table(table_data)
        
        return table, [Spacer(1, self.layout.ENTRY_SPACING*cm)]
    
    def _sanitize_zeitraum(self, zeitraum: str) -> str:
        """Sanitize time period strings"""
        if not zeitraum:
            return ""
        
        # Replace common variations of "until now"
        replacements = {
            "bis jetzt": "2025",
            "bis heute": "2025", 
            "bis JETZT": "2025"
        }
        
        for old, new in replacements.items():
            zeitraum = zeitraum.replace(old, new)
        
        return zeitraum
    
    def _build_table_data(self, zeitraum: str, right_column_content: List) -> List[List]:
        """Build table data structure for consistent formatting"""
        table_data = [
            [Paragraph(zeitraum, self.styles['Period']), right_column_content[0]]
        ]
        
        # Add empty cell for remaining content
        if len(right_column_content) > 1:
            table_data.append([Paragraph('', self.styles['Normal']), right_column_content[1]])
        
        # Add spacing before tasks if needed
        if len(right_column_content) > 2:
            table_data.append([Paragraph('', self.styles['Normal']), Spacer(1, 5)])
        
        # Add remaining content
        for j in range(2, len(right_column_content)):
            table_data.append([Paragraph('', self.styles['Normal']), right_column_content[j]])
        
        return table_data
    
    def _create_styled_table(self, table_data: List[List]) -> Table:
        """Create table with consistent styling"""
        col_widths = [A4[0] * self.layout.A4_WIDTH_FACTOR_LEFT, 
                     A4[0] * self.layout.A4_WIDTH_FACTOR_RIGHT]
        
        table = Table(table_data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (1, 0), (1, -1), self.layout.SECTION_SPACING*cm),
            ('BOTTOMPADDING', (0, 0), (0, 0), 0),
            ('TOPPADDING', (1, 1), (1, 1), 1),
        ]))
        
        return table


class SectionRenderer:
    """Renders common sections across different templates"""
    
    def __init__(self, styles: Dict[str, ParagraphStyle], table_generator: BaseTableGenerator):
        self.styles = styles
        self.table_generator = table_generator
    
    @safe_streamlit_operation("Section Rendering")
    def render_personal_data_section(self, elements: List, profile_data: Dict[str, Any]) -> None:
        """Render personal data section with consistent formatting"""
        personal_data = profile_data.get('persönliche_daten', {})
        
        # Name
        name = personal_data.get('name', 'Profil')
        elements.append(Paragraph(name, self.styles['Name']))
        
        # Create grayed style for secondary information
        grayed_style = ParagraphStyle(
            'GrayedLabelInline',
            parent=self.styles['LabelInline'],
            textColor=colors.grey
        )
        
        # Add personal information
        self._add_personal_info(elements, personal_data, profile_data, grayed_style)
    
    def _add_personal_info(self, elements: List, personal_data: Dict[str, Any], 
                          profile_data: Dict[str, Any], grayed_style: ParagraphStyle) -> None:
        """Add personal information paragraphs"""
        info_fields = [
            ('wohnort', 'Wohnort'),
            ('jahrgang', 'Jahrgang'),
            ('führerschein', 'Führerschein')
        ]
        
        for field, label in info_fields:
            value = personal_data.get(field, '')
            if value and value.strip():
                elements.append(Paragraph(f"{label}: {value}", grayed_style))
        
        # Add availability information
        self._add_availability_info(elements, profile_data, grayed_style)
        
        # Add salary expectations
        wunschgehalt = profile_data.get('wunschgehalt', '')
        if wunschgehalt:
            elements.append(Paragraph(f"Gehaltsvorstellung: {wunschgehalt}", grayed_style))
    
    def _add_availability_info(self, elements: List, profile_data: Dict[str, Any], 
                              grayed_style: ParagraphStyle) -> None:
        """Add availability information"""
        verfuegbarkeit_status = profile_data.get('verfuegbarkeit_status', '')
        verfuegbarkeit_details = profile_data.get('verfuegbarkeit_details', '')
        
        if verfuegbarkeit_status:
            if verfuegbarkeit_details:
                elements.append(Paragraph(f"ab {verfuegbarkeit_details}", grayed_style))
            else:
                elements.append(Paragraph(f"ab {verfuegbarkeit_status}", grayed_style))
    
    @safe_streamlit_operation("Contact Section Rendering")
    def render_contact_section(self, elements: List, personal_data: Dict[str, Any]) -> None:
        """Render contact information section"""
        from reportlab.platypus import HRFlowable
        
        kontakt = personal_data.get('kontakt', {})
        ansprechpartner = kontakt.get('ansprechpartner', '')
        
        if ansprechpartner and ansprechpartner.strip() and ansprechpartner != "Kein Ansprechpartner":
            elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey, 
                                     spaceBefore=3, spaceAfter=12))
            elements.append(Paragraph("IHR ANSPRECHPARTNER", self.styles['ContactHeader']))
            
            # Format contact person name
            anrede = self._format_contact_name(ansprechpartner)
            
            # Get contact details
            telefon, email = self._get_contact_details(ansprechpartner, kontakt)
            
            # Create grayed contact style
            grayed_contact_style = ParagraphStyle(
                'GrayedContactData',
                parent=self.styles['ContactData'],
                textColor=colors.grey
            )
            
            # Add contact information
            elements.append(Paragraph(ansprechpartner, grayed_contact_style))
            
            if telefon:
                elements.append(Paragraph(f"Tel.: {telefon}", grayed_contact_style))
            
            if email:
                elements.append(Paragraph(f"E-Mail: {email}", grayed_contact_style))
            
            elements.append(Spacer(1, 12))
            elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey, 
                                     spaceBefore=3, spaceAfter=12))
    
    def _format_contact_name(self, ansprechpartner: str) -> str:
        """Format contact person name with appropriate title"""
        if ansprechpartner == "Melike Demirkol":
            return "Frau Demirkol"
        elif ansprechpartner == "Alessandro Böhm":
            return "Herr Böhm"
        else:
            nachname = ansprechpartner.split()[-1] if ansprechpartner else 'Fischer'
            return f"Herr {nachname}"
    
    def _get_contact_details(self, ansprechpartner: str, kontakt: Dict[str, Any]) -> Tuple[str, str]:
        """Get contact details (phone, email) for specific contact person"""
        # Default phone number
        telefon = "02161 62126-00"
        
        # Special case for Salim Alizai
        if ansprechpartner == "Salim Alizai":
            telefon = kontakt.get('telefon', telefon)
        
        # Email handling
        email_mappings = {
            "Alessandro Böhm": "boehm@galdora.de",
            "Salim Alizai": "gl@galdora.de", 
            "Konrad Ruszczyk": "konrad@galdora.de"
        }
        
        email = email_mappings.get(ansprechpartner)
        if not email:
            # Fallback email generation
            nachname = ansprechpartner.split()[-1] if ansprechpartner else 'fischer'
            email = kontakt.get("email", f"{nachname.lower()}@galdora.de")
        
        return telefon, email