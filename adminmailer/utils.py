
from django.core.mail import EmailMessage
from django.contrib.contenttypes.models import ContentType
from django.conf import settings


def get_recipients(recipients, message):
    recipient_list = None
    #  '.' for django model instead of object attribute
    if ('recipient_list' in settings.ADMINMAILER and
       settings.ADMINMAILER['recipient_list'] and
       settings.ADMINMAILER['recipient_list'] != 'auth.group'):
        recipient_list = getattr(
            message.recipient_list, settings.ADMINMAILER['recipients'])
        if hasattr(recipient_list, 'all'):
            recipient_list = recipient_list.all()

    if '.' in recipients:
        app_label, model = recipients.split('.')
        objects = ContentType.objects.get(
            app_label=app_label, model=model
        )
        recipient_list = objects.get_all_objects_for_this_type()
    if '.' not in recipients and recipient_list:
        recipient_list = getattr(
            message.recipient_list, recipients)
        if hasattr(recipient_list, 'all'):
            recipient_list = recipient_list.all()
    if 'recipient_condition' in settings.ADMINMAILER:
        to_include = settings.ADMINMAILER['recipient_condition']
        recipient_list = [r for r in recipient_list if to_include(r)]
    return recipient_list


def create_email(subject, body, sender,
                 recipient, overwrite_email_recipients=None):
    extract_email_func = settings.ADMINMAILER['extract_email_func']
    if not overwrite_email_recipients:
        email_recipients = [extract_email_func(recipient)]
    else:
        email_recipients = overwrite_email_recipients

    if 'template_context' in settings.ADMINMAILER:
        for key, func in settings.ADMINMAILER['template_context'].items():
            body = body.replace(key, func(recipient))
    return EmailMessage(
        subject, body, sender, email_recipients
    )
