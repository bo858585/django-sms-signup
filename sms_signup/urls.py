from django.conf.urls import patterns, include, url
from views import RegistrationView, ActivationView

from  forms import REGEX

urlpatterns = patterns('',
    url(r'^$', RegistrationView.as_view(), name="signup"),
    url(r'^activation/(?P<phone>' + REGEX + r')/$', ActivationView.as_view(), name="signup_activation"),
)

