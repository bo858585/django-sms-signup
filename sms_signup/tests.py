# -*- coding: utf-8 -*-

"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

from django.core.urlresolvers import reverse
from django.utils.timezone import utc
from django.test import TestCase

from .models import ActivationSMSCode

import datetime

from random_words import RandomWords


class SMSSignupTests(TestCase):

    def test_signup_form_get(self):
        """
        Test the appearing of the signup page
        """
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, u"Войти")
        self.assertContains(response, u"Регистрация")
        self.assertContains(response, u"Восстановление пароля")
        self.assertContains(response, u"Номер телефона в международном формате")
        self.assertContains(response, u"Получить sms-код")

    def test_signup_form_post(self):
        """
        Test the redirect of the signup page after submitting the form
        """
        phone_number = "666666666666"

        response = self.client.post(
            reverse('signup'),
            {'username': phone_number},
            follow=True
        )
        self.assertRedirects(
            response,
            reverse('signup_activation', kwargs={"phone": phone_number})
        )

        self.assertContains(response, u"Войти")
        self.assertContains(response, u"Регистрация")
        self.assertContains(response, u"Восстановление пароля")
        self.assertContains(response, u"Номер телефона в международном формате")
        self.assertContains(response, phone_number)
        self.assertContains(response, u"Код подтверждения регистрации")
        self.assertContains(response, u"Активировать")

    def test_signup_activation_form_post(self):
        """
        Test the redirect and logging in of the signup activation page after submitting the form.
        
        """

        phone_number = "777777777777"

        # Genarates the random word for the sms code
        random_word = RandomWords()
        sms_code = random_word.random_word()

        # Create record with the random word at the db
        activation_sms_code_record = ActivationSMSCode.objects.create(
            sms_code=sms_code,
            phone=phone_number,
            sms_code_init_time=datetime.datetime.utcnow().replace(
                    tzinfo=utc),
            is_activated=False
        )
        activation_sms_code_record.save()

        # Send activation request and check entrance
        response = self.client.post(
            reverse('signup_activation', kwargs={"phone": phone_number}),
            {"username": phone_number, "sms_code": sms_code},
            follow=True
        )

        self.assertRedirects(
            response,
            reverse('home')
        )

        self.assertContains(response, u"Выйти")
        self.assertContains(response, u"Ваш аккаунт был активирован. Спасибо, за регистрацию")
