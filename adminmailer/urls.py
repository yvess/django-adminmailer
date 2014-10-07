# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function  # python3
from __future__ import unicode_literals, division  # python3

from django.conf.urls import patterns, url
from .views import send_test, send_all

urlpatterns = patterns(
    '',
    url(r'^send_test/(?P<pk>\d+)/$',
        send_test,
        name='adminmailer_send_test'),
    url(r'^send_all/(?P<pk>\d+)/$',
        send_all,
        name='adminmailer_send_all'),
)
