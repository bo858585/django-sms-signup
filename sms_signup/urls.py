from django.conf.urls import patterns, include, url
from views import RegistrationView, ActivationView

urlpatterns = patterns('',
    url(r'^$', RegistrationView.as_view(), name="signup"),
    url(r'^activation/(?P<phone>[\d]{11,12})/$', ActivationView.as_view(), name="signup_activation"),
)

