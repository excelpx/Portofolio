"""
Email Service Integration with Resend
Handles email sending for portfolio contact notifications
"""

import os
import logging
from typing import Optional, Dict, Any

try:
    import resend
    RESEND_AVAILABLE = True
except ImportError:
    RESEND_AVAILABLE = False
    logging.warning("Resend library not installed. Email functionality will be disabled.")

logger = logging.getLogger(__name__)

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "Excel.peter321@gmail.com")


def initialize_resend():
    """
    Initialize Resend email service with API key from environment variables
    Should be called once when application starts
    
    Returns:
        bool: True if initialization successful, False otherwise
    """
    if not RESEND_AVAILABLE:
        logger.warning("Resend library is not available")
        return False
    
    try:
        api_key = os.getenv("RESEND_API_KEY")
        
        if not api_key:
            logger.error("RESEND_API_KEY not found in environment variables")
            return False
        
        resend.api_key = api_key
        logger.info("✓ Resend email service initialized successfully")
        return True
    
    except Exception as e:
        logger.error(f"✗ Failed to initialize Resend: {e}")
        return False


def kirim_email_notifikasi(
    nama: str,
    email_pengirim: str,
    subjek: str,
    pesan: str,
    email_penerima: Optional[str] = None
) -> Dict[str, Any]:
    """
    Send email notification to admin about contact form submission
    
    This function sends an email notification to the portfolio admin
    when someone submits a contact form. It includes the sender's
    information and their message.
    
    Args:
        nama (str): Name of the person sending the message
        email_pengirim (str): Email address of the sender
        subjek (str): Subject of the message
        pesan (str): Content of the message
        email_penerima (str, optional): Email address to receive notification
                                        Defaults to ADMIN_EMAIL from .env
    
    Returns:
        dict: Dictionary containing:
            - 'success' (bool): Whether email was sent successfully
            - 'message_id' (str): Resend message ID (if successful)
            - 'error' (str): Error message (if failed)
            - 'timestamp' (str): When the email was sent
    
    Example:
        result = kirim_email_notifikasi(
            nama="John Doe",
            email_pengirim="john@example.com",
            subjek="Penawaran Kerja",
            pesan="Saya tertarik dengan portfolio Anda..."
        )
        
        if result['success']:
            print(f"Email sent with ID: {result['message_id']}")
        else:
            print(f"Error: {result['error']}")
    """
    
    if not RESEND_AVAILABLE:
        return {
            'success': False,
            'error': 'Resend library is not available. Email service disabled.'
        }
    
    recipient_email = email_penerima or ADMIN_EMAIL
    
    if not nama or not nama.strip():
        return {
            'success': False,
            'error': 'Nama pengirim tidak boleh kosong'
        }
    
    if not email_pengirim or '@' not in email_pengirim:
        return {
            'success': False,
            'error': 'Email pengirim tidak valid'
        }
    
    if not subjek or not subjek.strip():
        return {
            'success': False,
            'error': 'Subjek tidak boleh kosong'
        }
    
    if not pesan or not pesan.strip():
        return {
            'success': False,
            'error': 'Pesan tidak boleh kosong'
        }
    
    if not recipient_email or '@' not in recipient_email:
        return {
            'success': False,
            'error': 'Email penerima tidak valid'
        }
    
    try:
        html_body = f"""
        <html>
            <head>
                <style>
                    body {{
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                        color: #333;
                        line-height: 1.6;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        padding: 20px;
                        border: 1px solid #ddd;
                        border-radius: 8px;
                        background-color: #f9f9f9;
                    }}
                    .header {{
                        background-color: #007bff;
                        color: white;
                        padding: 20px;
                        border-radius: 8px 8px 0 0;
                        margin: -20px -20px 20px -20px;
                    }}
                    .content {{
                        margin: 20px 0;
                    }}
                    .field {{
                        margin: 15px 0;
                        padding: 10px;
                        background-color: white;
                        border-left: 4px solid #007bff;
                        padding-left: 15px;
                    }}
                    .label {{
                        font-weight: bold;
                        color: #007bff;
                    }}
                    .footer {{
                        margin-top: 30px;
                        padding-top: 20px;
                        border-top: 1px solid #ddd;
                        font-size: 12px;
                        color: #666;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h2>📬 New Portfolio Contact Message</h2>
                    </div>
                    
                    <div class="content">
                        <div class="field">
                            <span class="label">Nama Pengirim:</span><br>
                            {nama}
                        </div>
                        
                        <div class="field">
                            <span class="label">Email Pengirim:</span><br>
                            <a href="mailto:{email_pengirim}">{email_pengirim}</a>
                        </div>
                        
                        <div class="field">
                            <span class="label">Subjek:</span><br>
                            {subjek}
                        </div>
                        
                        <div class="field">
                            <span class="label">Pesan:</span><br>
                            {pesan.replace(chr(10), '<br>')}
                        </div>
                    </div>
                    
                    <div class="footer">
                        <p>Pesan ini dikirim secara otomatis dari formulir kontak di portfolio Anda.</p>
                        <p>Jangan lupa balas pesan dari pengirim di: <strong>{email_pengirim}</strong></p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        text_body = f"""
        Nama Pengirim: {nama}
        Email Pengirim: {email_pengirim}
        Subjek: {subjek}
        
        Pesan:
        {pesan}
        
        ---
        Pesan ini dikirim secara otomatis dari formulir kontak di portfolio Anda.
        """
        
        response = resend.Emails.send(
            {
                "from": f"Portfolio <noreply@{_get_domain_from_email(recipient_email)}>",
                "to": recipient_email,
                "subject": f"[Portfolio Contact] {subjek}",
                "html": html_body,
                "text": text_body,
                "reply_to": email_pengirim
            }
        )
        
        if response.get("id"):
            logger.info(f"✓ Email sent successfully to {recipient_email}")
            return {
                'success': True,
                'message_id': response.get("id"),
                'timestamp': response.get("created_at")
            }
        else:
            logger.error(f"✗ Failed to send email: {response}")
            return {
                'success': False,
                'error': response.get('message', 'Failed to send email')
            }
    
    except Exception as e:
        logger.error(f"✗ Exception while sending email: {e}")
        return {
            'success': False,
            'error': f'Failed to send email: {str(e)}'
        }


def kirim_email_konfirmasi(
    nama: str,
    email_pengirim: str
) -> Dict[str, Any]:
    """
    Send confirmation email to the person who submitted the form
    
    Args:
        nama (str): Name of the person
        email_pengirim (str): Email of the person
    
    Returns:
        dict: Result of email sending
    
    Example:
        result = kirim_email_konfirmasi(
            nama="John Doe",
            email_pengirim="john@example.com"
        )
    """
    
    if not RESEND_AVAILABLE:
        return {
            'success': False,
            'error': 'Resend library is not available'
        }
    
    try:
        html_body = f"""
        <html>
            <head>
                <style>
                    body {{
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                        color: #333;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        padding: 20px;
                        border: 1px solid #ddd;
                        border-radius: 8px;
                    }}
                    .header {{
                        background-color: #28a745;
                        color: white;
                        padding: 20px;
                        border-radius: 8px;
                        margin-bottom: 20px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h2>✓ Pesan Anda Diterima</h2>
                    </div>
                    
                    <p>Halo <strong>{nama}</strong>,</p>
                    
                    <p>Terima kasih telah menghubungi kami melalui formulir kontak portfolio.</p>
                    
                    <p>Pesan Anda telah kami terima dan akan kami balas sesegera mungkin.</p>
                    
                    <p>Best regards,<br>
                    Portfolio Team</p>
                </div>
            </body>
        </html>
        """
        
        response = resend.Emails.send(
            {
                "from": f"Portfolio <noreply@{_get_domain_from_email(email_pengirim)}>",
                "to": email_pengirim,
                "subject": "✓ Kami Telah Menerima Pesan Anda",
                "html": html_body
            }
        )
        
        if response.get("id"):
            logger.info(f"✓ Confirmation email sent to {email_pengirim}")
            return {
                'success': True,
                'message_id': response.get("id")
            }
        else:
            logger.error(f"✗ Failed to send confirmation email")
            return {
                'success': False,
                'error': 'Failed to send confirmation email'
            }
    
    except Exception as e:
        logger.error(f"✗ Exception while sending confirmation email: {e}")
        return {
            'success': False,
            'error': str(e)
        }


def _get_domain_from_email(email: str) -> str:
    """
    Extract domain from email address
    Helper function for email sender configuration
    
    Args:
        email (str): Email address
    
    Returns:
        str: Domain name
    """
    try:
        return email.split('@')[1]
    except IndexError:
        return "example.com"


"""
from Backend.utama.email_service import initialize_resend
initialize_resend()


from flask import request, jsonify
from Backend.utama.email_service import kirim_email_notifikasi, kirim_email_konfirmasi

@app.route('/api/kontak', methods=['POST'])
def handle_contact():
    data = request.json
    
    notif_result = kirim_email_notifikasi(
        nama=data['nama'],
        email_pengirim=data['email'],
        subjek=data['subjek'],
        pesan=data['pesan']
    )
    
    if notif_result['success']:
        kirim_email_konfirmasi(data['nama'], data['email'])
    
    if notif_result['success']:
        return jsonify({'message': 'Email sent successfully'}), 200
    else:
        return jsonify({'error': notif_result['error']}), 400
"""
