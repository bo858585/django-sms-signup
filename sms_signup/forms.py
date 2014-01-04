# -*- coding: utf-8 -*-

from django import forms
from django.forms.widgets import TextInput
from django.utils.translation import gettext as _
from django.contrib.auth import authenticate

#from jm_common.users.models import User
from django.contrib.auth.models import User

from .models import ActivationSMSCode


PHONE_REGEX = r'^[\d]{11,14}$'

PHONE_MAX_LENGTH = 14
ACTIVATION_CODE_MAX_LENGTH = 30

PHONE_LABEL = _(u"Номер телефона в международном формате")
PHONE_ERROR = _(
    u"Укажите номер телефона в международном формате (только цифры)")
USER_ALREADY_EXISTS = _(u"Пользователь с таким телефоном уже зарегистрирован")
USER_NOT_EXISTS = _(u"Пользователь с таким телефоном не существует")
WRONG_ACTIVATION_CODE = _(u"Неверный код активации")
WRONG_PASSWORD = _(u"Неверный пароль")
INACTIVE_ACCOUNT = _(u"Ваш аккаунт неактивен")
ACTIVATION_CODE_LABEL = _(u"Код подтверждения регистрации")
PASSOWRD_LABEL = _(u"Пароль")


class RegistrationForm(forms.Form):

    """
    Form for registering a new user account.

    Validates that the requested username (phone) is not already in use,
    and requires the password to be entered.

    """

    username = forms.RegexField(
        regex=PHONE_REGEX,
        widget=TextInput(),
        max_length=PHONE_MAX_LENGTH,
        label=PHONE_LABEL,
        error_messages={
            'invalid': PHONE_ERROR,
        }
    )

    def clean_username(self):
        """
        Validate that the username (phone number) exists

        """
        existing = User.objects.filter(
            username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError(USER_ALREADY_EXISTS)
        else:
            return self.cleaned_data['username']


class ActivationForm(forms.Form):

    """
    Registration activation form
    """

    username = forms.RegexField(
        regex=PHONE_REGEX,
        max_length=PHONE_MAX_LENGTH,
        widget=TextInput(
            attrs={
                'class': 'disabled',
                'readonly': 'readonly'
            }
        ),
        label=PHONE_LABEL,
        error_messages={
            'invalid': PHONE_ERROR,
        }
    )

    sms_code = forms.CharField(
        label=ACTIVATION_CODE_LABEL,
        max_length=ACTIVATION_CODE_MAX_LENGTH,
    )

    def clean_username(self):
        """
        Validate that the username (phone) exists

        """
        existing = User.objects.filter(
            username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError(USER_ALREADY_EXISTS)
        else:
            return self.cleaned_data['username']

    def clean_sms_code(self):
        """
        Validate that the user with the phone and the sms_code
        exists in db

        """
        try:
            worker_sms_code = ActivationSMSCode.objects.get(
                sms_code=self.cleaned_data['sms_code'],
                phone=self.cleaned_data['username']
            )
        except ActivationSMSCode.DoesNotExist:
            raise forms.ValidationError(WRONG_ACTIVATION_CODE)

        return self.cleaned_data['sms_code']


class LoginForm(forms.Form):

    """
    Registration activation form
    """

    username = forms.RegexField(
        regex=PHONE_REGEX,
        max_length=PHONE_MAX_LENGTH,
        widget=TextInput(),
        label=PHONE_LABEL,
        error_messages={
            'invalid': PHONE_ERROR,
        }
    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
        label=_(PASSOWRD_LABEL),
    )

    def clean_username(self):
        """
        Validate that the username (phone) exists.

        """
        existing = User.objects.filter(
            username__iexact=self.cleaned_data['username'])
        if not existing.exists():
            raise forms.ValidationError(USER_NOT_EXISTS)
        else:
            return self.cleaned_data['username']

    def clean_password(self):
        """
        Validate that the username (phone) with
        the password exists and user is active.

        """

        try:
            user = authenticate(
                username=self.cleaned_data['username'],
                password=self.cleaned_data['password']
            )
        except KeyError:
            raise forms.ValidationError(WRONG_PASSWORD)

        if user is None:
            raise forms.ValidationError(WRONG_PASSWORD)
        elif user is not None and not user.is_active:
            raise forms.ValidationError(INACTIVE_ACCOUNT)
        else:
            return self.cleaned_data['password']


class PasswordRecoveryForm(forms.Form):

    """
    Form for password recovery for a user account.
    """

    username = forms.RegexField(
        regex=PHONE_REGEX,
        widget=TextInput(),
        max_length=PHONE_MAX_LENGTH,
        label=PHONE_LABEL,
        error_messages={
            'invalid': PHONE_ERROR,
        }
    )

    def clean_username(self):
        """
        Validate that the username (phone number) exists

        """
        existing = User.objects.filter(
            username__iexact=self.cleaned_data['username'])
        print existing
        if not existing.exists():
            raise forms.ValidationError(USER_NOT_EXISTS)
        else:
            return self.cleaned_data['username']
