# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function  # python3
from __future__ import unicode_literals, division  # python3
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib import messages as contrib_messages
from django.core.mail import EmailMessage
from django.conf import settings
from adminmailer.models import Message
from django.contrib.contenttypes.models import ContentType


@permission_required('is_superuser')
def send_all(request, pk=None):
    EMAIL_BACKEND_DEFAULT = settings.EMAIL_BACKEND
    settings.EMAIL_BACKEND = "mailer.backend.DbBackend"

    message = get_object_or_404(Message, pk=pk)
    if not message.was_sended:
        subject, body = message.subject, message.body
        sender = settings.ADMINMAILER_SENDER
        recipients = settings.ADMINMAILER['recipients']
        # '.' for django model instead of object attribute
        if '.' in recipients:
            app_label, model = recipients.split('.')
            recipient_list = ContentType.objects.get(
                app_label=app_label, model=model
            ).get_object_for_this_type(pk=120)
            #).get_all_objects_for_this_type()
        else:
            recipient_list = getattr(
                message.recipient_list, recipients)
            if hasattr(recipient_list, 'all'):
                recipient_list = recipient_list.all()

        extract_email_func = settings.ADMINMAILER['extract_email_func']
        recipients_emails = [
            extract_email_func(recipient) for recipient in recipient_list]
        for email in recipients_emails:
            msg = EmailMessage(
                subject, body, sender, [email])
            msg.send()
        message.total_sended = len(recipients_emails)
        message.recipients = ", ".join(recipients_emails)
        message.was_sended, message.date_sended = True, datetime.now()
        message.save()
        contrib_messages.add_message(
            request, contrib_messages.INFO,
            'Das Email wurde verschickt an: %s' % ", ".join(recipients_emails)
        )
    else:
        contrib_messages.add_message(
            request, contrib_messages.ERROR,
            'Sie können das Email nur einmal an alle verschicken'
        )
    settings.EMAIL_BACKEND = EMAIL_BACKEND_DEFAULT
    return redirect(request.META.get('HTTP_REFERER', None))


@permission_required('is_superuser')
def send_test(request, pk=None):
    message = get_object_or_404(Message, pk=pk)

    subject, body = message.subject, message.body
    sender = settings.ADMINMAILER_SENDER

    recipients = [email.strip() for email in message.test_email.split(",")]
    msg = EmailMessage(subject, body, sender, recipients)
    msg.send()
    contrib_messages.add_message(
        request, contrib_messages.INFO,
        'Das Test Email wurde verschickt an: %s' % ", ".join(recipients)
    )

    return redirect(request.META.get('HTTP_REFERER', None))
