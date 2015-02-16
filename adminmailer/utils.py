# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function  # python3
from __future__ import unicode_literals, division  # python3
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
        recipient_list = [objects.get_object_for_this_type(pk=120)]
        # recipient_list = objects.get_all_objects_for_this_type()
    if '.' not in recipients and recipient_list:
        recipient_list = getattr(
            message.recipient_list, recipients)
        if hasattr(recipient_list, 'all'):
            recipient_list = recipient_list.all()
    return recipient_list


def create_email(subject, body, sender,
                 recipient, overwrite_email_recipients=None):
    extract_email_func = settings.ADMINMAILER['extract_email_func']
    if not overwrite_email_recipients:
        email_recipients = [extract_email_func(recipient)]
    else:
        email_recipients = overwrite_email_recipients

    if 'template_context' in settings.ADMINMAILER:
        for key, func in settings.ADMINMAILER['template_context'].iteritems():
            body.replace(key, func(recipient))
    return EmailMessage(
        subject, body, sender, email_recipients
    )