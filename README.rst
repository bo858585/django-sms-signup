=====
Sms_signup
=====

Sms_signup is a Django app to signup with user account
activation through sms without using an email. 

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "sms_signup" to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'sms_signup',
      )

2. Include the polls URLconf in your project urls.py like this::

    url(r'^signup/', include('sms_signup.urls')),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^login/$',  LoginView.as_view(), name='login'),

3. Copy templates from

https://github.com/bo858585/django-sms-signup/tree/feature/without_tests/sms_signup/templates ,

except base.html, to your project templates folder.
Your project base.html must have login, logout, signup links and messages viewing as at the example.

3. pip install -r requirements.txt

4. Run `python manage.py syncdb` to create the sms_signup models.

5. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).

6. Visit http://127.0.0.1:8000/ to signup.
