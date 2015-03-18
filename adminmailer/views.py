# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function  # python3
from __future__ import unicode_literals, division  # python3
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib import messages as contrib_messages
from django.conf import settings
from adminmailer.models import Message
from .utils import create_email, get_recipients


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

        recipient_list = get_recipients(recipients, message)
        recipients_emails = []
        extract_email_func = settings.ADMINMAILER['extract_email_func']
        for recipient in recipient_list:
            to_email = extract_email_func(recipient)
            if '@' in to_email:
                recipients_emails.append(to_email)
                msg = create_email(subject, body, sender, recipient)
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

    email_recipients = [email.strip() for email in message.test_email.split(",")]
    recipients = settings.ADMINMAILER['recipients']
    recipient_list = get_recipients(recipients, message)
    msg = create_email(
        subject, body, sender,
        recipient_list[0], overwrite_email_recipients=email_recipients
    )
    msg.send()
    contrib_messages.add_message(
        request, contrib_messages.INFO,
        'Das Test Email wurde verschickt an: %s' % ", ".join(email_recipients)
    )

    return redirect(request.META.get('HTTP_REFERER', None))
