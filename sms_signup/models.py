# -*- coding: utf-8 -*-

from django.db import models

# Create your models here.


class ActivationSMSCode(models.Model):
    """
    Table with sms activation codes for user which want to register
    """
    sms_code = models.CharField(max_length=30)
    phone = models.CharField(max_length=14)
    sms_code_init_time = models.DateTimeField(null=True, auto_now_add=True)
    is_activated = models.BooleanField(default=False)
