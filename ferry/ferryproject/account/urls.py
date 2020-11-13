from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.index, name='index'),#アカウントページ
    path('home/', views.home, name='home'),#アカウントログイン
    path('signup/', views.signup, name='signup'),#ユーザ登録
]