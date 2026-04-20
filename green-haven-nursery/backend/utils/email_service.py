"""
Green Haven Nursery - Email Service
Sends order confirmation emails with delivery codes
"""

from flask import current_app
from flask_mail import Message
from app import mail
import os


def send_order_confirmation(user, order, invoice_path=None):
    """
    Send order confirmation email to customer
    
    Args:
        user: User object
        order: Order object
        invoice_path: Path to invoice PDF (optional)
    """
    try:
        subject = f"Order Confirmation - {order.delivery_code}"
        
        # Email body (HTML)
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                }}
                .header {{
                    background: linear-gradient(135deg, #2D5016 0%, #4A7C2F 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                }}
                .content {{
                    padding: 30px;
                    background: #f9f9f9;
                }}
                .order-details {{
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 20px 0;
                }}
                .delivery-code {{
                    background: #E8F5E9;
                    color: #2D5016;
                    padding: 15px;
                    border-radius: 8px;
                    text-align: center;
                    font-size: 24px;
                    font-weight: bold;
                    margin: 20px 0;
                    border: 2px dashed #2D5016;
                }}
                .item {{
                    border-bottom: 1px solid #eee;
                    padding: 10px 0;
                }}
                .total {{
                    font-size: 20px;
                    font-weight: bold;
                    color: #2D5016;
                    text-align: right;
                    padding: 15px 0;
                }}
                .footer {{
                    text-align: center;
                    padding: 20px;
                    color: #666;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🌱 Green Haven Nursery</h1>
                <p>Thank you for your order!</p>
            </div>
            
            <div class="content">
                <h2>Hi {user.name},</h2>
                <p>We're excited to confirm your order! Your beautiful plants will be carefully packaged and delivered soon.</p>
                
                <div class="delivery-code">
                    <div style="font-size: 14px; margin-bottom: 5px;">Your Delivery Code</div>
                    {order.delivery_code}
                </div>
                
                <p><strong>Please keep this code handy</strong> - you'll need it to receive your delivery.</p>
                
                <div class="order-details">
                    <h3>Order Details</h3>
                    <p><strong>Order ID:</strong> #{order.id}</p>
                    <p><strong>Order Date:</strong> {order.created_at.strftime('%B %d, %Y')}</p>
                    <p><strong>Payment Method:</strong> Cash on Delivery (COD)</p>
                    
                    <h4>Items:</h4>
                    {"".join([f'''
                    <div class="item">
                        <div style="display: flex; justify-content: space-between;">
                            <span>{item.product.name} x {item.quantity}</span>
                            <span>${item.get_subtotal()}</span>
                        </div>
                    </div>
                    ''' for item in order.items])}
                    
                    <div class="total">
                        Total: ${float(order.total_amount):.2f}
                    </div>
                    
                    <h4>Delivery Address:</h4>
                    <p>{order.delivery_address}</p>
                </div>
                
                <h3>What's Next?</h3>
                <ul>
                    <li>Your plants are being carefully prepared for delivery</li>
                    <li>Expected delivery: 3-5 business days</li>
                    <li>Keep your delivery code ready when the driver arrives</li>
                    <li>Payment will be collected upon delivery</li>
                </ul>
                
                <h3>Care Instructions</h3>
                <p>Each plant comes with detailed care instructions. For additional support, visit our website or contact us at info@greenhaven.com</p>
            </div>
            
            <div class="footer">
                <p>Green Haven Nursery | Bringing nature to your doorstep</p>
                <p>Email: info@greenhaven.com | Phone: (555) 123-4567</p>
                <p>If you have any questions, please don't hesitate to contact us.</p>
            </div>
        </body>
        </html>
        """
        
        # Plain text version
        text_body = f"""
        Green Haven Nursery - Order Confirmation
        
        Hi {user.name},
        
        Thank you for your order!
        
        Your Delivery Code: {order.delivery_code}
        (Please keep this code - you'll need it for delivery)
        
        Order Details:
        Order ID: #{order.id}
        Order Date: {order.created_at.strftime('%B %d, %Y')}
        Payment Method: Cash on Delivery (COD)
        
        Items:
        {"".join([f"{item.product.name} x {item.quantity} - ${item.get_subtotal()}\n" for item in order.items])}
        
        Total: ${float(order.total_amount):.2f}
        
        Delivery Address:
        {order.delivery_address}
        
        Expected Delivery: 3-5 business days
        
        Questions? Contact us at info@greenhaven.com or (555) 123-4567
        
        Best regards,
        Green Haven Nursery Team
        """
        
        # Create message
        msg = Message(
            subject=subject,
            recipients=[user.email],
            body=text_body,
            html=html_body
        )
        
        # Attach invoice if available
        if invoice_path and os.path.exists(invoice_path):
            with open(invoice_path, 'rb') as f:
                msg.attach(
                    f"invoice_{order.delivery_code}.pdf",
                    "application/pdf",
                    f.read()
                )
        
        # Send email
        mail.send(msg)
        
        return True
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        # Log error but don't fail the order
        return False


def send_test_email(recipient):
    """
    Send a test email to verify email configuration
    
    Args:
        recipient (str): Email address to send test email to
    """
    try:
        msg = Message(
            subject="Test Email - Green Haven Nursery",
            recipients=[recipient],
            body="This is a test email from Green Haven Nursery. If you received this, email configuration is working correctly!"
        )
        
        mail.send(msg)
        return True
        
    except Exception as e:
        print(f"Test email error: {str(e)}")
        return False
