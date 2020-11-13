from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django import forms
from django.contrib.admin import widgets
import os


class CustomUser(AbstractUser):
    pass
    
    