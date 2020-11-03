from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login

User = get_user_model()
def index(request):
    return render(request, 'myapp/index.html')
 
 
@login_required
def home(request):
    return render(request, 'myapp/home.html')

def signup(request):#アカウント作成
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')#ユーザー名
            raw_pass = form.cleaned_data.get('password1')#パスワード
            authority=form.cleaned_data.get('authority')#権限
            user = authenticate(request, username=username, password1=raw_pass,authority=authority)
            user=form.save()
            return render(request, 'myapp/index.html')
    else:
        form = SignUpForm()
    return render(request, 'myapp/signup.html', {'form': form})




