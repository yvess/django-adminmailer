from django.conf.urls import url
from .views import send_test, send_all

urlpatterns = [
    url(r'^send_test/(?P<pk>\d+)/$',
        send_test,
        name='adminmailer_send_test'),
    url(r'^send_all/(?P<pk>\d+)/$',
        send_all,
        name='adminmailer_send_all'),
]
