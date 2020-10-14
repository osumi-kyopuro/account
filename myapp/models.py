from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django import forms
from django.contrib.admin import widgets
import os

CHOICES = (
    #("request.POSTの中身", "画面に表示される内容"),
    ("管理者", "管理者"),
    ("一般人", "一般人"),
)

class CustomUser(AbstractUser):
    #authority = models.BooleanField(null=True,default=False)
    authority = models.CharField(verbose_name="カラム名",choices=CHOICES,max_length=100)
    