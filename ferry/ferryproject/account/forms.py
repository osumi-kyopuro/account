from django.contrib.auth.forms import UserCreationForm
from django import forms
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
# ユーザ作成フォームを継承
class SignUpForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username','password1', 'password2',)
    