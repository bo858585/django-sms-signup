# -*- coding: utf-8 -*-


class SMSAuthBackend(object):

    def authenticate(self, username=None, password=None):
        user = get_object_or_None(
            User,
            username=username,
            password=password
        )
        if not user:
            return
        if user.check_password(password):
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
