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

class Images(models.Model):
    images=models.ImageField(upload_to='')


class CustomUser(AbstractUser):
    mail = models.EmailField(max_length=100)
    authority = models.CharField(verbose_name="カラム名",default='一般人',choices=CHOICES,max_length=100,blank=True, null=True)
    