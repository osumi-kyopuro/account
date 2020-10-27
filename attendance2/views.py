from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from .forms import AttendForm
from builtins import str
from _datetime import timezone
from django.utils import timezone
from django.db.models import F, Q
from django.conf.locale import ja
from django.shortcuts import redirect, render
from django import forms
from .models import Attendance
#import .models

# Create your views here.
def list_check(request):#データ整合チェック
    from .models import Attendance
    Attendance.objects.filter(scheduled_attend_time__gt=F('scheduled_leave_time')).delete()
    latest_order = Attendance.objects.latest('id')
    if latest_order.attend_time!=None and latest_order.leave_time!=None:
        latest_order.work_time = latest_order.leave_time - latest_order.attend_time
    latest_order.save()
    c = Attendance.objects.filter(Q(user=latest_order.user), Q(scheduled_attend_time__range=(latest_order.scheduled_attend_time-timedelta(minutes=30),latest_order.scheduled_leave_time+timedelta(minutes=30)))|Q(scheduled_leave_time__range=(latest_order.scheduled_attend_time-timedelta(minutes=30),latest_order.scheduled_leave_time+timedelta(minutes=30)))|Q(scheduled_attend_time__lte=latest_order.scheduled_attend_time,scheduled_leave_time__gte=latest_order.scheduled_leave_time)).count()
    if c > 1:
        Attendance.objects.latest('id').delete()
    data = Attendance.objects.all()
    params = {  'message': 'データ一覧', 
                'data': data#データ整合完了データ
            }
    return render(request, 'attendance2/list.html', params)

def new(request):#シフト追加
    from .models import Attendance
    params = {'message': '', 'form': None}
    if request.method == 'POST':
        form = AttendForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_check')#データ整合チェック
        else:
            params['message'] = '再入力して下さい'
            params['form'] = form
    else:
        params['form'] = AttendForm()
    return render(request, 'attendance2/new.html', params)


def sortlist(request):#データ時系列順
    from .models import Attendance
    from django.db.models import Sum
    data = Attendance.objects.order_by("scheduled_attend_time")
    params = {  'message': 'データ一覧', 
                'data': data
            }
    return render(request, 'attendance2/sortlist.html', params)
 
 
def list(request):#データ登録順
    from .models import Attendance
    data = Attendance.objects.all()
    params = {'message': 'データ一覧', 'data': data}
    return render(request, 'attendance2/list.html', params)


from django.shortcuts import (
        render,
        redirect,
        get_object_or_404,
    )
from django.views.decorators.http import require_POST  # 追加する
from .models import Attendance
from .forms import AttendForm
def delete_menu(request):#データ削除メニュー
    from .models import Attendance
    data = Attendance.objects.all()
    params = {'message': 'データ一覧', 'data': data}
    return render(request, 'attendance2/delete_menu.html', params)
    
@require_POST
def delete(request):#データ削除関数
    delete_ids = request.POST.getlist('delete')
    if delete_ids:    
        Attendance.objects.filter(id__in=delete_ids).delete()
    return redirect('list')
    



def mylist(request):#自分のシフトデータ
    from .models import Attendance
    from django.db.models import Sum
    data = Attendance.objects.filter(user=request.user).order_by("scheduled_attend_time")
    absence_count=Attendance.objects.filter(user=request.user,attend_time=None ,leave_time=None,scheduled_leave_time__lt= datetime.now()).count()
    late_count = Attendance.objects.filter(user=request.user,attend_time__gt = F('scheduled_attend_time')).count()
    early_count = Attendance.objects.filter(user=request.user,leave_time__lt=F('scheduled_leave_time')).count()
    sum = data.aggregate(Sum('work_time'))
    params = {  'message': 'データ一覧', #メッセージ
                'data': data,#自分のシフトデータ
                'sum':sum,#総労働時間
                'user':request.user,#ログインユーザー名
                'absence_count':absence_count,#欠席回数
                'late_count':late_count,#遅刻回数
                'early_count':early_count#早退回数
            }
    return render(request, 'attendance2/mylist.html', params)



    
