# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import View
from django.contrib import auth, messages
from django.utils.translation import ugettext as _
from django.utils.timezone import utc
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model

from .forms import RegistrationForm, ActivationForm, LoginForm, PasswordRecoveryForm
from .models import ActivationSMSCode
from .backend import SMSAuthBackend

from random_words import RandomWords


import datetime
from datetime import timedelta

from smsaero.utils import send_sms_async

ACTIVATION_ALREADY_HAS_BEEN = _(u'Активация уже производилась')
WRONG_ACTIVATION_CODE = _(u'Неверный код активации')
ACTIVATION_PERIOD_EXPIRED = _(u'Истек период активации')
LOGIN_ERROR = _(u'При входе возникла ошибка')
SEND_MESSAGE_ERROR = _(u'Ошибка при попытке отправки сообщения')
ACCOUNT_ACTIVATED = _(u"Ваш аккаунт был активирован. Спасибо, за регистрацию")
NO_SUCH_USER = _(u"Нет такого пользователя")
PASSWORD_HAS_BEEN_SENT = _(u"Пароль был отправлен")
ACTIVATION_PERIOD = 2  # days

User = get_user_model()


def redirect_with_message(request, message_type, message_text, redirect_page):
    """
    Redirects to the page and shows the message
    """

    messages.add_message(
        request,
        message_type,
        message_text
    )
    return HttpResponseRedirect(reverse(redirect_page))


class RegistrationView(View):

    """
    User registration
    """

    form_class = RegistrationForm
    template_name = 'sms_signup/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial={})
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['username']
            # Genarates the random word for the sms code
            random_word = RandomWords()
            sms_code = random_word.random_word()

            # Creates the record with the random
            # activation word and the phone number
            ActivationSMSCode.objects.create(
                sms_code=sms_code,
                phone=phone,
                sms_code_init_time=datetime.datetime.utcnow().replace(
                    tzinfo=utc)
            )

            try:
                print sms_code, phone
                # Sends sms message with the random word
                send_sms_async(phone, sms_code)
            except Exception:
                return redirect_with_message(
                    request,
                    messages.ERROR,
                    SEND_MESSAGE_ERROR,
                    "signup"
                )

            return HttpResponseRedirect(
                reverse('signup_activation',
                        kwargs={
                            'phone': form.cleaned_data['username']
                        }
                        )
            )

        return render(request, self.template_name, {'form': form})


class ActivationView(View):

    """
    User account activation
    """

    form_class = ActivationForm
    initial = {}
    template_name = 'sms_signup/activation.html'

    def get(self, request, *args, **kwargs):
        phone = kwargs.get('phone', None)
        # Init form with the phone number
        self.initial['username'] = phone
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['username']

            # Compares the db sms code and request sms code
            sms_code_value = form.cleaned_data['sms_code']
            try:
                user_sms_code = ActivationSMSCode.objects.get(
                    sms_code=sms_code_value,
                    phone=phone
                )
            except ActivationSMSCode.DoesNotExist:
                return redirect_with_message(
                    request,
                    messages.ERROR,
                    WRONG_ACTIVATION_CODE,
                    "signup"
                )

            if not user_sms_code.is_activated:
                # Checks that activation period is not expired
                signup_time = datetime.datetime.utcnow().replace(
                    tzinfo=utc) - timedelta(days=ACTIVATION_PERIOD)
                if signup_time < user_sms_code.sms_code_init_time:
                    # Creates the user
                    password = User.objects.make_random_password()
                    username = form.cleaned_data['username']
                    user = self.create_user(
                        phone=username,
                        password=password
                    )
                    user_sms_code.is_activated = True
                    user_sms_code.save()
                    print password, username
                    # Sends the password in the sms
                    try:
                        send_sms_async(username, password)
                    except Exception as e:
                        print str(e)
                        return redirect_with_message(
                            request,
                            messages.ERROR,
                            SEND_MESSAGE_ERROR,
                            "signup"
                        )

                    messages.add_message(
                        request,
                        messages.INFO,
                        ACCOUNT_ACTIVATED
                    )

                    # Authenticates the user
                    return login(request, username, password)
                else:
                    return redirect_with_message(
                        request,
                        messages.ERROR,
                        ACTIVATION_PERIOD_EXPIRED,
                        "signup"
                    )
            else:
                return redirect_with_message(
                    request,
                    messages.ERROR,
                    ACTIVATION_ALREADY_HAS_BEEN,
                    "signup"
                )

        return render(request, self.template_name, {'form': form})

    def create_user(self, phone, password):
        """
        Creating the user
        """
        # email=phone, because
        # User._meta.get_field('email')._unique = True at common
        # need to remove later
        user = User.objects.create_user(
            username=phone,
            password=password,
            email=phone
        )
        user.backend = SMSAuthBackend
        user.profile_type = 'worker'#
        user.get_profile_model().phone = phone#

        user.save()
        return user


class LoginView(View):

    """
    User login
    """

    form_class = LoginForm
    initial = {}
    template_name = 'sms_signup/login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return login(
                request,
                request.POST['username'],
                request.POST['password']
            )

        return render(request, self.template_name, {'form': form})

    def logout(request):
        auth.logout(request)
        return HttpResponseRedirect("/account/loggedout/")


def login(request, username, password):
    """
    Log in the user
    """

    user = auth.authenticate(
        username=username,
        password=password
    )

    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect(reverse("home"))
    else:
        return redirect_with_message(
            request,
            messages.ERROR,
            LOGIN_ERROR,
            "login"
        )


class PasswordRecoveryView(View):

    """
    Password recovery
    """

    form_class = PasswordRecoveryForm
    template_name = 'sms_signup/password_recovery.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial={})
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['username']
            password = User.objects.make_random_password()

            try:
                u = User.objects.get(username__exact=phone)
            except:
                return redirect_with_message(
                    request,
                    messages.ERROR,
                    NO_SUCH_USER,
                    "forgot_password"
                )

            u.set_password(password)
            u.save()

            try:
                print password, phone
                # Sends sms message with the random word
                send_sms_async(phone, password)
            except Exception:
                return redirect_with_message(
                    request,
                    messages.ERROR,
                    SEND_MESSAGE_ERROR,
                    "forgot_password"
                )

            return redirect_with_message(
                request,
                messages.INFO,
                PASSWORD_HAS_BEEN_SENT,
                "home"
            )
        return render(request, self.template_name, {'form': form})
