# -*- coding: utf-8 -*-

"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

from django.core.urlresolvers import reverse
from django.utils.timezone import utc
from django.utils.translation import ugettext as _
from django.test import TestCase

from .models import ActivationSMSCode

import datetime

from random_words import RandomWords


INPUT = _(u"Войти")
REGISTRATION = _(u"Регистрация")
PASSWORD_RECOVERY = _(u"Восстановление пароля")
PHONE_INTERNATIONAL_FORMAT =\
    _(u"Номер телефона в международном формате")
RECEIVE_SMS_CODE = _(u"Получить sms-код")
REGISTRATION_CONFIRM_CODE = _(u"Код подтверждения регистрации")
ACTIVATE = _(u"Активировать")
LOGOUT = _(u"Выйти")
ACCOUNT_IS_ACTIVE = _(u"Ваш аккаунт был активирован. Спасибо, за регистрацию")


class SMSSignupTests(TestCase):
    """
    @phone_number must be real number
    """

    def setUp(self):
        self.phone_number = "79215836781"

    def test_signup_form_get(self):
        """
        Test the appearing of the signup page
        """

        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, INPUT)
        self.assertContains(response, REGISTRATION)
        self.assertContains(response, PASSWORD_RECOVERY)
        self.assertContains(
            response,
            PHONE_INTERNATIONAL_FORMAT)
        self.assertContains(response, RECEIVE_SMS_CODE)

    def test_signup_form_post(self):
        """
        Test the redirect of the signup page after submitting the form
        """

        response = self.client.post(
            reverse('signup'),
            {'username': self.phone_number},
            follow=True
        )
        self.assertRedirects(
            response,
            reverse('signup_activation', kwargs={"phone": self.phone_number})
        )

        self.assertContains(response, INPUT)
        self.assertContains(response, REGISTRATION)
        self.assertContains(response, PASSWORD_RECOVERY)
        self.assertContains(
            response,
            PHONE_INTERNATIONAL_FORMAT)
        self.assertContains(response, self.phone_number)
        self.assertContains(response, REGISTRATION_CONFIRM_CODE)
        self.assertContains(response, ACTIVATE)

    def test_signup_activation_form_post(self):
        """
        Test the redirect and logging in of the signup
        activation page after submitting the form.

        """

        # Genarates the random word for the sms code
        random_word = RandomWords()
        sms_code = random_word.random_word()

        # Create record with the random word at the db
        activation_sms_code_record = ActivationSMSCode.objects.create(
            sms_code=sms_code,
            phone=self.phone_number,
            sms_code_init_time=datetime.datetime.utcnow().replace(
                tzinfo=utc),
            is_activated=False
        )
        activation_sms_code_record.save()

        # Send activation request and check entrance
        response = self.client.post(
            reverse('signup_activation', kwargs={"phone": self.phone_number}),
            {"username": self.phone_number, "sms_code": sms_code},
            follow=True
        )

        self.assertRedirects(
            response,
            reverse('home')
        )

        self.assertContains(response, LOGOUT)
        self.assertContains(
            response,
            ACCOUNT_IS_ACTIVE)