def attend_time(request):#出勤
    from .models import Attendance
    data=Attendance.objects.get(Q(user=request.user),Q(scheduled_attend_time__lt=datetime.now()+timedelta(minutes=30)),Q(scheduled_leave_time__gt=datetime.now()),Q(attend_time=None),Q(leave_time=None))
    data.attend_time = timezone.now()
    if data.attend_time > data.scheduled_attend_time:
        data.late=True
    data.save()
    params = {  'message': request.user,#アカウントユーザー名
                'attend_time':datetime.now().strftime('%H:%M:%S')#出勤時刻
            }
    return render(request, 'attendance2/attend_time.html',params)


 

def leave_time(request):#退勤
    from .models import Attendance
    data=Attendance.objects.get(Q(user=request.user),Q(leave_time=None),Q(attend_time__isnull=False))
    data.leave_time = timezone.now()
    if data.leave_time < data.scheduled_leave_time:
        data.early=True
    data.work_time=data.leave_time - data.attend_time
    data.save()
    params = {  'message': request.user,#アカウントユーザー名
                'leave_time':datetime.now().strftime('%H:%M:%S'),#退勤時刻
                'work_time':data.work_time#労働時間
            }
    return render(request, 'attendance2/leave_time.html',params)

def home(request):#TOPページ
    from .models import Attendance
    params = {'message': str(request.user)}
    #現在時刻が出勤予定時刻から30分以内であり、出勤も退勤もしていない時
    if Attendance.objects.filter(Q(user=request.user),Q(scheduled_attend_time__lt=datetime.now()+timedelta(minutes=30)),Q(scheduled_leave_time__gt=datetime.now()),Q(attend_time=None),Q(leave_time=None)).exists():
        #シフトデータがある時
        if Attendance.objects.filter(Q(user=request.user),Q(scheduled_leave_time__gt=datetime.now()),Q(attend_time=None)|Q(leave_time=None)).exists():
            data=Attendance.objects.filter(Q(user=request.user),Q(scheduled_leave_time__gt=datetime.now()),Q(attend_time=None)|Q(leave_time=None)).earliest('scheduled_attend_time')
            params = {  'message': request.user,#アカウントユーザー名表示
                        'attend_flag':True,#出勤ボタン表示flag
                        'leave_flag':False,#退勤ボタン表示flag
                        'data_flag':True,#データ存在flag
                        'data':data#次のシフト表示
                    }
        #シフトデータがない時
        else:
            params = {  'message': request.user,
                        'attend_flag':True,
                        'leave_flag':False,
                        'data_flag':False
                    }
    #出勤している時
    elif Attendance.objects.filter(Q(user=request.user),Q(leave_time=None),Q(attend_time__isnull=False)).exists():
        #シフトデータがある時
        if Attendance.objects.filter(Q(user=request.user),Q(scheduled_leave_time__gt=datetime.now()),Q(attend_time=None)|Q(leave_time=None)).exists():
            data=Attendance.objects.filter(Q(user=request.user),Q(scheduled_leave_time__gt=datetime.now()),Q(attend_time=None)|Q(leave_time=None)).earliest('scheduled_attend_time')
            params = {  'message': request.user,
                        'attend_flag':False,
                        'leave_flag':True,
                        'data_flag':True,
                        'data':data
                    }
        #シフトデータがない時
        else:
            params = {  'message': request.user,
                        'attend_flag':False,
                        'leave_flag':True,
                        'data_flag':False
                    }
    #退勤したか欠勤した時
    elif Attendance.objects.filter(user=request.user,scheduled_leave_time__gt=datetime.now()).exists():
        #シフトデータがある時
        if Attendance.objects.filter(Q(user=request.user),Q(scheduled_leave_time__gt=datetime.now()),Q(attend_time=None)|Q(leave_time=None)).exists():
            data=Attendance.objects.filter(Q(user=request.user),Q(scheduled_leave_time__gt=datetime.now()),Q(attend_time=None)|Q(leave_time=None)).earliest('scheduled_attend_time')
            params = {  'message': request.user,
                        'attend_flag':False,
                        'leave_flag':False,
                        'data_flag':True,
                        'data':data
                    }
        #シフトデータがない時
        else:
            params = {  'message': request.user,
                        'attend_flag':False,
                        'leave_flag':False,
                        'data_flag':False
                    }
    #シフトデータがない場合
    else:
        params = {  'message': request.user,
                    'attend_flag':False,
                    'leave_flag':False,
                    'data_flag':False
                }
    return render(request, 'attendance2/home.html',params)

