django-sms-signup
=================

Sms_signup is a Django app to signup with user account
activation through sms without using an email. 

Quick start
-----------

1. Install https://github.com/DrMartiner/django-smsaero

2. At /admin/smsaero/ add signature "REKLAMA" to "Подписи сообщений" or get it with instructions here http://smsaero.ru/api/

3. `cd to your project apps directory`

4. `git clone git@github.com:bo858585/django-sms-signup.git`

5. `pip install django-sms-signup/dist/django-sms-signup-0.1.tar.gz`

6. Add "sms_signup" to your INSTALLED_APPS at setting.py:
```python
INSTALLED_APPS = (
    ...
    'sms_signup',
)
```

7. Include the URLconf in your project urls.py like here:
```python
url(r'^$', TemplateView.as_view(template_name="base.html"), name='home'),
url(r'^signup/', include('sms_signup.urls')),
url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
url(r'^login/$',  LoginView.as_view(), name='login'),
url(r'^forgot_password/$',  PasswordRecoveryView.as_view(), name='forgot_password'),
```
Parameters "name" of the base.html template must be exact as in this example.

8. Copy templates from
https://github.com/bo858585/django-sms-signup/tree/feature/without_tests/sms_signup/templates ,
except base.html, to your project 'templates/sms_signup' folder. Your project base.html must have login, logout, signup links and messages output like at this example.

9. Run `python manage.py syncdb` to create the sms_signup models.

10. Start the development server and visit http://127.0.0.1:8000/signup/

11. For a testing create settings_test.py:
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
pythonmanagepy test sms_signup.SMSSignupTests --settings=signup_project.settings_test
```
