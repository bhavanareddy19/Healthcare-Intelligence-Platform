"""
Generate PDF versions of sample clinical notes
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import os

def create_pdf_from_text(input_file: str, output_file: str):
    """Convert a text file to PDF with proper formatting."""

    # Read the text file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Create PDF document
    doc = SimpleDocTemplate(
        output_file,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    # Define styles
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=14,
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=11,
        spaceBefore=12,
        spaceAfter=6,
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=9,
        leading=12,
        spaceAfter=6,
        fontName='Helvetica'
    )

    # Build the story (content)
    story = []

    # Process content line by line
    lines = content.split('\n')

    for line in lines:
        line = line.strip()

        if not line:
            story.append(Spacer(1, 6))
            continue

        # Escape special characters for reportlab
        line = line.replace('&', '&amp;')
        line = line.replace('<', '&lt;')
        line = line.replace('>', '&gt;')

        # Determine style based on content
        if line.isupper() and len(line) > 3 and ':' not in line:
            # Main headers (all caps without colon)
            story.append(Paragraph(line, title_style))
        elif line.endswith(':') and line.isupper():
            # Section headers (all caps ending with colon)
            story.append(Paragraph(line, heading_style))
        elif line.endswith(':') and len(line) < 50:
            # Sub-section headers
            story.append(Paragraph(f"<b>{line}</b>", body_style))
        else:
            # Regular body text
            story.append(Paragraph(line, body_style))

    # Build PDF
    doc.build(story)
    print(f"Created: {output_file}")

def main():
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define input/output files
    files = [
        ("sample_clinical_note_1.txt", "sample_clinical_note_1.pdf"),
        ("sample_clinical_note_2.txt", "sample_clinical_note_2.pdf"),
        ("sample_clinical_note_3.txt", "sample_clinical_note_3.pdf"),
    ]

    for txt_file, pdf_file in files:
        input_path = os.path.join(script_dir, txt_file)
        output_path = os.path.join(script_dir, pdf_file)

        if os.path.exists(input_path):
            create_pdf_from_text(input_path, output_path)
        else:
            print(f"Warning: {input_path} not found")

    print("\nAll PDFs generated successfully!")

if __name__ == "__main__":
    main()
