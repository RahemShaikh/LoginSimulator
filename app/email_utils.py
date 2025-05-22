import smtplib, ssl
import config

def send_email(receiver_email, subject, message) -> None:
    '''
    Sends an email to the specified email address.

    Args:
        receiver_email (str): The email address of the receiver.
        subject (str): The subject line of the email.
        message (str): The body content of the email.
    '''

    # Port number for secure SMTP (SSL) connection
    port = 465

    # Create a secure SSL context for encrypted connection
    context = ssl.create_default_context()

    # Email address of the sender
    sender_email = config.SENDER_EMAIL
    
    # Connect securely to the SMTP server and send the email
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:

        # Log in to the SMTP server with sender credentials
        server.login(sender_email, config.SENDER_PASSWORD)
        
        # Format the email with subject line and message body
        email_message = f"Subject: {subject}\n\n{message}"
        server.sendmail(sender_email, receiver_email, email_message)