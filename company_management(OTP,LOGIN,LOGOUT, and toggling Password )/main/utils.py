import random
from datetime import datetime, timedelta
from django.core.mail import send_mail
from smtplib import SMTPException  # Correct import for SMTPException
import logging

logger = logging.getLogger(__name__)

def generate_otp():
    """
    Generate a 6-digit OTP.
    """
    return random.randint(100000, 999999)

def is_otp_expired(timestamp, expiry_minutes=5):
    """
    Check if the OTP has expired.
    :param timestamp: The timestamp when the OTP was generated.
    :param expiry_minutes: Time in minutes after which the OTP expires.
    :return: True if expired, False otherwise.
    """
    return datetime.now() - timestamp > timedelta(minutes=expiry_minutes)

def send_otp_email(email, otp):
    """
    Send an OTP email.
    :param email: Recipient's email address.
    :param otp: The OTP to send.
    :return: None
    :raises: SMTPException if the email fails to send.
    """
    subject = 'OTP Verification'
    message = f'Your OTP is {otp}. It is valid for 5 minutes.'
    from_email = 'heifermpc@example.com'  # Replace with your email
    try:
        send_mail(subject, message, from_email, [email], fail_silently=False)
        logger.info(f"OTP email sent to {email}")
    except SMTPException as e:
        logger.error(f"SMTPException: Failed to send email to {email}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while sending email to {email}: {e}")
        raise
