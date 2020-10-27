from django.urls import path
from . import views
import re
urlpatterns = [
    path('', views.home, name='home'),#TOPページ
    path('attend_time',views.attend_time,name='attend_time'),#出勤
    path('leave_time', views.leave_time, name='leave_time'),#退勤
    path('new', views.new, name='new'),#シフト追加フォーム
    path('list', views.list, name='list'),#全シフトデータ
    path('mylist', views.mylist, name='mylist'),#自分のシフトデータ
    path('sortlist', views.sortlist, name='sortlist'),#シフトデータ時系列順
    path('list_check', views.list_check, name='list_check'),#データ整合
    path('delete_menu', views.delete_menu, name='delete_menu'),#データ整合
    path('delete', views.delete, name='delete'),#データ削除
]