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
    'sms_signup',
)
```

2. Include the polls URLconf in your project urls.py like this::

```python
url(r'^$', TemplateView.as_view(template_name="base.html"), name='home'),
url(r'^signup/', include('sms_signup.urls')),
url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
url(r'^login/$',  LoginView.as_view(), name='login'),
```

3. Copy templates from

https://github.com/bo858585/django-sms-signup/tree/feature/without_tests/sms_signup/templates ,

except base.html, to your project 'templates/sms_signup' folder.
Your project base.html must have login, logout, signup links and messages output like at the example.

4. `pip install -r requirements.txt`

5. Run `python manage.py syncdb` to create the sms_signup models.

6. Start the development server and visit http://127.0.0.1:8000/signup/
