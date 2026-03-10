from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
# from customer.models import Customer

def send_welcome_email(customer):
    subject = 'Welcome to Our E-commerce Platform'
    to_email = (customer.email,)
    from_email = settings.DEFAULT_FROM_EMAIL

    html_content = render_to_string(
        'email/welcome_email.html',
        {"customer": customer}
    )

    email = EmailMultiAlternatives(
        subject,
        to=to_email,
        from_email=from_email
    )

    email.attach_alternative(html_content, 'text/html')
    email.send()

