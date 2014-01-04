django-sms-signup
=================

Sms_signup is a Django app to signup with user account
activation through sms without using an email. 

Quick start
-----------

1. Add "sms_signup" to your INSTALLED_APPS setting like this::
```python
INSTALLED_APPS = (
    ...

    'sendsms',
    'sms_signup',
)
```

2. Include the URLconf in your project urls.py like this::
```python
url(r'^$', TemplateView.as_view(template_name="base.html"), name='home'),
url(r'^signup/', include('sms_signup.urls')),
url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
url(r'^login/$',  LoginView.as_view(), name='login'),
url(r'^forgot_password/$',  PasswordRecoveryView.as_view(), name='forgot_password'),
url(r'^password_sent/$',  TemplateView.as_view(template_name = "password_sent.html"), name='password_sent'),
```
Parameters "name" of the base template must be exact in this example.

3. Copy templates from
https://github.com/bo858585/django-sms-signup/tree/feature/without_tests/sms_signup/templates ,
except base.html, to your project 'templates/sms_signup' folder.
Your project base.html must have login, logout, signup links and messages output like at the example.
4. `pip install -r requirements.txt`

5. Add lines to setting_local:: 
```python
PHONE_NUMBER_FROM = "+380974657365" # test
SENDSMS_BACKEND = 'sendsms.backends.console.SmsBackend'
```

6. Run `python manage.py syncdb` to create the sms_signup models.

7. Start the development server and visit http://127.0.0.1:8000/signup/

8. For a testing create settings_test.py::
```python
from .settings import *
SKIP_SOUTH_TESTS = True
SOUTH_TESTS_MIGRATE = False
inst = list(INSTALLED_APPS)
inst.remove('south')
INSTALLED_APPS = tuple(inst)
```
Then test application:
```python
pythonmanagepy test sms_signup --settings=project.settings_test
```
