from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from .tokens import generate_token


@shared_task
def send_activation_mail(user,current_site):
    mail_subject = 'Activate your Expense Tracker account'
    message = render_to_string('active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':generate_token.make_token(user),
    })
    email = EmailMessage(
                mail_subject, message, to=[user.email]
    )
    email.send()
    
    