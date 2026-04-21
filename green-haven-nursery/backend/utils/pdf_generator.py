"""
Green Haven Nursery - PDF Invoice Generator
Generates professional PDF invoices for orders
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from datetime import datetime
import os


def generate_invoice(order, user):
    """
    Generate PDF invoice for an order
    
    Args:
        order: Order object
        user: User object
    
    Returns:
        str: Path to generated PDF file
    """
    try:
        # Create invoices directory if it doesn't exist
        invoice_dir = os.path.join(os.path.dirname(__file__), '..', 'invoices')
        os.makedirs(invoice_dir, exist_ok=True)
        
        # Generate filename
        filename = f"invoice_{order.delivery_code}.pdf"
        filepath = os.path.join(invoice_dir, filename)
        
        # Create PDF
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        elements = []
        
        # Styles
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2D5016'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#2D5016'),
            spaceAfter=12
        )
        
        # Title
        title = Paragraph("🌱 Green Haven Nursery", title_style)
        elements.append(title)
        
        subtitle = Paragraph("INVOICE", styles['Heading2'])
        elements.append(subtitle)
        elements.append(Spacer(1, 0.3*inch))
        
        # Invoice details
        invoice_data = [
            ['Invoice Number:', f"#{order.id}"],
            ['Delivery Code:', order.delivery_code],
            ['Date:', order.created_at.strftime('%B %d, %Y')],
            ['Status:', order.status.upper()],
            ['Payment Method:', 'Cash on Delivery (COD)']
        ]
        
        invoice_table = Table(invoice_data, colWidths=[2*inch, 4*inch])
        invoice_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2D5016')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(invoice_table)
        elements.append(Spacer(1, 0.4*inch))
        
        # Customer details
        customer_heading = Paragraph("Bill To:", heading_style)
        elements.append(customer_heading)
        
        customer_data = [
            ['Name:', user.name],
            ['Email:', user.email],
            ['Phone:', user.phone],
            ['Address:', order.delivery_address]
        ]
        
        customer_table = Table(customer_data, colWidths=[1.5*inch, 4.5*inch])
        customer_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica', 10),
            ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#2D5016')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(customer_table)
        elements.append(Spacer(1, 0.4*inch))
        
        # Order items
        items_heading = Paragraph("Order Items:", heading_style)
        elements.append(items_heading)
        
        # Items table header
        items_data = [['Item', 'Quantity', 'Price', 'Subtotal']]
        
        # Items rows
        for item in order.items:
            items_data.append([
                item.product.name,
                str(item.quantity),
                f"${float(item.price):.2f}",
                f"${item.get_subtotal():.2f}"
            ])
        
        # Add total row
        items_data.append(['', '', 'TOTAL:', f"${float(order.total_amount):.2f}"])
        
        items_table = Table(items_data, colWidths=[3*inch, 1*inch, 1*inch, 1*inch])
        items_table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2D5016')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 11),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            
            # Body
            ('FONT', (0, 1), (-1, -2), 'Helvetica', 10),
            ('ALIGN', (1, 1), (-1, -2), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            
            # Total row
            ('FONT', (0, -1), (-1, -1), 'Helvetica-Bold', 12),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.HexColor('#2D5016')),
            ('ALIGN', (2, -1), (-1, -1), 'RIGHT'),
            ('TOPPADDING', (0, -1), (-1, -1), 12),
            
            # Grid
            ('GRID', (0, 0), (-1, -2), 0.5, colors.grey),
            ('LINEABOVE', (0, -1), (-1, -1), 2, colors.HexColor('#2D5016')),
            
            # Padding
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(items_table)
        elements.append(Spacer(1, 0.5*inch))
        
        # Footer notes
        notes = Paragraph(
            "<b>Important:</b> Please keep your delivery code ready when the driver arrives. "
            "Payment will be collected at the time of delivery.",
            styles['Normal']
        )
        elements.append(notes)
        elements.append(Spacer(1, 0.3*inch))
        
        footer = Paragraph(
            "Thank you for choosing Green Haven Nursery!<br/>"
            "For questions or support, contact us at info@greenhaven.com or (555) 123-4567",
            ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=9,
                textColor=colors.grey,
                alignment=TA_CENTER
            )
        )
        elements.append(footer)
        
        # Build PDF
        doc.build(elements)
        
        return filepath
        
    except Exception as e:
        print(f"PDF generation error: {str(e)}")
        return None
