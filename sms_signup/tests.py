# -*- coding: utf-8 -*-

"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django_webtest import WebTest
from .models import WorkerSMSCode
from django.core.urlresolvers import reverse
import datetime
from django.utils.timezone import utc


from random import randint


class SignupTestCase(WebTest):
    csrf_checks = False
    extra_environ = {'HTTP_ACCEPT_LANGUAGE': 'ru'}

    def test_signup(self):
        test_sms_code = "test_sms_code"
        test_phone = randint(10000000000, 99999999999999)
        worker_sms_code = WorkerSMSCode(
            sms_code=test_sms_code,
            phone=test_phone,
            sms_code_init_time=datetime.datetime.utcnow().replace(tzinfo=utc),
            is_activated=True
        )
        worker_sms_code.save()

        url = reverse('signup')
        res = self.app.post(url, { "username": test_phone }, expect_errors=True)
        print res.context
        self.assertEquals(res.status_code, 200, 'Request for added leader was passet')
#        self.assertEquals(
 #           worker_sms_code,
  #          WorkerSMSCode.objects.get(pk=worker_sms_code.pk),
   #         'Paid to date was changed'
    #    )
        print res

    def test_labels_existing_at_worker_signup(self):
        signup = self.app.get('/signup/')
        assert u'Номер телефона в международном формате' in signup
        assert u'Получить sms-код' in signup

    def test_labels_existing_at_worker_signup_activation(self):
        username = randint(10000000000, 99999999999999)
        signup = self.app.get('/signup/activation/{}/'.format(username))
        assert u'Номер телефона в международном формате' in signup
        assert u'Код подтверждения регистрации' in signup

    def test_signupl(self):
        form = self.app.get('/signup/').form
        username = randint(10000000000, 99999999999999)
        form['username'] = username
        print form
        response = form.submit().follow()
        print response.context
        self.assertEqual(response.context['username'].username, username)
        print response.context
        print response.template



